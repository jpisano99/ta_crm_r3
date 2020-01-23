from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Names, Orders, BookingsSchema
import my_app.tool_box as tool

def test_query():

    # tool.drop_tables("Customer_Ids")
    # tool.create_tables("Customer_Ids")
    #
    # tool.drop_tables("Customer_Names")
    # tool.create_tables("Customer_Names")
    #
    # tool.drop_tables("Orders")
    # tool.create_tables("Orders")
    #
    # tool.drop_tables("Web_Orders")
    # tool.create_tables("Web_Orders")


    cust_ids = Customer_Ids.query.all()

    cust_names = Customer_Names.query.all()


    for cust_id in cust_ids:
        these_names = cust_names.my_cust_id
        this_id = cust_id.end_customer_global_ultimate_id
        print(this_id,these_names)
        exit()
        print(this_id)
        cust_names = Customer_Names.query.filter_by(end_customer_global_ultimate_id=this_id)
        for cust_name in cust_names:
            print('\t',cust_name.erp_end_customer_name)
    return


def query_bookings():
    sql = "SELECT * FROM ta_adoption_db.bookings " \
          "WHERE end_customer_global_ultimate_id = '26768' " \
          "ORDER BY erp_sales_order_number ASC;"

    # FedEx 2636069
    # LA County 26768

    sql_results = db.engine.execute(sql)

    print()
    print('---------------------------------')
    prev_so_num = ''
    for row, x in enumerate(sql_results):
        curr_so_num = x.erp_sales_order_number

        if row == 0:
            print('Customer Name: ', x.erp_end_customer_name)

        if curr_so_num != prev_so_num:
            print('\tSO Num:', x.erp_sales_order_number)
            print('\t\t', row, x.product_id)
            prev_so_num = curr_so_num
        else:
            print('\t\t', row, x.product_id)

    return

def query_web_orders():
    sql = "SELECT * FROM ta_adoption_db.bookings " \
          "WHERE end_customer_global_ultimate_id = '26768' " \
          "ORDER BY web_order_id ASC;"

    # FedEx 2636069
    # LA County 26768

    sql_results = db.engine.execute(sql)

    print()
    print('---------------------------------')
    prev_so_num = ''
    for row, x in enumerate(sql_results):
        curr_so_num = x.web_order_id

        if row == 0:
            print('Customer Name: ', x.erp_end_customer_name)

        if curr_so_num != prev_so_num:
            print('\tWeb Order Num:', x.web_order_id)
            print('\t\t', row, x.product_id)
            prev_so_num = curr_so_num
        else:
            print('\t\t', row, x.product_id)

    return


if __name__ == "__main__" and __package__ is None:
    # query_bookings()
    # query_web_orders()
    test_query()
