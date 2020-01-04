from my_app.settings import db_config
from sqlalchemy import desc, asc
import my_app.tool_box as tool
from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Names, Orders
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

        # if rec_num == 2437:
        #     print (cust_id, cust_name, cust_so_num)
        #     print (valid_cust_id, valid_cust_name, valid_so_num)
        #     exit()

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
    # Flag Bookings "DELETE" that have no useful data
    #
    if len(delete_list) > 0:
        my_str = ""
        for delete_id in delete_list:
            my_str = my_str + "id = " + str(delete_id) + " or "

        my_str = my_str[:-3] + ";"
        sql = "UPDATE bookings SET hash_value = 'DELETE' WHERE " + my_str
        sql_results = db.engine.execute(sql)

        print("Rows Marked DELETE ", sql_results.rowcount)

        # Physically Delete the marked records
        del_rows = Bookings.query.filter_by(hash_value = 'DELETE').delete()
        print('Actually Deleted ', del_rows)
        db.session.commit()

        rec_count = Bookings.query.all()
        print('Bookings size NOW', len(rec_count))
    else:
        print ('No Bookings Records to Delete')

    #
    # Loop over the repair records
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

        if not valid_cust_name:
            # print("Customer Name Needed")
            # We need a cust_name
            if valid_cust_id:
                name1 = cust_id_dict[cust_id][0]
            if valid_so_num:
                name2 = cust_so_dict[cust_so_num][1]
            # print("\t\t", rec_num, "cust name options:", name1, ' / ', name2)

            # Select a name
            if name1 == 'INVALID' and name2 == 'INVALID':
                cust_name = 'INVALID'
            elif name1 != 'INVALID':
                cust_name = name1
            elif name2 != 'INVALID':
                cust_name = name2

            r.erp_end_customer_name = cust_name
            # print("\t\t\tName Results:", cust_name)
            # print()

        if not valid_cust_id:
            #print("Customer ID Needed")
            # We need a cust_id
            if valid_cust_name:
                id1 = cust_name_dict[cust_name][0]
            if valid_so_num:
                id2 = cust_so_dict[cust_so_num][0]
            #print("\t\t", rec_num, "cust id options:", id1, ' / ', id2)

            # Select an ID
            if id1 == 'INVALID' and id2 == 'INVALID':
                cust_id = 'INVALID'
            elif id1 != 'INVALID':
                cust_id = id1
            elif id2 != 'INVALID':
                cust_id = id2

            r.end_customer_global_ultimate_id = cust_id
            # print("\t\t\tID Results:", cust_id)
            # print()
        r.hash_value = "REPAIRED"
        db.session.commit()
        print(rec_num)

    exit()



    #
    #
    # for r in my_bookings:
    #     cust_name = r.erp_end_customer_name
    #     cust_id = r.end_customer_global_ultimate_id
    #     cust_so_num = r.erp_sales_order_number
    #
    #     if cust_name not in cust_name_dict:



        #
        #
        # if valid_cust_id and (valid_cust_name or valid_so_num):
        #     if cust_name == 'UNKNOWN':
        #         print (cust_id, cust_name, cust_so_num)
        #         time.sleep(.1)
        #
        # if valid_cust_name and (valid_cust_id or valid_so_num):
        #     if cust_name == 'UNKNOWN':
        #         print (cust_id, cust_name, cust_so_num)
        #         time.sleep(.1)
        #     # print(cust_id, cust_name, cust_so_num)
        #
        # if valid_so_num and (valid_cust_id or valid_cust_name):
        #     if cust_name == 'UNKNOWN':
        #         print (cust_id, cust_name, cust_so_num)
        #         time.sleep(.1)






        # # If cust_id AND cust_name are valid then add to the
        # if (cust_id != '-999') and (cust_name_dict != 'UNKNOWN'):
        #     cust_id_dict[cust_id] = cust_name
        #     cust_name_dict[cust_name] = cust_id
        #
        #     if cust_so_num != '-7777' and cust_so_num != '-6666' and cust_so_num != '-9999':
        #         cust_so_dict[cust_so_num] = cust_id

    print('phase 0 done')
    print("records needing repair", len(repair_list))
    exit()

    # Now loop over every record and improve the data
    for r in my_bookings:
        row_num = r.id
        cust_name = r.erp_end_customer_name
        cust_id = r.end_customer_global_ultimate_id
        cust_so_num = r.erp_sales_order_number
        update_flag = False

        if cust_id == '-999':
            if cust_name in cust_name_dict:
                cust_id = cust_name_dict[cust_name]
                update_flag = True
            elif cust_so_num in cust_so_dict:
                cust_id = cust_so_dict[cust_so_num]
                update_flag = True

        if update_flag is True:
            my_rec = Bookings.query.filter(Bookings.id == row_num)
            my_rec.end_customer_global_ultimate_id = cust_id
            db.session.commit()

    print(len(cust_name_dict))
    print(len(cust_so_dict))
    print(len(cust_id_dict))
    exit()


    kwargs = {'end_customer_global_ultimate_id': '-999',
              'erp_sales_order_number': '-7777',
              'erp_end_customer_name' : 'UNKNOWN'}
    my_bookings = Bookings.query.filter_by(**kwargs).delete()
    print(my_bookings)
    db.session.commit()

    #
    # Get all the names with no customer id (-999)
    #
    my_bookings = Bookings.query.filter(Bookings.end_customer_global_ultimate_id == "-999").all()
        # filter(Bookings.erp_end_customer_name != "UNKNOWN").all()
    print(len(my_bookings), " Bookings Records with INVALID Customer ID")
    names_with_no_id = {}
    for x in my_bookings:
        names_with_no_id[x.erp_end_customer_name] = (x.end_customer_global_ultimate_id, x.erp_sales_order_number)
    print("Customers Names WITHOUT an ID ", len(names_with_no_id))

    #
    # Get all ORDERS with VALID customer ids
    #
    # my_bookings = Bookings.query.filter(Bookings.end_customer_global_ultimate_id != "-999"). \
    #     filter(Bookings.erp_sales_order_number != "UNKNOWN").all()
    # print(len(my_bookings), " Bookings Records with VALID Customer ID")



    #
    # Get all names with VALID customer ids
    #
    my_bookings = Bookings.query.filter(Bookings.end_customer_global_ultimate_id != "-999").all()
    print(len(my_bookings), " Bookings Records with VALID Customer ID")
    names_with_id = {}
    orders_with_id = {}
    for x in my_bookings:
        names_with_id[x.erp_end_customer_name] = x.end_customer_global_ultimate_id
        orders_with_id[x.erp_sales_order_number] = x.end_customer_global_ultimate_id
    print("Customers Names WITH VALID an ID ", len(names_with_id))

    if "-9999" in orders_with_id:
        del orders_with_id["-9999"]
    if "-6666" in orders_with_id:
        del orders_with_id["-6666"]
    if "-7777" in orders_with_id:
        del orders_with_id["-7777"]

    # for k, v in orders_with_id.items():
    #     print(k, v)
    #     time.sleep(.5)
    print(len(orders_with_id))
    # exit()
    #
    # Try to Match the Customer Names with existing Customer IDs
    #
    matched = 0
    possible_cust = ''
    for cust_name, cust_info in names_with_no_id.items():
        cust_id = cust_info[0]
        cust_order_num = cust_info[1]

        if cust_name in names_with_id:
            # We Got an Exact Match on an existing
            print('EXACT NAME Matched ', cust_name)
            names_with_no_id[cust_name] = names_with_id[cust_name]

        elif cust_order_num in orders_with_id:
            print('Matched Order Number', cust_name, cust_order_num, orders_with_id[cust_order_num])
            time.sleep(.5)

        else:
            # Try the best fuzzy match
            best_match = 0
            for k, v in names_with_id.items():
                match_ratio = fuzz.ratio(cust_name, k)
                if match_ratio > best_match:
                    possible_cust = k
                    best_match = match_ratio
            if best_match >= 80:
                print("BEST match ", best_match, ": ", cust_name, " / ", possible_cust)
                names_with_no_id[cust_name] = names_with_id[k]
            else:
                print("WEAK match ", best_match, ": ", cust_name, " / ", possible_cust)
    print()
    print()
    for k, v in names_with_no_id.items():
        print(k, " / ", v)

    print(matched)
    exit()



    #
    # Create New Tables based on imported & updated data
    #
    # tool.drop_tables("Customer_Ids")
    # tool.create_tables("Customer_Ids")
    #
    # tool.drop_tables("Customer_Names")
    # tool.create_tables("Customer_Names")
    #
    # tool.drop_tables("Orders")
    # tool.create_tables("Orders")

    #
    # Create Customer ID Table
    #
    sql = "INSERT INTO `customer_ids` (`end_customer_global_ultimate_id`) " + \
          "SELECT DISTINCT `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"
    sql_results = db.engine.execute(sql)
    print("Loaded Unique Customer IDs:", sql_results.rowcount, ' rows')

    #
    # Create Customer Names Table
    #
    sql = "INSERT INTO `customer_names` (`erp_end_customer_name`, `end_customer_global_ultimate_id`) " + \
          "SELECT DISTINCT `erp_end_customer_name`, `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"
    sql_results = db.engine.execute(sql)
    print("Loaded Customer_Names:", sql_results.rowcount, ' rows')

    #
    # Create Customer Orders Table
    #
    sql = "INSERT INTO `orders` (`erp_sales_order_number`, `end_customer_global_ultimate_id`) " + \
          "SELECT DISTINCT `erp_sales_order_number`, `end_customer_global_ultimate_id` FROM " + \
          "`" + db_config['DATABASE'] + "`.`Bookings`"

    sql_results = db.engine.execute(sql)
    print("Loaded Customer Unique Order Numbers:", sql_results.rowcount)

    exit()


if __name__ == "__main__" and __package__ is None:
    scrub_new_data()
