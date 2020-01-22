from my_app import db


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
    query_web_orders()
