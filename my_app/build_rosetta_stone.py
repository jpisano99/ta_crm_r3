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
sub_by_num_dict = {}
sub_by_name_dict = {}
sub_wb, sub_ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
print(sub_ws.nrows)
for row in range(1, sub_ws.nrows):
    sub_cust_name = sub_ws.cell_value(row, 2)
    sub_status = sub_ws.cell_value(row, 8)
    sub_term = str(int(sub_ws.cell_value(row, 10)))
    sub_renewal_date = sub_ws.cell_value(row, 11)
    sub_web_order = str(sub_ws.cell_value(row, 17))

    if sub_ws.cell_type(row, 11) == xlrd.XL_CELL_DATE:
        sub_renewal_date = datetime.datetime(*xlrd.xldate_as_tuple(sub_renewal_date, sub_wb.datemode))

    sub_by_num_dict[sub_web_order] = [sub_cust_name, sub_term, sub_renewal_date, sub_status]
    sub_by_name_dict[sub_cust_name] = [sub_web_order, sub_term, sub_renewal_date, sub_status]


#
# Get ALL Enterprise Agreement Subscripption Data
#
en_by_num_dict = {}
en_by_name_dict = {}
en_wb, en_ws = tool.open_wb(app_cfg['XLS_EN_AGREEMENTS'])
print(en_ws.nrows)
for row in range(1, en_ws.nrows):
    en_cust_name = en_ws.cell_value(row, 2)
    en_status = en_ws.cell_value(row, 8)
    en_term = str(int(en_ws.cell_value(row, 10)))
    en_renewal_date = en_ws.cell_value(row, 11)
    en_web_order = str(en_ws.cell_value(row, 17))

    if en_ws.cell_type(row, 11) == xlrd.XL_CELL_DATE:
        en_renewal_date = datetime.datetime(*xlrd.xldate_as_tuple(en_renewal_date, en_wb.datemode))

    en_by_num_dict[en_web_order] = [en_cust_name, en_term, en_renewal_date, en_status]
    en_by_name_dict[en_cust_name] = [en_web_order, en_term, en_renewal_date, en_status]

# ELA2-M
# EA2F-SECURITY-4S
# E2-N-TAAS
#
#
# Sub309212
# E2-N-TAAS
# E2N-TAAS-WPFND


#
# Get ALL PSS & TSA Contact Info
#
magic_dict={}
magic_wb, magic_ws = tool.open_wb(app_cfg['XLS_DASHBOARD'])
# print(magic_ws.nrows)
for row in range(1, magic_ws.nrows):
    magic_cust_name= magic_ws.cell_value(row, 3)
    magic_as_pid = magic_ws.cell_value(row, 2)
    magic_sales_lv_1 = magic_ws.cell_value(row, 4)
    magic_sales_lv_2 = magic_ws.cell_value(row, 5)
    magic_pss = magic_ws.cell_value(row, 6)
    magic_tsa = str(magic_ws.cell_value(row, 7))
    magic_as_dm= str(magic_ws.cell_value(row, 15))

    magic_dict[magic_cust_name] = [magic_as_pid, magic_pss, magic_tsa,
                                   magic_sales_lv_1, magic_sales_lv_2, magic_as_dm]

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


print(telemetry_dict)
print(sub_by_num_dict)
print(sub_by_name_dict)
print(magic_dict)

print()
print('**************BUILD THE SHEET*******************')
print()

my_list = []
my_list.append(['Customer Name',  'Telemetry Name', 'Telemetry VRF', 'Num Of Licenses ', 'Sensors Installed', 'Inactive Agents',
                '% Installed', '% Active', 'Adoption Factor','Sub Order Num', ' Sub Term', 'Sub Status',
                'Req Start Date', 'Renewal Date', 'Days to Renew',
                'PSS', 'TSA', 'Sales Lv 1', 'Sales Lv 2', 'CX PID', 'CX Delivery Manager', 'Customer ID'])

for telemetry_name, telemetry_info in telemetry_dict.items():
    telemetry_vrf_number = telemetry_info[0]
    telemetry_num_of_licenses = telemetry_info[1]
    telemetry_actual_sensors_installed = telemetry_info[2]
    telemetry_inactive_agents = telemetry_info[3]

    # Get the SasS Tracking Data
    cust_name = ''
    cust_id = ''
    sub_so_num = ''
    sub_start_date = ''
    req_start_date = ''
    if telemetry_name in saas_tracking_dict:
        cust_name = saas_tracking_dict[telemetry_name][0]
        cust_id = saas_tracking_dict[telemetry_name][1]
        sub_so_num = saas_tracking_dict[telemetry_name][2]
        req_start_date = saas_tracking_dict[telemetry_name][3]

    # Get the Subscription Data
    sub_term = ''
    sub_renewal_date = ''
    sub_status = ''
    if sub_so_num in sub_by_num_dict:
        sub_term = sub_by_num_dict[sub_so_num][1]
        sub_renewal_date = sub_by_num_dict[sub_so_num][2]
        sub_status = sub_by_num_dict[sub_so_num][3]

    elif sub_so_num in en_by_num_dict:
        sub_term = en_by_num_dict[sub_so_num][1]
        sub_renewal_date = en_by_num_dict[sub_so_num][2]
        sub_status = en_by_num_dict[sub_so_num][3]

    elif cust_name in sub_by_name_dict:
        sub_term = sub_by_name_dict[cust_name][1]
        sub_renewal_date = sub_by_name_dict[cust_name][2]
        sub_status = sub_by_name_dict[cust_name][3]
    else:
        sub_status = "Subscription Not Found"

    # Get the Sales Contact Info
    as_pid = ''
    pss = ''
    tsa = ''
    as_dm = ''
    sales_lv_1 = ''
    sales_lv_2 = ''
    if cust_name in magic_dict:
        as_pid = magic_dict[cust_name][0]
        pss = magic_dict[cust_name][1]
        tsa = magic_dict[cust_name][2]
        sales_lv_1 = magic_dict[cust_name][3]
        sales_lv_2 = magic_dict[cust_name][4]
        as_dm = magic_dict[cust_name][3]
    else:
        cust_id = 'ID NOT Found in Bookings Sheet'

    # Calc Sensor Utilization
    pct_installed = ''
    pct_active = ''
    if int(telemetry_num_of_licenses) != 0:
        pct_installed = int(telemetry_actual_sensors_installed) / int(telemetry_num_of_licenses)
        pct_active = (int(telemetry_actual_sensors_installed) - int(telemetry_inactive_agents)) / int(telemetry_num_of_licenses)



    # Calc Days to renew
    days_to_renew = ''
    now = datetime.datetime.now()
    adoption_factor = ''
    if isinstance(req_start_date, datetime.datetime) and isinstance(sub_renewal_date, datetime.datetime):
        days_to_renew = (sub_renewal_date - now).days

        sub_days_total = int(sub_term) * 30
        sub_days_active = sub_days_total - days_to_renew

        pct_sub_expired = sub_days_active/sub_days_total
        print(sub_renewal_date, sub_days_total,sub_days_active, days_to_renew, pct_sub_expired)
        adoption_factor = (pct_active / pct_sub_expired) * 100
        print()
        print(pct_active, adoption_factor)

        pct_installed = str(round((pct_installed * 100), 1)) + '%'
        pct_active = str(round((pct_active * 100), 1)) + '%'



    # Build the output row
    my_list.append([cust_name, telemetry_name, telemetry_vrf_number, telemetry_num_of_licenses,
                    telemetry_actual_sensors_installed, telemetry_inactive_agents,
                    pct_installed, pct_active, adoption_factor, sub_so_num, sub_term, sub_status, req_start_date,
                    sub_renewal_date, days_to_renew, pss, tsa, sales_lv_1, sales_lv_2, as_pid, as_dm, cust_id])

tool.push_list_to_xls(my_list, 'tmp_rosetta_stone.xlsx')

