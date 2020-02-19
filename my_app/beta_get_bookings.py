import my_app.tool_box as tool
from my_app.settings import app_cfg
from datetime import datetime
import xlrd

from my_app.models import Bookings


def get_bookings(cust_name, coverage_dict):
    my_bookings = Bookings.query.filter(Bookings.erp_end_customer_name == cust_name).all()
    my_booking = ''

    for my_booking in my_bookings:
        pass

    jim = [my_booking.end_customer_global_ultimate_id,
            my_booking.erp_end_customer_name,
            my_booking.web_order_id,
            my_booking.erp_sales_order_number,
            my_booking.product_id,
            my_booking.sales_level_1,
            my_booking.sales_level_2,
            my_booking.sales_level_3,
            my_booking.sales_level_4,
            my_booking.sales_level_5,
            my_booking.sales_agent_name]

    print(jim)

    exit()
    # bookings_list = []
    # bookings = []
    # booking_rec = {}
    #
    # for row_num in range(1, cust_ws.nrows):
    #     if cust_ws.cell_value(row_num, 13) != cust_name:
    #         continue
    #     else:
    #         # Gather the fields we want
    #         cust_id = cust_ws.cell_value(row_num, 15)
    #         cust_erp_name = cust_ws.cell_value(row_num, 13)
    #         cust_ultimate_name = cust_ws.cell_value(row_num, 14)
    #         cust_so = cust_ws.cell_value(row_num, 11)
    #         cust_sku = cust_ws.cell_value(row_num, 19)
    #         cust_sales_lev_1 = cust_ws.cell_value(row_num, 3)
    #         cust_sales_lev_2 = cust_ws.cell_value(row_num, 4)
    #         cust_sales_lev_3 = cust_ws.cell_value(row_num, 5)
    #         cust_sales_lev_4 = cust_ws.cell_value(row_num, 6)
    #         cust_sales_lev_5 = cust_ws.cell_value(row_num, 7)
    #         cust_sales_lev_6 = cust_ws.cell_value(row_num, 8)
    #         cust_acct_mgr = cust_ws.cell_value(row_num, 9)
    #
    #         sales_level = cust_sales_lev_1 + ',' + cust_sales_lev_2 + ',' + cust_sales_lev_3 + ',' + \
    #             cust_sales_lev_4 + ',' + cust_sales_lev_5 + ',' + cust_sales_lev_6
    #
    #         sales_team = tool.find_team(coverage_dict, sales_level)
    #         pss = sales_team[0]
    #         tsa = sales_team[1]
    #
    #     bookings_list.append([cust_id, cust_erp_name, cust_ultimate_name, cust_so, cust_sku,
    #            cust_sales_lev_1, cust_sales_lev_2, cust_sales_lev_3, cust_sales_lev_4, cust_sales_lev_5, cust_sales_lev_6,
    #            cust_acct_mgr, pss, tsa])
    #
    #     booking_rec["sls_lv1"] = cust_sales_lev_1
    #     booking_rec["sls_lv2"] = cust_sales_lev_2
    #     booking_rec["sls_lv3"] = cust_sales_lev_3
    #     booking_rec["sls_lv4"] = cust_sales_lev_4
    #     booking_rec["sls_lv5"] = cust_sales_lev_5
    #     booking_rec["sls_lv6"] = cust_sales_lev_6
    #     print(booking_rec)
    #     exit()

    return


if __name__ == "__main__" and __package__ is None:
    # bookings_wb, bookings_ws = tool.open_wb(app_cfg['XLS_BOOKINGS'])
    team_dict = tool.build_coverage_dict()

    # cust_name = 'PENSKE LOGISTICS LLC'
    # cust_name = 'BLUE CROSS & BLUE SHIELD OF ALABAMA'
    # cust_name = 'CENTERS FOR MEDICARE AND MEDICAID SERVICES'
    # cust_name = 'FEDEX SERVICES'
    cust_name = 'JACOB K JAVITS CONVENTION CTR'

    my_bookings = get_bookings(cust_name, team_dict)

    for booking in my_bookings:
        print(booking)

