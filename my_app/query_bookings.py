from my_app import db


def query_bookings():
    sql = "SELECT * FROM ta_adoption_db.bookings " \
          "WHERE end_customer_global_ultimate_id = '2636069' " \
          "ORDER BY erp_sales_order_number ASC;"

    # FedEx 2636069
    # LA County 26768

    sql_results = db.engine.execute(sql)
    print(sql_results)
    for x in sql_results:
        print(x.erp_end_customer_name, x.product_id)
    return


if __name__ == "__main__" and __package__ is None:
    query_bookings()
