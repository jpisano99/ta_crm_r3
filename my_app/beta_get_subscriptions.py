import my_app.tool_box as tool
from my_app.settings import app_cfg
from datetime import datetime
import xlrd
from my_app.models import Subscriptions


def get_subscriptions(sub_ws, cust_name):

    my_subscriptions = Subscriptions.query.filter(Subscriptions.end_customer == cust_name).all()
    my_subscription = ''

    subs_list = []
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

            subs_list.append([sub_cust_name, sub_sku, sub_id, sub_web_order_id, sub_term,
                             sub_start_date, sub_renew_date, sub_renew_status, sub_monthly_rev])

    return subs_list


if __name__ == "__main__" and __package__ is None:
    sub_wb, sub_ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
    # cust_name = 'PENSKE LOGISTICS LLC'
    # cust_name = 'BLUE CROSS & BLUE SHIELD OF ALABAMA'
    # cust_name = 'CENTERS FOR MEDICARE AND MEDICAID SERVICES'
    # cust_name = 'FEDEX SERVICES'
    cust_name = 'JACOB K JAVITS CONVENTION CTR'

    my_subs = get_subscriptions(sub_ws, cust_name)
    for my_sub in my_subs:
        print(my_sub)
