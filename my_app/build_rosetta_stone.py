import my_app.tool_box as tool
from my_app.settings import app_cfg
import xlrd
import datetime

#
# Get All Customer names and VRFs from Ravi's Sheet
#
telemetry_dict = {}
telemetry_wb, telemetry_ws = tool.open_wb(app_cfg['XLS_TELEMETRY'])
print('Telemetry Customers Reporting', telemetry_ws.nrows)
for row in range(1, telemetry_ws.nrows):
    telemetry_name = telemetry_ws.cell_value(row, 2)
    telemetry_vrf_number = str(int(telemetry_ws.cell_value(row, 3)))
    telemetry_num_of_licenses = telemetry_ws.cell_value(row, 4)
    telemetry_actual_sensors_installed = telemetry_ws.cell_value(row, 5)
    telemetry_inactive_agents = telemetry_ws.cell_value(row, 6)

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
# Get ALL Enterprise Agreement Subscription Data
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

#
# Get ALL PSS & TSA Contact Info
#
magic_dict = {}
magic_wb, magic_ws = tool.open_wb(app_cfg['XLS_DASHBOARD'])
for row in range(1, magic_ws.nrows):
    magic_cust_name = magic_ws.cell_value(row, 3)
    magic_as_pid = magic_ws.cell_value(row, 2)
    magic_sales_lv_1 = magic_ws.cell_value(row, 4)
    magic_sales_lv_2 = magic_ws.cell_value(row, 5)
    magic_pss = magic_ws.cell_value(row, 6)
    magic_tsa = str(magic_ws.cell_value(row, 7))
    magic_as_dm = str(magic_ws.cell_value(row, 15))

    magic_dict[magic_cust_name] = [magic_as_pid, magic_pss, magic_tsa,
                                   magic_sales_lv_1, magic_sales_lv_2, magic_as_dm]

#
# Get ALL items from BU SAAS Smartsheet tracking sheet
#
saas_tracking_dict = {}
saas_tracking_rows = tool.get_list_from_ss(app_cfg['SS_SAAS'])

for my_row in range(1, len(saas_tracking_rows)):
    saas_tracking_name = saas_tracking_rows[my_row][2]
    saas_cust_id = saas_tracking_rows[my_row][3]
    saas_telemetry_name = saas_tracking_rows[my_row][4]
    saas_tracking_so_number = saas_tracking_rows[my_row][6]
    saas_tracking_start_date = saas_tracking_rows[my_row][7]

    if saas_tracking_start_date != '':
        saas_tracking_start_date = datetime.datetime.strptime(saas_tracking_start_date, '%Y-%m-%d')

    if type(saas_tracking_so_number) is float:
        tmp_int = int(saas_tracking_so_number)
        saas_tracking_so_number = str(tmp_int)

    if type(saas_cust_id) is float:
        tmp_int = int(saas_cust_id)
        saas_cust_id = str(tmp_int)

    saas_tracking_dict[saas_telemetry_name] = [saas_tracking_name, saas_cust_id, saas_tracking_so_number,
                                               saas_tracking_start_date]

print(telemetry_dict)
print(sub_by_num_dict)
print(sub_by_name_dict)
print(magic_dict)
print(saas_tracking_dict)

print()
print('**************BUILD THE SHEET*******************')
print()

my_list = []
as_of_date = '2/3/20'
my_list.append(['Customer Name', 'Num Of Licenses ', '% of Sensors Installed', '% of Active Sensors',
                'Adoption Factor' + '\n' + '(% Active Sensors : % of Subscription Consumed)'
                + '\n' + ' as of ' + as_of_date,
                'Subscription Term', 'Subscription Status', 'Days to Renew',
                'PSS', 'TSA', 'Sales Lv 1', 'Sales Lv 2',
                'Telemetry Name', 'Telemetry VRF',  'Sensors Installed', 'Active Agents',
                'Sub Order Num', 'Req Start Date', 'Renewal Date',
                'CX PID', 'CX Delivery Manager', 'Customer ID'])

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
        cust_name = "Missing Data: - "+telemetry_name
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
        as_dm = magic_dict[cust_name][5]
    else:
        cust_id = 'Cust ID NOT Found in Bookings Sheet'

    # Calc Sensor Utilization
    pct_installed = 0
    pct_active = 0
    telemetry_active_agents = 0
    if int(telemetry_num_of_licenses) != 0:
        telemetry_active_agents = telemetry_actual_sensors_installed - telemetry_inactive_agents
        pct_installed = telemetry_actual_sensors_installed / telemetry_num_of_licenses
        pct_active = telemetry_active_agents / telemetry_num_of_licenses

    # Calc Days to renew
    days_to_renew = ''
    now = datetime.datetime.now()
    adoption_factor = 0
    if isinstance(req_start_date, datetime.datetime) and isinstance(sub_renewal_date, datetime.datetime):
        days_to_renew = (sub_renewal_date - now).days

        sub_days_total = int(sub_term) * 30
        sub_days_active = sub_days_total - days_to_renew

        pct_sub_expired = sub_days_active/sub_days_total
        adoption_factor = (pct_active / pct_sub_expired)

    # All the math is done so now
    # Format these all to push_list_to_xls.py
    telemetry_num_of_licenses = int(telemetry_num_of_licenses)
    telemetry_actual_sensors_installed = int(telemetry_actual_sensors_installed)
    telemetry_active_agents = int(telemetry_active_agents)
    pct_installed = str(round(pct_installed, 1)) + '_%_'
    pct_active = str(round(pct_active, 1)) + '_%_'
    adoption_factor = str(round(adoption_factor, 2)) + '_non$_'

    # Build the output row
    my_list.append([cust_name, telemetry_num_of_licenses, pct_installed, pct_active,
                    adoption_factor,
                    sub_term, sub_status, days_to_renew,
                    pss, tsa, sales_lv_1, sales_lv_2,
                    telemetry_name, telemetry_vrf_number,
                    telemetry_actual_sensors_installed, telemetry_active_agents,
                    sub_so_num, req_start_date, sub_renewal_date,
                    as_pid, as_dm, cust_id])

tool.push_list_to_xls(my_list, 'tmp_rosetta_stone.xlsx', app_cfg['UPDATES_SUB_DIR'], 'tbl_rosetta')
