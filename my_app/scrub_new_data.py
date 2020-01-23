from my_app.settings import db_config
from sqlalchemy import desc, asc
import my_app.tool_box as tool
from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Aliases, Sales_Orders
from fuzzywuzzy import fuzz
import time


def scrub_new_data():
    #
    # Scrub Raw Bookings Table of Invalid Data
    #
    rec_count = Bookings.query.all()
    print('Bookings size start', len(rec_count))

    #
    # First Step: Fix and Update Bad SO Nums
    # For SOs with these 3 numbers create an SO number from 15 chars cust_name + so_number
    #
    so_records = Bookings.query.filter((Bookings.erp_sales_order_number == "-9999") |
                                    (Bookings.erp_sales_order_number == "-6666") |
                                    (Bookings.erp_sales_order_number == "-7777")).all()
    for r in so_records:
        cust_so_num = (r.erp_end_customer_name[:15]).replace(' ', '_')+r.erp_sales_order_number
        r.erp_sales_order_number = cust_so_num
    db.session.commit()

    #
    # Second Step: Loop over Bookings and Build Indexes of following 3 Unique Identifiers
    #
    cust_name_dict = {}  # {cust_name:cust_id}
    cust_id_dict = {}  # {cust_id:cust_name}
    cust_so_dict = {}  # {so:cust_id}
    repair_list = []
    delete_list = []

    my_bookings = Bookings.query.order_by(Bookings.id.asc())
    for r in my_bookings:
        valid_cust_name = False
        valid_cust_id = False
        valid_so_num = False

        rec_num = r.id
        cust_name = r.erp_end_customer_name
        cust_id = r.end_customer_global_ultimate_id
        cust_so_num = r.erp_sales_order_number

        # Check Validity of each
        if cust_name != 'UNKNOWN':
            valid_cust_name = True
        else:
            cust_name = 'INVALID'

        if cust_id != '-999':
            valid_cust_id = True
        else:
            cust_id = 'INVALID'

        if cust_so_num[:7] != 'UNKNOWN':
            valid_so_num = True
        else:
            cust_so_num = 'INVALID'

        # Is this record able to be repaired ?
        # Flag this record to DELETE if ALL 3 are invalid
        if (not valid_cust_name) and (not valid_cust_id) and (not valid_so_num):
            delete_list.append(r.id)
            continue

        # Create a dict entry for all Valid values
        if valid_cust_name:
            cust_name_dict[cust_name] = [cust_id, cust_so_num]
        if valid_cust_id:
            cust_id_dict[cust_id] = [cust_name, cust_so_num]
        if valid_so_num:
            cust_so_dict[cust_so_num] = [cust_id, cust_name]

        # Does this record need repair ?
        if (not valid_cust_name) or (not valid_cust_id) or (not valid_so_num):
            repair_list.append([rec_num, valid_cust_name, valid_cust_id, valid_so_num])

    #
    # Step 3: Flag Bookings "DELETE" that have no useful data / backup and remove from production
    #
    if len(delete_list) > 0:
        my_str = ""
        for delete_id in delete_list:
            my_str = my_str + "id = " + str(delete_id) + " or "

        my_str = my_str[:-3] + ";"
        sql = "UPDATE bookings SET hash_value = 'DELETE' WHERE " + my_str
        sql_results = db.engine.execute(sql)

        print("Rows Marked DELETE ", sql_results.rowcount)

        # Backup Deleted Rows
        sql = "CREATE TABLE bookings_deleted LIKE bookings;"
        sql_results = db.engine.execute(sql)
        sql = "INSERT INTO bookings_deleted SELECT * FROM bookings WHERE hash_value = 'DELETE';"
        sql_results = db.engine.execute(sql)

        # Physically Delete the marked records
        del_rows = Bookings.query.filter_by(hash_value = 'DELETE').delete()
        print('Actually Deleted ', del_rows)
        db.session.commit()

        rec_count = Bookings.query.all()
        print('Bookings size NOW', len(rec_count))
    else:
        print ('No Bookings Records to Delete')

    #
    # Step 4: Loop over the repair records to assign a valid Cust_name / Cust_id
    #
    print("Repair List is:", len(repair_list))
    for repair_rec in repair_list:
        r = Bookings.query.filter_by(id=repair_rec[0]).first()
        rec_num = r.id
        cust_name = r.erp_end_customer_name
        cust_id = r.end_customer_global_ultimate_id
        cust_so_num = r.erp_sales_order_number
        valid_cust_name = repair_rec[1]
        valid_cust_id = repair_rec[2]
        valid_so_num = repair_rec[3]

        name1, name2 = 'INVALID', 'INVALID'
        id1, id2 = 'INVALID', 'INVALID'

        # Do we need a cust_name?
        if not valid_cust_name:
            if valid_cust_id:
                name1 = cust_id_dict[cust_id][0]
            if valid_so_num:
                name2 = cust_so_dict[cust_so_num][1]

            # Select a name
            if name1 == 'INVALID' and name2 == 'INVALID':
                cust_name = 'INVALID'
            elif name1 != 'INVALID':
                cust_name = name1
            elif name2 != 'INVALID':
                cust_name = name2

            # Set a valid cust_name
            r.erp_end_customer_name = cust_name

        # Do we need a cust_id ?
        if not valid_cust_id:
            if valid_cust_name:
                id1 = cust_name_dict[cust_name][0]
            if valid_so_num:
                id2 = cust_so_dict[cust_so_num][0]

            # Select an ID
            if id1 == 'INVALID' and id2 == 'INVALID':
                cust_id = 'INVALID'
            elif id1 != 'INVALID':
                cust_id = id1
            elif id2 != 'INVALID':
                cust_id = id2

            # Set a valid cust_id
            r.end_customer_global_ultimate_id = cust_id

        r.hash_value = "REPAIRED"
        db.session.commit()
        print(rec_num)

    #
    # Create New Tables based on imported & updated data
    #
    tool.drop_tables("Web_Orders")
    tool.drop_tables("Sales_Orders")
    tool.drop_tables("Customer_Aliases")
    tool.drop_tables("Customer_Ids")

    tool.create_tables("Customer_Ids")
    tool.create_tables("Customer_Aliases")
    tool.create_tables("Sales_Orders")
    tool.create_tables("Web_Orders")

    #
    # Create Customer ID Table
    #
    sql = "INSERT INTO `customer_ids` (`customer_id`) " + \
          "SELECT DISTINCT `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"
    sql_results = db.engine.execute(sql)
    print("Loaded Unique Customer IDs:", sql_results.rowcount, ' rows')

    #
    # Create Customer Alias Table
    #
    sql = "INSERT INTO `customer_aliases` (`customer_alias`, `customer_id`) " + \
          "SELECT DISTINCT `erp_end_customer_name`, `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"
    sql_results = db.engine.execute(sql)
    print("Loaded Customer_Aliases:", sql_results.rowcount, ' rows')

    #
    # Create Customer Sales Order Table
    #
    sql = "INSERT INTO `sales_orders` (`so_number`, `customer_id`) " + \
          "SELECT DISTINCT `erp_sales_order_number`, `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"
    sql_results = db.engine.execute(sql)
    print("Loaded Customer Unique Order Numbers:", sql_results.rowcount)

    #
    # Create Customer Web Orders Table
    #
    sql = "INSERT INTO `web_orders` (`web_order_id`, `customer_id`) " + \
          "SELECT DISTINCT `web_order_id`, `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"
    sql_results = db.engine.execute(sql)
    print("Loaded Customer Web Order Numbers:", sql_results.rowcount)

    sql = "DELETE FROM `web_orders` WHERE `web_order_id` = 'UNKNOWN'"
    sql_results = db.engine.execute(sql)
    print("Scrubbed Customer Unique Web Order Numbers:", sql_results.rowcount)

    return


if __name__ == "__main__" and __package__ is None:
    scrub_new_data()

