import my_app.tool_box as tool
from my_app.models import Bookings
from my_app import db
from my_app.table_stats import table_stats


def report_customer_contacts():
    #
    # Build a Team Dict of PSS/TSA
    #
    team_dict = tool.build_coverage_dict()

    #
    # customer_aliases = Customer_Aliases.query.all()
    # print(customer_aliases)
    # customer_names = Bookings.query.all()

    # Go to the Repo and get all Customer Aliases/Customer Global IDs

    # Find the most recent snapshot in the repo
    most_recent_update = table_stats({'bookings': 'archive_bookings_repo'})
    date_added = most_recent_update[0][0].strftime("%Y-%m-%d")
    print("Reporting on most recent snapshot", most_recent_update[0][0])

    sql = "SELECT distinct erp_end_customer_name, end_customer_global_ultimate_name, end_customer_global_ultimate_id " + \
        "FROM archive_bookings_repo " +\
        "WHERE date_added = '" + date_added + "';"
    customer_aliases = db.engine.execute(sql)
    print("Processing ", customer_aliases.rowcount, " customers")

    #
    # Define Header Row
    #
    customer_contact_list = [['Customer Name', 'Ultimate Customer Name', 'Customer ID', 'PSS', 'TSA', 'Account Mgr',
                              'Sales_Lev_1', 'Sales_Lev_2', 'Sales_Lev_3',
                              'Sales_Lev_4', 'Sales_Lev_5', 'Sales_Lev_6']]

    sales_levels = ''
    for r in customer_aliases:
        # Go get all sales levels and agents
        this_cust_info = Bookings.query.filter_by(erp_end_customer_name=r.erp_end_customer_name).all()
        x = ''

        # Search for a valid set of sales levels
        for x in this_cust_info:
            sales_levels = x.sales_level_1 + ',' + x.sales_level_2 + ',' + x.sales_level_3 + ',' + \
                           x.sales_level_4 + ',' + x.sales_level_5 + ',' + x.sales_level_6

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
                    r.erp_end_customer_name, r.end_customer_global_ultimate_name, r.end_customer_global_ultimate_id,
                    pss, tsa,
                    x.sales_agent_name,
                    x.sales_level_1, x.sales_level_2, x.sales_level_3, x.sales_level_4,
                    x.sales_level_5, x.sales_level_6
                    ])

    tool.push_list_to_xls(customer_contact_list, 'tmp_simple_customer_' + date_added.replace('-', '_') + '.xlsx')

    return


if __name__ == "__main__" and __package__ is None:
    report_customer_contacts()
    exit()



