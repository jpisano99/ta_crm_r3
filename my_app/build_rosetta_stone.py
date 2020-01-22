import my_app.tool_box as tool
from my_app.settings import app_cfg
from fuzzywuzzy import fuzz
import xlrd
from datetime import datetime
import time


saas_name_dict={}
rs_wb, rs_ws = tool.open_wb(app_cfg['XLS_ROSETTA'])
print(rs_ws.nrows)
for row in range(1, rs_ws.nrows):
    saas_platform_name = rs_ws.cell_value(row, 0)
    saas_vrf_number = str(int(rs_ws.cell_value(row, 1)))
    print(saas_platform_name, saas_vrf_number)
    saas_name_dict[saas_platform_name] = saas_vrf_number

sub_dict={}
sub_wb, sub_ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
print(sub_ws.nrows)
for row in range(1, sub_ws.nrows):
    sub_cust_name = sub_ws.cell_value(row, 2)
    sub_web_order = str(sub_ws.cell_value(row, 17))
    print(sub_cust_name, sub_web_order)
    sub_dict[sub_web_order] = sub_cust_name
print(sub_dict)

nirali_dict = {}
nirali_wb, nirali_ws = tool.open_wb(app_cfg['XLS_SAAS_NAMES'])
print(nirali_ws.nrows)
for row in range(1, nirali_ws.nrows):
    nirali_name = nirali_ws.cell_value(row, 1)
    nirali_so_number = str(nirali_ws.cell_value(row, 2))
    # print(nirali_name, nirali_so_number)
    print(nirali_name)
    nirali_dict[nirali_name] = nirali_so_number


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
# do a fuzzy match search against all customer aliases
my_list = []
my_list.append(['ravi_name', 'ravi_vrf_number', 'possible_nirali_cust_name', 'possible_nirali_so_num', 'match_score',
               'subscription_cust_name', 'subscription_order_num', 'customer_id'])
for saas_platform_name, saas_vrf_number in saas_name_dict.items():

    best_match = 0
    possible_cust = ''
    possible_so = ''

    for nirali_name, nirali_so_number in nirali_dict.items():
        # match_ratio = fuzz.ratio(saas_platform_name, nirali_name)
        match_ratio = fuzz.partial_ratio(saas_platform_name, nirali_name)
        if match_ratio > best_match:
            possible_cust = nirali_name
            possible_so = nirali_so_number
            best_match = match_ratio

    if possible_cust in cust_dict:
        cust_id= cust_dict[possible_cust]
    else:
        cust_id = 'ID NOT Found in Bookings Sheet'

    if possible_so in sub_dict:
        sub_cust_name = sub_dict[possible_so]
    else:
        sub_cust_name = 'SO NOT Found in Subscription Sheet'

    my_list.append([saas_platform_name, saas_vrf_number, possible_cust, possible_so,
                    best_match, sub_cust_name, possible_so, cust_id])
    # print(saas_platform_name, possible_cust, best_match)
    # time.sleep(.5)


tool.push_list_to_xls(my_list, 'tmp_jim.xlsx')

