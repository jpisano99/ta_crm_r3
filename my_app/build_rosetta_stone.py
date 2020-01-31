import my_app.tool_box as tool
from my_app.settings import app_cfg
from fuzzywuzzy import fuzz
import xlrd
from datetime import datetime
import time

#
# Get All Customer names and VRFs from Ravi's Sheet
#
saas_name_dict={}
rs_wb, rs_ws = tool.open_wb(app_cfg['XLS_ROSETTA'])
print('SaaS Platform Customers', rs_ws.nrows)
for row in range(1, rs_ws.nrows):
    saas_platform_name = rs_ws.cell_value(row, 0)
    saas_vrf_number = str(int(rs_ws.cell_value(row, 1)))
    saas_num_of_licenses = str(int(rs_ws.cell_value(row, 3)))
    saas_actual_sensors_installed = str(int(rs_ws.cell_value(row, 4)))
    saas_inactive_agents = str(int(rs_ws.cell_value(row, 5)))

    saas_name_dict[saas_platform_name] = [saas_vrf_number, saas_num_of_licenses,
                                          saas_actual_sensors_installed, saas_inactive_agents]

#
# Get ALL subscriptions and Customer Names from Subscription Report
#
sub_dict={}
sub_wb, sub_ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
print(sub_ws.nrows)
for row in range(1, sub_ws.nrows):
    sub_cust_name = sub_ws.cell_value(row, 2)
    sub_web_order = str(sub_ws.cell_value(row, 17))
    sub_renewal_date = sub_ws.cell_value(row, 11)

    if sub_ws.cell_type(row, 11) == xlrd.XL_CELL_DATE:
        sub_renewal_date = datetime(*xlrd.xldate_as_tuple(sub_renewal_date, sub_wb.datemode))
        # print(sub_renewal_date, type(sub_renewal_date))

    sub_dict[sub_web_order] = [sub_cust_name, sub_renewal_date]
print(sub_dict)


#
# Get ALL items from Nirali SAAS tracking sheet
#
nirali_dict = {}
nirali_wb, nirali_ws = tool.open_wb(app_cfg['XLS_SAAS_NAMES'])
print(nirali_ws.nrows)
for row in range(1, nirali_ws.nrows):
    nirali_name = nirali_ws.cell_value(row, 1)
    nirali_so_number = nirali_ws.cell_value(row, 2)
    nirali_start_date = nirali_ws.cell_value(row, 3)

    if nirali_ws.cell_type(row, 3) == xlrd.XL_CELL_DATE:
        nirali_start_date = datetime(*xlrd.xldate_as_tuple(nirali_start_date, nirali_wb.datemode))
        print(nirali_start_date, type(nirali_start_date))

    if type(nirali_so_number) is float:
        tmp_int = int(nirali_so_number)
        nirali_so_number = str(tmp_int)


    nirali_dict[nirali_name] = [nirali_so_number, nirali_start_date]

#
# Get ALL Unique customer Names and ID's from Bookings data
#
cust_dict = {}
cust_wb, cust_ws = tool.open_wb(app_cfg['XLS_UNIQUE_CUSTOMERS'])
print(cust_ws.nrows)
for row in range(1, cust_ws.nrows):
    cust_name = cust_ws.cell_value(row, 0)
    cust_id = str(cust_ws.cell_value(row, 1))
    print(cust_name, cust_id)
    # print(cust_name)
    cust_dict[cust_name] = cust_id


print()
print('*********************************')
#
# Perform a fuzzy match search against all customer aliases in Nirali's Sheet vs Ravi's Platform Sheet
#
my_list = []
my_list.append(['ravi_name', 'ravi_vrf_number', 'num_of_lic', 'sensors installed','inactive agents',
                'best_match_nirali_cust_name', 'best_match_nirali_so_num', 'match_score',
               'nirali Req Start Date', 'subscription renewal date', 'subscription_cust_name',
                'subscription_order_num', 'customer_id', 'PSS', 'TSA', 'CX Engineer','CX Status'])
for saas_platform_name, saas_info in saas_name_dict.items():
    saas_vrf_number = saas_info[0]
    saas_num_of_licenses = saas_info[1]
    saas_actual_sensors_installed = saas_info[2]
    saas_inactive_agents = saas_info[3]

    best_match = 0
    possible_cust = ''
    possible_so = ''
    req_start_date = ''
    sub_renewal_date = ''

    for nirali_name, nirali_info in nirali_dict.items():
        # match_ratio = fuzz.ratio(saas_platform_name, nirali_name)
        match_ratio = fuzz.partial_ratio(saas_platform_name, nirali_name)
        if match_ratio > best_match:
            possible_cust = nirali_name
            possible_so = nirali_info[0]
            req_start_date = nirali_info[1]
            best_match = match_ratio

    if possible_cust in cust_dict:
        cust_id= cust_dict[possible_cust]
    else:
        cust_id = 'ID NOT Found in Bookings Sheet'

    if possible_so in sub_dict:
        sub_cust_name = sub_dict[possible_so][0]
        sub_renewal_date = sub_dict[possible_so][1]
    else:
        sub_cust_name = 'SO NOT Found in Subscription Sheet'

    my_list.append([saas_platform_name, saas_vrf_number, saas_num_of_licenses, saas_actual_sensors_installed, saas_inactive_agents,
                    possible_cust, possible_so, best_match, req_start_date,
                    sub_renewal_date, sub_cust_name, possible_so, cust_id, 'TBD','TBD','TBD','TBD'])
    # print(saas_platform_name, possible_cust, best_match)
    # time.sleep(.5)


tool.push_list_to_xls(my_list, 'tmp_rosetta_stone.xlsx')

