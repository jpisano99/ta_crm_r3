import my_app.tool_box as tool
from my_app import db


def clean_up():
    tool.drop_tables("bookings")
    tool.drop_tables("bookings_deleted")

    tool.drop_tables("subscriptions")
    tool.drop_tables("subscriptions_deleted")

    tool.drop_tables("services")
    tool.drop_tables("telemetry")

    tool.drop_tables("subscription_ids")
    tool.drop_tables("web_orders")
    tool.drop_tables("sales_orders")

    tool.drop_tables("customer_aliases")
    tool.drop_tables("customer_ids")

    return


def archive_db():
    sql = "SELECT DISTINCT `date_added` FROM `archive_bookings_repo` ;"
    sql_results = db.engine.execute(sql)
    repo_date_list = []
    for r in sql_results:
        print('Found in Repo', r.date_added)
        repo_date_list.append(r.date_added)
    print('--------------------')

    if tool.table_exist('bookings'):
        sql = "SELECT DISTINCT `date_added` FROM `bookings` ;"
        sql_results = db.engine.execute(sql)

        for r in sql_results:
            print('Adding Date in Current Bookings', r.date_added)
            if r.date_added in repo_date_list:
                print('repo already has this update', r.date_added)
                print('Aborting')
                exit()

    # Merge Bookings
    sql = "INSERT INTO `archive_bookings_repo` "\
            "(fiscal_year, " \
            "fiscal_quarter_id, " \
            "fiscal_period_id, " \
            "sales_level_1, " \
            "sales_level_2, " \
            "sales_level_3, " \
            "sales_level_4, " \
            "sales_level_5, " \
            "sales_level_6, " \
            "sales_agent_name, "\
            "email_id, "\
            "erp_sales_order_number, " \
            "web_order_id, " \
            "erp_end_customer_name, " \
            "end_customer_global_ultimate_name, " \
            "end_customer_global_ultimate_id, " \
            "tms_level_2_sales_allocated, " \
            "product_family, " \
            "bundle_product_id, " \
            "product_id, " \
            "tms_sales_allocated_product_bookings_net, " \
            "tms_sales_allocated_service_bookings_net, " \
            "hash_value, " \
            "date_added) " \
        " SELECT " \
            "fiscal_year, " \
            "fiscal_quarter_id, " \
            "fiscal_period_id, " \
            "sales_level_1, " \
            "sales_level_2, " \
            "sales_level_3, " \
            "sales_level_4, " \
            "sales_level_5, " \
            "sales_level_6, " \
            "sales_agent_name, " \
            "email_id, " \
            "erp_sales_order_number, " \
            "web_order_id, " \
            "erp_end_customer_name, " \
            "end_customer_global_ultimate_name, " \
            "end_customer_global_ultimate_id, " \
            "tms_level_2_sales_allocated, " \
            "product_family, " \
            "bundle_product_id, " \
            "product_id, " \
            "tms_sales_allocated_product_bookings_net, " \
            "tms_sales_allocated_service_bookings_net, " \
            "hash_value, " \
            "date_added " \
        "FROM bookings;"

    # Merge Subscriptions
    sql = "INSERT INTO `archive_subscriptions_repo` "\
        "(bill_to_customer, " \
        "reseller, " \
        "end_customer, " \
        "offer_name, " \
        "consumption_health, " \
        "over_consumed_tf_groups, " \
        "next_true_forward, " \
        "subscription_id, " \
        "status, " \
        "start_date, " \
        "initial_term, " \
        "renewal_dat, " \
        "currency, " \
        "monthly_charge, " \
        "auto_renewal_term, " \
        "billing_model, " \
        "purchase_order_number, " \
        "weborderid, " \
        "site_url, " \
        "customer_success_manager, " \
        "partner_success_manager, " \
        "sales_owner, " \
        "customer_success_manager_email, " \
        "partner_success_manager_email, " \
        "sales_owner_email, " \
        "account_type, " \
        "days_until_renewal, " \
        "recent_milestone_date, " \
        "tf_order_status, " \
        "tf_order_date, " \
        "hash_value, " \
        "date_added) " \
    " SELECT " \
        "bill_to_customer, " \
        "reseller, " \
        "end_customer, " \
        "offer_name, " \
        "consumption_health, " \
        "over_consumed_tf_groups, " \
        "next_true_forward, " \
        "subscription_id, " \
        "status, " \
        "start_date, " \
        "initial_term, " \
        "renewal_dat, " \
        "currency, " \
        "monthly_charge, " \
        "auto_renewal_term, " \
        "billing_model, " \
        "purchase_order_number, " \
        "weborderid, " \
        "site_url, " \
        "customer_success_manager, " \
        "partner_success_manager, " \
        "sales_owner, " \
        "customer_success_manager_email, " \
        "partner_success_manager_email, " \
        "sales_owner_email, " \
        "account_type, " \
        "days_until_renewal, " \
        "recent_milestone_date, " \
        "tf_order_status, " \
        "tf_order_date, " \
        "hash_value, " \
        "date_added "
    "FROM subscriptions;"





    print(sql)
    sql_results = db.engine.execute(sql)
    print("Loaded Bookings:", sql_results.rowcount, ' rows')
    exit()

    sql = "INSERT INTO `archive_services_repo` SELECT * FROM services;"
    sql_results = db.engine.execute(sql)
    print("Loaded Services:", sql_results.rowcount, ' rows')

    sql = "INSERT INTO `archive_subscriptions_repo` SELECT * FROM subscriptions;"
    sql_results = db.engine.execute(sql)
    print("Loaded Subscriptions:", sql_results.rowcount, ' rows')

    sql = "INSERT INTO archive_telemetry_repo SELECT * FROM telemetry;"
    sql_results = db.engine.execute(sql)
    print("Loaded Telemetry:", sql_results.rowcount, ' rows')

    return


if __name__ == "__main__" and __package__ is None:
    archive_db()
    # clean_up()
    exit()
