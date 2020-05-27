import my_app.tool_box as tool
from my_app import db


def report_new_as_bookings():
    #
    # Build a Team Dict of PSS/TSA
    #
    team_dict = tool.build_coverage_dict()

    # Create the Start and End Dates / Tables
    start_date = "2020-03-30"
    start_tbl = "tmp_booking_" + start_date.replace('-', '_')
    end_date = "2020-05-27"
    end_tbl = "tmp_booking_" + end_date.replace('-', '_')

    #
    # Re-Hash the Bookings Repo
    #
    # print("Hashing Bookings Repo")
    # tool.create_row_hash('Archive_Bookings_Repo')

    # Start Table
    # sql = "DROP TABLE " + start_tbl + ";"
    # db.engine.execute(sql)
    sql = "CREATE TABLE " + start_tbl + " LIKE archive_bookings_repo;"
    db.engine.execute(sql)
    sql = "INSERT INTO " + start_tbl + " SELECT * " +\
        "FROM archive_bookings_repo " +\
        "WHERE date_added = '" + start_date + "' ;"
    db.engine.execute(sql)
    sql = "DELETE FROM " + start_tbl + " WHERE product_id NOT LIKE 'AS%';"
    db.engine.execute(sql)

    # End Table
    # sql = "DROP TABLE " + end_tbl + ";"
    # db.engine.execute(sql)
    sql = "CREATE TABLE " + end_tbl + " LIKE archive_bookings_repo;"
    db.engine.execute(sql)
    sql = "INSERT INTO " + end_tbl + " SELECT * " +\
        "FROM archive_bookings_repo " +\
        "WHERE date_added = '" + end_date + "' ;"
    db.engine.execute(sql)
    sql = "DELETE FROM " + end_tbl + " WHERE product_id NOT LIKE 'AS%';"
    db.engine.execute(sql)

    # Compare the two
    sql = "SELECT * FROM " + start_tbl + ";"
    starting_rows = db.engine.execute(sql)
    base_dict = {}
    for r in starting_rows:
        base_dict[r.hash_value] = r.id

    sql = "SELECT * FROM " + end_tbl + ";"
    ending_rows = db.engine.execute(sql)

    #
    # Define Header Row
    #
    new_as_list = [['Customer Name', 'Product ID', 'PSS', 'TSA', 'Account Mgr',
                    'SO Number', 'Web Order ID', 'Date Added', 'Svc Revenue', 'Prod Revenue']]

    # Loop over the most recent Bookings records with AS orders
    for r in ending_rows:

        # We found a new AS Booking Lets capture it
        if r.hash_value not in base_dict:
            # Go get a PSS/TSA and Sales Levels
            sales_levels = r.sales_level_1 + ',' + r.sales_level_2 + ',' + r.sales_level_3 + ',' + \
                           r.sales_level_4 + ',' + r.sales_level_5 + ',' + r.sales_level_6
            sales_team = tool.find_team(team_dict, sales_levels)
            pss = sales_team[0]
            tsa = sales_team[1]

            print('Found New', r.erp_end_customer_name, r.product_id, pss, tsa, r.sales_agent_name,
                  r.erp_sales_order_number, r.web_order_id)

            new_as_list.append([r.erp_end_customer_name, r.product_id, pss, tsa, r.sales_agent_name,
                                r.erp_sales_order_number, r.web_order_id, r.date_added,
                                r.tms_sales_allocated_service_bookings_net,
                                r.tms_sales_allocated_product_bookings_net])

    # Push the list to excel
    tool.push_list_to_xls(new_as_list, 'tmp_new_AS_Bookings as of ' + end_date.replace('-', '_') + '.xlsx')
    return


if __name__ == "__main__" and __package__ is None:
    report_new_as_bookings()
    exit()
