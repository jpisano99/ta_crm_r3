import my_app.tool_box as tool
from my_app import db


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

    #
    # Merge Bookings
    #
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
    sql_results = db.engine.execute(sql)
    print("Loaded Bookings:", sql_results.rowcount, ' rows')

    #
    # Merge Subscriptions
    #
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
        "renewal_date, " \
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
    "SELECT " \
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
        "renewal_date, " \
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
        "date_added " \
    "FROM subscriptions;"
    sql_results = db.engine.execute(sql)
    print("Loaded Subscriptions:", sql_results.rowcount, ' rows')

    #
    # Merge Services
    #
    sql = "INSERT INTO `archive_services_repo` " \
            "(pid, " \
            "delivery_manager, " \
            "end_customer, " \
            "project_department_name, " \
            "op_pm, " \
            "color_indicator, " \
            "delivery_pm, " \
            "tracking_status, " \
            "tracking_sub_status, " \
            "comments, " \
            "dmc_updates, " \
            "dmc_act_fcst_end, " \
            "op_forecast, " \
            "cost_index, " \
            "sku, " \
            "project_name, " \
            "unit, " \
            "region, " \
            "wm_in_op, " \
            "so, " \
            "as_approved_cost_budget, " \
            "as_approved_revenue_budget, " \
            "actual_total_costs, " \
            "actual_revenue, " \
            "status, " \
            "project_class, " \
            "project_scheduled_start_date, " \
            "scheduled_end_date, " \
            "project_creation_date, " \
            "project_closed_date, " \
            "traffic_lights_account_team, " \
            "tracking_responsible, " \
            "hash_value, " \
            "date_added) " \
        "SELECT " \
            "pid, " \
            "delivery_manager, " \
            "end_customer, " \
            "project_department_name, " \
            "op_pm, " \
            "color_indicator, " \
            "delivery_pm, " \
            "tracking_status, " \
            "tracking_sub_status, " \
            "comments, " \
            "dmc_updates, " \
            "dmc_act_fcst_end, " \
            "op_forecast, " \
            "cost_index, " \
            "sku, " \
            "project_name, " \
            "unit, " \
            "region, " \
            "wm_in_op, " \
            "so, " \
            "as_approved_cost_budget, " \
            "as_approved_revenue_budget, " \
            "actual_total_costs, " \
            "actual_revenue, " \
            "status, " \
            "project_class, " \
            "project_scheduled_start_date, " \
            "scheduled_end_date, " \
            "project_creation_date, " \
            "project_closed_date, " \
            "traffic_lights_account_team, " \
            "tracking_responsible, " \
            "hash_value, " \
            "date_added " \
        "FROM services;"
    sql_results = db.engine.execute(sql)
    print("Loaded Services:", sql_results.rowcount, ' rows')

    #
    # Merge Telemetry
    #
    sql = "INSERT INTO archive_telemetry_repo " \
            "(type, " \
            "erp_cust_name, " \
            "erp_cust_id, " \
            "so_number, " \
            "sub_id, " \
            "start_date, " \
            "name, " \
            "vrf, " \
            "licensed, " \
            "installed, " \
            "inactive, " \
            "autoupg, " \
            "windows, " \
            "linux, " \
            "aix, " \
            "lightwt, " \
            "legacy, " \
            "deepvis, " \
            "enforce, " \
            "enforce_enabled, " \
            "pid_enabled, " \
            "forensics_enabled, " \
            "inventory, " \
            "anyconnect, " \
            "anyproxy, " \
            "erspan, " \
            "f5, " \
            "netflow, " \
            "netscaler, " \
            "others, " \
            "hash_value, " \
            "date_added) " \
        "SELECT " \
            "type, " \
            "erp_cust_name, " \
            "erp_cust_id, " \
            "so_number, " \
            "sub_id, " \
            "start_date, " \
            "name, " \
            "vrf, " \
            "licensed, " \
            "installed, " \
            "inactive, " \
            "autoupg, " \
            "windows, " \
            "linux, " \
            "aix, " \
            "lightwt, " \
            "legacy, " \
            "deepvis, " \
            "enforce, " \
            "enforce_enabled, " \
            "pid_enabled, " \
            "forensics_enabled, " \
            "inventory, " \
            "anyconnect, " \
            "anyproxy, " \
            "erspan, " \
            "f5, " \
            "netflow, " \
            "netscaler, " \
            "others, " \
            "hash_value, " \
            "date_added " \
        "FROM telemetry;"
    sql_results = db.engine.execute(sql)
    print("Loaded Telemetry:", sql_results.rowcount, ' rows')

    tool.create_row_hash('Archive_Telemetry_Repo')
    tool.create_row_hash('Archive_Bookings_Repo')
    tool.create_row_hash('Archive_Subscriptions_Repo')
    tool.create_row_hash('Archive_Services_Repo')

    return


if __name__ == "__main__" and __package__ is None:
    archive_db()
    exit()
