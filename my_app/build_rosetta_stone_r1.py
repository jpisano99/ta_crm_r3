import my_app.tool_box as tool
from my_app.settings import app_cfg
import datetime
from my_app.models import Bookings, Telemetry, Subscriptions, Customer_Ids, Services
import time
from my_app import db


def sub_analysis(cust_name):
    sql = 'CREATE TABLE ta_adoption_db.archive_services_repo LIKE ta_adoption_db.services;'
    sql = "SELECT * FROM ta_adoption_db.archive_subscriptions_repo " + \
          "WHERE end_customer = '" + cust_name + "'"
    sub_recs = db.engine.execute(sql)
    print("Customer Subscriptions for:", cust_name, sub_recs.rowcount)

    #
    # Gather Subscription record info and sort it
    #
    sub_list = []
    for sub_rec in sub_recs:
        sub_id = sub_rec.subscription_id
        sub_offer_name = sub_rec.offer_name
        sub_start_date = sub_rec.start_date
        sub_term = int(float(sub_rec.initial_term))
        sub_status = sub_rec.status
        sub_so_num = sub_rec.weborderid
        sub_renewal_date = sub_rec.renewal_date
        sub_date_added = sub_rec.date_added

        sub_info = [sub_id, sub_offer_name, sub_start_date, sub_term, sub_status,
                    sub_so_num, sub_renewal_date, sub_date_added]
        sub_list.append(sub_info)

    #
    # Create a reverse 2 level sorted index list of (SubId, Date Added to repo)
    #
    sub_list.sort(key=lambda x: (x[0], x[7]), reverse=True)

    print('---------------------')
    for x in sub_list:
        print(x[0],x[5], x[4], x[7])

    web_order_dict = {}

    for x in sub_list:
        sub_id = x[0]
        web_order_id = x[5]
        web_order_dict[web_order_id] = sub_id

    print(web_order_dict)

    return


def build_rosetta_stone():
    #
    # Build a Team Dict to figure out PSS/TSA
    #
    team_dict = tool.build_coverage_dict()

    #
    # Define Header Row
    #
    rosetta_list = []
    rosetta_list.append(['Customer Name', 'Num Of Licenses ', '% of Sensors Installed', '% of Active Sensors',
                'Adoption Factor' + '\n' + '(% Active Sensors : % of Subscription Consumed)'
                + '\n' + ' as of ',
                'Subscription Term', 'Subscription Status', 'Days to Renew',
                'PSS', 'TSA', 'AM', 'Sales Lv 1', 'Sales Lv 2',
                'Telemetry Name', 'Telemetry VRF', 'Sensors Installed', 'Active Agents',
                'Sub Type', 'Sub Order Num','Sub ID', 'Req Start Date', 'Renewal Date',
                'CX PID', 'CX Delivery Manager', 'Customer ID'])

    #
    # Main Loop over all Customer IDs
    #
    customer_ids = Customer_Ids.query.all()
    print('There are', len(customer_ids), 'unique Customer IDs')
    print()

    for my_id_info in customer_ids:
        customer_id = my_id_info.customer_id
        if customer_id == 'INVALID':
            continue

        # Loop over each Alias we found
        for alias_num, my_alias in enumerate(my_id_info.customer_aliases):
            customer_name = my_alias.customer_alias

            #
            # Perform All Queries for this Customer Alias
            #
            sql = "SELECT * FROM ta_adoption_db.subscriptions where end_customer = " + '"' + \
                   customer_name + '"'

            # sql = "SELECT * FROM ta_adoption_db.subscriptions where end_customer = " + '"' + \
            #        customer_name + '"' + " and status = 'ACTIVE'"
            my_subs = db.engine.execute(sql)
            my_services = Services.query.filter_by(end_customer=customer_name).all()
            my_telemetry = Telemetry.query.filter_by(erp_cust_name=customer_name).all()
            my_bookings = Bookings.query.filter_by(erp_end_customer_name=customer_name).all()

            #
            # Get where this was sold and by who
            #
            cust_sales_lev_1 = my_bookings[0].sales_level_1
            cust_sales_lev_2 = my_bookings[0].sales_level_2
            cust_sales_lev_3 = my_bookings[0].sales_level_3
            cust_sales_lev_4 = my_bookings[0].sales_level_4
            cust_sales_lev_5 = my_bookings[0].sales_level_5
            cust_sales_lev_6 = my_bookings[0].sales_level_6
            sales_level = cust_sales_lev_1 + ',' + cust_sales_lev_2 + ',' + cust_sales_lev_3 + ',' + \
                cust_sales_lev_4 + ',' + cust_sales_lev_5 + ',' + cust_sales_lev_6
            sales_team = tool.find_team(team_dict, sales_level)
            pss = sales_team[0]
            tsa = sales_team[1]
            cust_acct_mgr = my_bookings[0].sales_agent_name

            #
            # Subscription Analysis
            # Loop over each Subscription for this Customer_Name / Customer_ID
            #
            rosetta_row = []
            for my_rec in my_subs:
                #
                # Gather Subscription record info
                #
                sub_id = my_rec.subscription_id
                sub_offer_name = my_rec.offer_name
                sub_start_date = my_rec.start_date
                sub_term = int(float(my_rec.initial_term))
                sub_status = my_rec.status
                sub_so_num = my_rec.weborderid
                sub_renewal_date = my_rec.renewal_date

                #
                # Check Telemetry Table and SaaS data
                #
                telemetry_name = ''
                telemetry_vrf_number = ''
                telemetry_num_of_licenses = 0
                telemetry_actual_sensors_installed = 0
                telemetry_inactive_agents = 0
                telemetry_so = ''
                telemetry_start_date = ''

                # Calculated Fields for Telemetry
                saas_flag = False
                telemetry_active_agents = 0
                pct_installed = 0
                pct_active = 0

                if len(my_telemetry) == 1:
                    # print("\tNumber of Telemetry sessions", len(my_telemetry), my_telemetry[0].name)
                    saas_flag = True
                    # Telemetry Data
                    telemetry_name = my_telemetry[0].name
                    telemetry_vrf_number = my_telemetry[0].vrf
                    telemetry_num_of_licenses = my_telemetry[0].licensed
                    telemetry_actual_sensors_installed = my_telemetry[0].installed
                    telemetry_inactive_agents = my_telemetry[0].inactive
                    telemetry_so = my_telemetry[0].so_number
                    telemetry_start_date = my_telemetry[0].start_date
                elif len(my_telemetry) > 1:
                    print("\tERROR: More than one Telemetry session found !", len(my_telemetry))
                    exit()

                #
                # Make the Calculations for Telemetry
                #
                if int(telemetry_num_of_licenses) != 0:
                    telemetry_active_agents = telemetry_actual_sensors_installed - telemetry_inactive_agents
                    pct_installed = telemetry_actual_sensors_installed / telemetry_num_of_licenses
                    pct_active = telemetry_active_agents / telemetry_num_of_licenses

                # Fields to grab from other places
                as_pid = '1234'
                as_dm = 'jim'

                # Calc Adoption Factor and Days to Renewal
                days_to_renew = ''
                now = datetime.datetime.now()
                adoption_factor = 0
                if isinstance(telemetry_start_date, datetime.datetime) and \
                   isinstance(sub_renewal_date, datetime.datetime):
                    days_to_renew = (sub_renewal_date - now).days

                    sub_days_total = int(sub_term) * 30
                    sub_days_active = sub_days_total - days_to_renew

                    pct_sub_expired = sub_days_active / sub_days_total
                    adoption_factor = (pct_active / pct_sub_expired)
                    adoption_factor = str(round(adoption_factor, 2)) + '_non$_'

                #
                # All the math is done so now
                # Format these all to push_list_to_xls.py
                #
                telemetry_num_of_licenses = int(telemetry_num_of_licenses)
                telemetry_actual_sensors_installed = int(telemetry_actual_sensors_installed)
                telemetry_active_agents = int(telemetry_active_agents)
                pct_installed = str(round(pct_installed, 1)) + '_%_'
                pct_active = str(round(pct_active, 1)) + '_%_'

                # Push out a row
                rosetta_row = [customer_name, telemetry_num_of_licenses, pct_installed, pct_active,
                                adoption_factor,
                                sub_term, sub_status, days_to_renew,
                                pss, tsa, cust_acct_mgr, cust_sales_lev_1, cust_sales_lev_2,
                                telemetry_name, telemetry_vrf_number,
                                telemetry_actual_sensors_installed, telemetry_active_agents,
                                sub_offer_name, sub_so_num, 'SubID',telemetry_start_date, sub_renewal_date,
                                as_pid, as_dm, customer_id]

                rosetta_list.append(rosetta_row)

    tool.push_list_to_xls(rosetta_list, 'stan.xlsx')

    print('done')
    my_telemetry = Telemetry.query.all()
    a_list = [['cust','vrf','order']]
    for r in my_telemetry:
        telemetry_cust = r.erp_cust_name
        vrf = r.vrf
        order = r.so_number
        found_it = False
        for my_row in rosetta_list:
            if my_row[0] == telemetry_cust:
                found_it = True
                # print('found',telemetry_cust)
                break
        if found_it == False:
            a_list.append([telemetry_cust, vrf, order])
            print('MISSING', telemetry_cust, vrf, order)
    tool.push_list_to_xls(a_list, 'blanche.xlsx')

    return


if __name__ == "__main__" and __package__ is None:
    build_rosetta_stone()
    # sub_analysis('CHOCTAW CASINO ADMINISTRATION')
    print()
    # sub_analysis('Clarivate Analytics')
    # sub_analysis('WHATABURGER INC')
