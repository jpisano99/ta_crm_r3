import my_app.tool_box as tool
from my_app.settings import app_cfg
import xlrd
from datetime import datetime
import datetime
import time

#
# Get All Customer names and VRFs from Ravi's Sheet
#
telemetry_dict={}
telemetry_wb, telemetry_ws = tool.open_wb(app_cfg['XLS_TELEMETRY'])
print('Telemetry Customers Reporting', telemetry_ws.nrows)
for row in range(1, telemetry_ws.nrows):
    telemetry_name = telemetry_ws.cell_value(row, 0)
    telemetry_vrf_number = str(int(telemetry_ws.cell_value(row, 2)))
    telemetry_num_of_licenses = str(int(telemetry_ws.cell_value(row, 3)))
    telemetry_actual_sensors_installed = str(int(telemetry_ws.cell_value(row, 4)))
    telemetry_inactive_agents = str(int(telemetry_ws.cell_value(row, 5)))

    telemetry_dict[telemetry_name] = [telemetry_vrf_number, telemetry_num_of_licenses,
                                          telemetry_actual_sensors_installed, telemetry_inactive_agents]


#
# Get ALL subscriptions and Customer Names from Subscription Report
#
sub_dict = {}
sub_wb, sub_ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
print(sub_ws.nrows)
for row in range(1, sub_ws.nrows):
    sub_cust_name = sub_ws.cell_value(row, 2)
    sub_web_order = str(sub_ws.cell_value(row, 17))
    sub_renewal_date = sub_ws.cell_value(row, 11)

    if sub_ws.cell_type(row, 11) == xlrd.XL_CELL_DATE:
        sub_renewal_date = datetime.datetime(*xlrd.xldate_as_tuple(sub_renewal_date, sub_wb.datemode))
        # print(sub_renewal_date, type(sub_renewal_date))

    sub_dict[sub_web_order] = [sub_cust_name, sub_renewal_date]


#
# Get ALL PSS & TSA Contact Info
#
magic_dict={}
magic_wb, magic_ws = tool.open_wb(app_cfg['XLS_DASHBOARD'])
# print(magic_ws.nrows)
for row in range(1, magic_ws.nrows):
    magic_cust_name= magic_ws.cell_value(row, 3)
    magic_as_pid = magic_ws.cell_value(row, 2)
    magic_pss = magic_ws.cell_value(row, 6)
    magic_tsa = str(magic_ws.cell_value(row, 7))
    magic_as_dm= str(magic_ws.cell_value(row, 15))

    # print(magic_cust_name, magic_as_pid, magic_pss, magic_tsa, magic_as_dm)

    magic_dict[magic_cust_name] = [magic_as_pid, magic_pss, magic_tsa, magic_as_dm]

#
# Get ALL items from SAAS tracking sheet
#
saas_tracking_dict = {}
saas_tracking_wb, saas_tracking_ws = tool.open_wb(app_cfg['XLS_SAAS_TRACKING'])
print(saas_tracking_ws.nrows)
for row in range(1, saas_tracking_ws.nrows):
    saas_tracking_name = saas_tracking_ws.cell_value(row, 2)
    saas_cust_id = saas_tracking_ws.cell_value(row, 3)
    saas_telemetry_name = saas_tracking_ws.cell_value(row, 4)
    saas_tracking_so_number = saas_tracking_ws.cell_value(row, 6)
    saas_tracking_start_date = saas_tracking_ws.cell_value(row, 7)

    if saas_tracking_ws.cell_type(row, 7) == xlrd.XL_CELL_DATE:
        saas_tracking_start_date = datetime.datetime(*xlrd.xldate_as_tuple(saas_tracking_start_date, saas_tracking_wb.datemode))
        # print(saas_tracking_start_date, type(saas_tracking_start_date))

    if type(saas_tracking_so_number) is float:
        tmp_int = int(saas_tracking_so_number)
        saas_tracking_so_number = str(tmp_int)

    if type(saas_cust_id) is float:
        tmp_int = int(saas_cust_id)
        saas_cust_id = str(tmp_int)
    saas_tracking_dict[saas_telemetry_name] = [saas_tracking_name, saas_cust_id, saas_tracking_so_number, saas_tracking_start_date]


# #
# # Get ALL Unique customer Names and ID's from Bookings data
# #
# cust_dict = {}
# cust_wb, cust_ws = tool.open_wb(app_cfg['XLS_UNIQUE_CUSTOMERS'])
# print(cust_ws.nrows)
# for row in range(1, cust_ws.nrows):
#     cust_name = cust_ws.cell_value(row, 0)
#     cust_id = str(cust_ws.cell_value(row, 1))
#     # print(cust_name, cust_id)
#     # print(cust_name)
#     cust_dict[cust_name] = cust_id


print(telemetry_dict)
print(sub_dict)
print(magic_dict)

print()
print('*********************************')
#
# Perform a fuzzy match search against all customer aliases in Nirali's Sheet vs Ravi's Platform Sheet
#
my_list = []
my_list.append(['Customer Name',  'telemetry Name', 'telemetry VRF', 'Num Of Licenses ', 'Sensors Installed', 'Inactive Agents',
                '% Installed', '% Active', 'Sub Order Num', 'Fuzzy Score',
                'Req Start Date', 'Renewal Date', 'Days to Renew',
                'PSS', 'TSA', 'CX PID', 'CX Delivery Manager', 'Customer ID' ])
for telemetry_name, telemetry_info in telemetry_dict.items():
    telemetry_vrf_number = telemetry_info[0]
    telemetry_num_of_licenses = telemetry_info[1]
    telemetry_actual_sensors_installed = telemetry_info[2]
    telemetry_inactive_agents = telemetry_info[3]

    if telemetry_name in saas_tracking_dict:
        cust_name = saas_tracking_dict[telemetry_name][0]
        cust_id = saas_tracking_dict[telemetry_name][1]
        sub_so_num = saas_tracking_dict[telemetry_name][2]
        sub_start_date = saas_tracking_dict[telemetry_name][3]
        # print(cust_name, cust_id, sub_start_date)
        # exit()

    req_start_date = ''
    sub_renewal_date = ''
    days_to_renew = ''
    pss = ''
    tsa = ''
    as_pid = ''
    as_dm = ''

    # Some calculations
    pct_installed = ''
    pct_active = ''
    if int(telemetry_num_of_licenses) != 0:
        pct_installed = int(telemetry_actual_sensors_installed) / int(telemetry_num_of_licenses)
        pct_active = (int(telemetry_actual_sensors_installed) - int(telemetry_inactive_agents)) / int(telemetry_num_of_licenses)

    # Look up from dashboard
    if cust_name in magic_dict:
        pss = magic_dict[cust_name][1]
        tsa = magic_dict[cust_name][2]
        as_pid = magic_dict[cust_name][0]
        as_dm = magic_dict[cust_name][3]
        # [magic_as_pid, magic_pss, magic_tsa, magic_as_dm]
    else:
        cust_id = 'ID NOT Found in Bookings Sheet'

    # Calc Days to renew
    if isinstance(req_start_date, datetime.datetime) and isinstance(sub_renewal_date, datetime.datetime):
        now = datetime.datetime.now()
        days_to_renew = (sub_renewal_date - now).days

    my_list.append([cust_name, telemetry_name, telemetry_vrf_number, telemetry_num_of_licenses, telemetry_actual_sensors_installed, telemetry_inactive_agents,
                    pct_installed, pct_active, sub_so_num, 'TBD', req_start_date,
                    sub_renewal_date, days_to_renew, pss, tsa, as_pid, as_dm, cust_id])
    # print(saas_platform_name, possible_cust, best_match)
    # time.sleep(.5)


tool.push_list_to_xls(my_list, 'tmp_rosetta_stone.xlsx')

