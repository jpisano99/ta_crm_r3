import my_app.tool_box as tool
from my_app.models import Bookings
from my_app import db
from my_app.table_stats import table_stats
import time

#
# Build a Team Dict of PSS/TSA
#
team_dict = tool.build_coverage_dict()

# Create the Start and End Dates / Tables
start_date = "2020-02-03"
start_tbl = "tmp_booking_" + start_date.replace('-', '_')
end_date = "2020-03-11"
end_tbl = "tmp_booking_" + end_date.replace('-', '_')
#
# # Re-Hash the Bookings Repo
# tool.create_row_hash('Archive_Bookings_Repo')

# Start Table
sql = "DROP TABLE " + start_tbl + ";"
db.engine.execute(sql)
sql = "CREATE TABLE " + start_tbl + " LIKE archive_bookings_repo;"
db.engine.execute(sql)
sql = "INSERT INTO " + start_tbl + " SELECT * " +\
        "FROM archive_bookings_repo " +\
        "WHERE date_added = '" + start_date + "' ;"
db.engine.execute(sql)
sql = "DELETE FROM " + start_tbl + " WHERE product_id NOT LIKE 'AS%';"
db.engine.execute(sql)

# End Table
sql = "DROP TABLE " + end_tbl + ";"
db.engine.execute(sql)
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
                         'SO Number', 'Web Order ID', 'Date Added', 'Rec ID']]

# Loop over the most recent Bookings records with AS orders
for r in ending_rows:

    # We found a new AS Booking Lets capture it
    if r.hash_value not in base_dict:
        # Go get a PSS/TSA and Sales Levels
        sales_levels = r.sales_level_1 + ',' + r.sales_level_2 + ',' + r.sales_level_3 + ',' + r.sales_level_4 + ',' + \
            r.sales_level_5 + ',' + r.sales_level_6
        sales_team = tool.find_team(team_dict, sales_levels)
        pss = sales_team[0]
        tsa = sales_team[1]

        print('Found New', r.erp_end_customer_name, r.product_id, pss, tsa, r.sales_agent_name, r.erp_sales_order_number, r.web_order_id)
        new_as_list.append([r.erp_end_customer_name, r.product_id, pss, tsa, r.sales_agent_name,
                            r.erp_sales_order_number, r.web_order_id, r.date_added])

# Push the list to excel
tool.push_list_to_xls(new_as_list, 'new_AS.xlsx',)
exit()


# Go to the Repo and get all Customer Aliases/Customer Global IDs

# Find the most recent snapshot in the repo
most_recent_update = table_stats({'bookings': 'archive_bookings_repo'})
date_added = most_recent_update[0][0].strftime("%Y-%m-%d")
print("Reporting on most recent snapshot", most_recent_update[0][0])


sql = "SELECT distinct erp_end_customer_name, end_customer_global_ultimate_id " + \
        "FROM archive_bookings_repo " +\
        "WHERE date_added = '" + date_added + "';"
customer_aliases = db.engine.execute(sql)
print("Processing ", customer_aliases.rowcount, " customers")

#
# Define Header Row
#
subscription_list = [['Customer Name', 'Customer ID', 'PSS', 'TSA', 'Account Mgr',
                         'Sales_Lev_1', 'Sales_Lev_2', 'Sales_Lev_3',
                         'Sales_Lev_4', 'Sales_Lev_5', 'Sales_Lev_6']]

sales_levels = ''
for r in customer_aliases:
    # Go get all sales levels and agents
    this_cust_info = Bookings.query.filter_by(erp_end_customer_name=r.erp_end_customer_name).all()

    # Search for a valid set of sales levels
    for x in this_cust_info:
        sales_levels = x.sales_level_1 + ',' + x.sales_level_2 + ',' + x.sales_level_3 + ',' + x.sales_level_4 + ',' + \
              x.sales_level_5 + ',' + x.sales_level_6

        # Skip any levels that has MISC in it
        if sales_levels.find('MISC') != -1:
            continue
        else:
            break

    # Go get a PSS/TSA
    sales_team = tool.find_team(team_dict, sales_levels)
    pss = sales_team[0]
    tsa = sales_team[1]

    customer_contact_list.append([
                r.erp_end_customer_name, r.end_customer_global_ultimate_id,
                pss, tsa,
                x.sales_agent_name,
                x.sales_level_1, x.sales_level_2, x.sales_level_3, x.sales_level_4, x.sales_level_5, x.sales_level_6
                ])

tool.push_list_to_xls(customer_contact_list, 'simple_customer.xlsx')

exit()



