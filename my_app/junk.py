import my_app.tool_box as tool
from my_app.settings import app_cfg
import datetime
import xlrd
import time

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

print(len(sub_by_name_dict))

#
# Get data from Rosetta Stone Data
#
adopt_dict = {}
adopt_rows = tool.get_list_from_ss('TA Telemetry w/ Adoption Factor as of 2/18/20')
for my_row in range(1, len(adopt_rows)):
    cust_name = adopt_rows[my_row][0]
    num_of_lic = str(adopt_rows[my_row][1]) + '_non$_'
    pct_adopt = str(adopt_rows[my_row][2]) + '_%_'
    sub_status = adopt_rows[my_row][6]
    pss = adopt_rows[my_row][8]
    try:
        sensors_installed = str(int(adopt_rows[my_row][14])) + '_non$_'
    except:
        sensors_installed = adopt_rows[my_row][14]
    adopt_dict[cust_name] = [num_of_lic, sensors_installed, pct_adopt, sub_status, pss]

#
# Main loop over Backlog List
#
cx_tracking_rows = tool.get_list_from_ss('Tetration US Customers CX Priority List - Top 35')
cx_tracking_list = [['Customer', 'Customer ID', 'CX PID', 'CX Qtr', 'CX Comments',
                    'Num of Lic', 'Sensors Installed', 'Pct Adopt', 'Sub Status', 'PSS']]
for my_row in range(1, len(cx_tracking_rows)):
    cx_cust_name = cx_tracking_rows[my_row][7]

    # Customer ID
    if cx_tracking_rows[my_row][8] != '':
        cx_cust_id = str(int(cx_tracking_rows[my_row][8]))
    else:
        cx_cust_id = ''

    # CX PID
    if cx_tracking_rows[my_row][9] != '':
        try:
            cx_pid = str(int(cx_tracking_rows[my_row][9])) + '_non$_'
        except:
            cx_pid = str(cx_tracking_rows[my_row][9])

    cx_qtr = cx_tracking_rows[my_row][13]
    cx_comments = cx_tracking_rows[my_row][21]

    telemetry_data = []
    if cx_cust_name in adopt_dict:
        telemetry_data = adopt_dict[cx_cust_name]
    else:
        telemetry_data.append('No Telemetry Data Found')
        telemetry_data.append('')
        telemetry_data.append('')
        telemetry_data.append('')
        telemetry_data.append('')
        # If no telemetry then do a subscription look up
        if cx_cust_name in sub_by_name_dict:
            print(cx_cust_name, sub_by_name_dict[cx_cust_name])
            exit()

            # sub_by_name_dict[sub_cust_name] = [sub_web_order, sub_term, sub_renewal_date, sub_status]
        else:
            pass

    # print(cx_cust_name,cx_cust_id, cx_pid, cx_qtr, cx_comments, telemetry_data)
    # print(cx_cust_name, cx_cust_id, cx_pid, cx_qtr, cx_comments)
    cx_tracking_list.append([cx_cust_name, cx_cust_id, cx_pid, cx_qtr, cx_comments,
                             telemetry_data[0], telemetry_data[1], telemetry_data[2],
                             telemetry_data[3], telemetry_data[4]])

print(cx_tracking_list)
tool.push_list_to_xls(cx_tracking_list, 'jim.xlsx')

exit()
