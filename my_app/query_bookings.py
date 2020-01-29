from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Aliases, Sales_Orders, BookingsSchema
import my_app.tool_box as tool
import time


def test_query():
    cust_ids = Customer_Ids.query.all()
    bookings = Bookings.query.all()

    for cust_id in cust_ids:
        these_alaises = cust_id.customer_aliases
        these_orders = cust_id.customer_so_numbers
        these_web_orders = cust_id.customer_web_order_ids

        this_id = cust_id.customer_id
        print()
        print('Customer ID', this_id, these_alaises)
        print('\tCustomer Aliases')
        for a_name in these_alaises:
            print('\t', a_name.customer_alias)

        print('\t\tSales Orders ')
        for a_order in these_orders:

            print('\t\t', a_order.so_number, a_order.my_customer_id.customer_id)
            stan = Bookings.query.filter_by(erp_sales_order_number=a_order.so_number).all()
            for k in stan:
                print('\t\t\t', k.erp_sales_order_number,k.bundle_product_id)
            #exit()

        print('\t\tWeb Orders ')
        for a_web_order in these_web_orders:
            print('\t\t', a_web_order.web_order_id, a_web_order.my_customer_id.customer_id)

        time.sleep(.5)
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
