import my_app.tool_box as tool
from my_app.settings import app_cfg
from my_app.Customer import Customer
# from my_app.func_lib.find_team import find_team
from datetime import datetime
import xlrd
import time


def get_subscriptions(sub_ws, cust_name):
    for row_num in range(1, sub_ws.nrows):
        if sub_ws.cell_value(row_num, 2) != cust_name:
            continue
        else:
            # Gather the fields we want
            sub_cust_name = sub_ws.cell_value(row_num, 2)
            sub_sku = sub_ws.cell_value(row_num, 3)
            sub_id = sub_ws.cell_value(row_num, 7)
            sub_web_order_id = sub_ws.cell_value(row_num, 17)
            sub_term = sub_ws.cell_value(row_num, 10)
            sub_start_date = sub_ws.cell_value(row_num, 9)
            sub_renew_date = sub_ws.cell_value(row_num, 11)
            sub_renew_status = sub_ws.cell_value(row_num, 8)
            sub_monthly_rev = sub_ws.cell_value(row_num, 13)

            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(sub_start_date, sub_wb.datemode)
            sub_start_date = datetime(year, month, day)

            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(sub_renew_date, sub_wb.datemode)
            sub_renew_date = datetime(year, month, day)

            print(sub_cust_name, sub_sku, sub_id, sub_web_order_id, sub_term,
                  sub_start_date, sub_renew_date, sub_renew_status, sub_monthly_rev)

            # if sub_cust_name in cust_alias_db:
            #     cust_id = cust_alias_db[sub_cust_name]
            #     cust_obj = cust_db[cust_id]
            #     sub_info = [sub_id, sub_cust_name, sub_start_date, sub_renew_date, sub_renew_status, sub_monthly_rev]
            #     cust_obj.add_sub_id(sub_info)

    return


if __name__ == "__main__" and __package__ is None:
    sub_wb, sub_ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
    # cust_name = 'PENSKE LOGISTICS LLC'
    # cust_name = 'BLUE CROSS & BLUE SHIELD OF ALABAMA'
    # cust_name = 'CENTERS FOR MEDICARE AND MEDICAID SERVICES'
    # cust_name = 'FEDEX SERVICES'
    cust_name = 'JACOB K JAVITS CONVENTION CTR'

    get_subscriptions(sub_ws, cust_name)