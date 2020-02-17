import my_app.tool_box as tool
from my_app.settings import app_cfg
from datetime import datetime
import time

# Get SAAS Data from the BU Tracking Sheet
saas_tracking_dict = {}
saas_tracking_rows = tool.get_list_from_ss(app_cfg['SS_SAAS'])

for my_row in range(1, len(saas_tracking_rows)):
    saas_tracking_name = saas_tracking_rows[my_row][2]
    saas_cust_id = saas_tracking_rows[my_row][3]
    saas_telemetry_name = saas_tracking_rows[my_row][4]
    saas_tracking_so_number = saas_tracking_rows[my_row][6]
    saas_tracking_start_date = saas_tracking_rows[my_row][7]

    if saas_tracking_start_date != '':
        saas_tracking_start_date = datetime.strptime(saas_tracking_start_date, '%Y-%m-%d')

    if type(saas_tracking_so_number) is float:
        tmp_int = int(saas_tracking_so_number)
        saas_tracking_so_number = str(tmp_int)

    if type(saas_cust_id) is float:
        tmp_int = int(saas_cust_id)
        saas_cust_id = str(tmp_int)

    saas_tracking_dict[saas_telemetry_name] = [saas_tracking_name, saas_cust_id, saas_tracking_so_number,
                                               saas_tracking_start_date]

print(saas_tracking_dict)
exit()