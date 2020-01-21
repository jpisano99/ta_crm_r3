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

exit()

saas_wb, saas_ws = tool.open_wb(app_cfg['XLS_SAAS_NAMES'])
print(saas_ws.nrows)

cust_wb, cust_ws = tool.open_wb(app_cfg['XLS_UNIQUE_CUSTOMERS'])
print(cust_ws.nrows)




# do a fuzzy match search against all customer aliases
best_match = 0
for k, v in cust_alias_db.items():
    match_ratio = fuzz.ratio(as_cust_name, k)
    if match_ratio > best_match:
        possible_cust = k
        best_match = match_ratio
