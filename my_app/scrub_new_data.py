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

    my_bookings = Bookings.query.order_by(Bookings.id.asc())
    # print(len(my_bookings))
    cust_name_dict = {}  # {cust_name:cust_id}
    cust_id_dict = {}  # {cust_id:cust_name}
    cust_so_dict = {}  # {so:cust_id}

    # Loop through and build reference dicts
    for r in my_bookings:
        cust_name = r.erp_end_customer_name
        cust_id = r.end_customer_global_ultimate_id
        cust_so_num = r.erp_sales_order_number

        if (cust_id != '-999') and (cust_name_dict != 'UNKNOWN'):
            cust_id_dict[cust_id] = cust_name
            cust_name_dict[cust_name] = cust_id

            if cust_so_num != '-7777' and cust_so_num != '-6666' and cust_so_num != '-9999':
                cust_so_dict[cust_so_num] = cust_id


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
