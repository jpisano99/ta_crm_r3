from my_app.settings import db_config
from sqlalchemy import desc, asc
import my_app.tool_box as tool
from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Names, Orders
import time


def scrub_new_data():
    #
    # Scrub Raw Bookings Table of Invalid Data
    #
    kwargs = {'end_customer_global_ultimate_id': '-999',
              'erp_sales_order_number': '-7777',
              'erp_end_customer_name' : 'UNKNOWN'}
    my_bookings = Bookings.query.filter_by(**kwargs).delete()
    print(my_bookings)
    db.session.commit()

    #
    # Get all the names with no customer id (-999)
    #
    my_bookings = Bookings.query.filter(Bookings.end_customer_global_ultimate_id == "-999"). \
        filter(Bookings.erp_end_customer_name != "UNKNOWN").all()
    print(len(my_bookings), " Bookings Records with INVALID Customer ID")
    names_with_no_id = {}
    for x in my_bookings:
        names_with_no_id[x.erp_end_customer_name] = x.end_customer_global_ultimate_id
    print("Customers Names WITHOUT an ID ", len(names_with_no_id))

    #
    # Get all names with VALID customer ids
    #
    my_bookings = Bookings.query.filter(Bookings.end_customer_global_ultimate_id != "-999").all()
    print(len(my_bookings), " Bookings Records with VALID Customer ID")
    names_with_id = {}
    for x in my_bookings:
        names_with_id[x.erp_end_customer_name] = x.end_customer_global_ultimate_id
    print("Customers Names WITH VALID an ID ", len(names_with_id))

    for k, v in names_with_no_id.items():
        if k in names_with_id:
            print('Matched ', k)
        else:
            print("NO match ", k)


    exit()



    #
    # Create New Tables based on imported & updated data
    #
    tool.drop_tables("Customer_Ids")
    tool.create_tables("Customer_Ids")

    tool.drop_tables("Customer_Names")
    tool.create_tables("Customer_Names")

    tool.drop_tables("Orders")
    tool.create_tables("Orders")

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
