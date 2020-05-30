from my_app.tool_box import open_wb
from my_app.tool_box import push_list_to_xls
import time

class Customer:
    def __init__(self, cust_id):
        self.cust_id = cust_id
        self.pss = ''
        self.tsa = ''
        self.am = ''
        self.sales_lev_1 = ''
        self.sales_lev_2 = ''
        self.sales_lev_3 = ''
        self.sales_lev_4 = ''
        self.sales_lev_5 = ''
        self.sales_lev_6 = ''

        self.aliases = []  # Simple list of customer erp names for this cust id
        self.prod_booking = []
        self.svc_booking = []
        self.segments = []

        # self.orders = {}  # Simple dict of {SO #: [sku, price]}
        # self.as_pids = {}  # Simple dict of {SO #: [(pid1, as_customer_name, as_sku)]}
        # self.subs = []  # Simple list of lists of subscriptions[]
        # self.saas = {}

    def add_prod_booking(self, fiscal_year, fiscal_qtr, sku, booking_amt):
        self.prod_booking.append([fiscal_year, fiscal_qtr, sku, booking_amt])

    def add_svc_booking(self, fiscal_year, fiscal_qtr, sku, booking_amt, svc_type):
        self.svc_booking.append([fiscal_year, fiscal_qtr, sku, booking_amt, svc_type])

    def add_sls_levels(self, sls_lv1, sls_lv2, sls_lv3):
        # as_pid_info is a full list of tuples (as_pid, as_cust_name, as_sku)
        # with ALL PIDs for this SO for this cust_id
        self.segments.append([sls_lv1, sls_lv2, sls_lv3])

    def add_order(self, order_num, sku):
        # Check to see if this SO # already exists
        if order_num in self.orders:
            sku_list = self.orders[order_num]
            sku_list.append(sku)
            self.orders[order_num] = sku_list
        else:
            self.orders[order_num] = [sku]

    def add_alias(self, erp_name):
        add_it = True
        for alias in self.aliases:
            if alias == erp_name:
                add_it = False
                break
        if add_it is True:
            self.aliases.append(erp_name)

    def add_as_pid(self, order_num, as_pid_info):
        # as_pid_info is a full list of tuples (as_pid, as_cust_name, as_sku)
        # with ALL PIDs for this SO for this cust_id
        self.as_pids[order_num] = as_pid_info

    def add_sub_id(self, sub_info):
        # sub_id_pid_info is a list of lists (sub_id, sub_cust_name, start_date, renew_date, status, monthly_rev)
        # with ALL Subscriptions for this erp_customer name
        self.subs.append(sub_info)


def create_summary(total_prod, total_svc):
    deal_size = ''
    if total_prod <= 100000:
        deal_size = "Small"
    elif (total_prod > 100000) and (total_prod <= 750000):
        deal_size = 'Medium'
    elif total_prod > 750000:
        deal_size = 'Large'

    if total_prod > 0:
        prod_to_svc_ratio = round(((total_svc/total_prod)*100), 2)
        prod_to_svc_ratio = str(prod_to_svc_ratio)+' %'
    else:
        prod_to_svc_ratio = ''

    # results = {'cust_key': cust_key,
    #            'deal_size': deal_size,
    #            'total_prod': total_prod,
    #            'total_svc': total_svc,
    #            'prod_to_svc_mix': prod_to_svc_ratio
    #            }
    return [deal_size, prod_to_svc_ratio]


if __name__ == "__main__" and __package__ is None:
    wb_prod, ws_prod = open_wb('all_prod_tetration_bookings.xlsx')
    wb_svc, ws_svc = open_wb('all_as_tetration_bookings.xlsx')

    print('Opened:', ws_prod.nrows, ' Product Rows')
    print('Opened:', ws_svc.nrows, ' Service Rows')

    # Create a dict of Customer Objects
    cust_db = {}

    #
    # Loop over the product sheet
    #
    for row in range(1, ws_prod.nrows):
        fiscal_year = ws_prod.cell_value(row, 0)
        fiscal_qtr = ws_prod.cell_value(row, 1)
        sls_lv1 = ws_prod.cell_value(row, 3)
        sls_lv2 = ws_prod.cell_value(row, 4)
        sls_lv3 = ws_prod.cell_value(row, 5)
        cust_alias = ws_prod.cell_value(row, 13)
        cust_id = ws_prod.cell_value(row, 15)
        sku = ws_prod.cell_value(row, 19)
        prod_booking = ws_prod.cell_value(row, 21)

        # Does this Customer object exist ?
        if cust_id in cust_db:
            cust_obj = cust_db[cust_id]
        else:
            cust_obj = Customer(cust_id)
            cust_db[cust_id] = cust_obj

        cust_obj.add_alias(cust_alias)
        cust_obj.add_prod_booking(fiscal_year, fiscal_qtr, sku, prod_booking)
        cust_obj.add_sls_levels(sls_lv1, sls_lv2, sls_lv3)

    #
    # Loop over the services sheet
    #
    for row in range(1, ws_svc.nrows):
        fiscal_year = ws_prod.cell_value(row, 0)
        fiscal_qtr = ws_prod.cell_value(row, 1)
        svc_type = ws_svc.cell_value(row, 3)
        sku = ws_svc.cell_value(row, 7)
        sls_lv1 = ws_svc.cell_value(row, 11)
        sls_lv2 = ws_svc.cell_value(row, 12)
        sls_lv3 = ws_svc.cell_value(row, 13)
        cust_alias = ws_svc.cell_value(row, 20)
        cust_id = ws_svc.cell_value(row, 21)
        svc_booking = ws_svc.cell_value(row, 23)

        # Does this Customer object exist ?
        if cust_id in cust_db:
            cust_obj = cust_db[cust_id]
        else:
            cust_obj = Customer(cust_id)
            cust_db[cust_id] = cust_obj

        cust_obj.add_alias(cust_alias)
        cust_obj.add_svc_booking(fiscal_year, fiscal_qtr, sku, svc_booking, svc_type)
        cust_obj.add_sls_levels(sls_lv1, sls_lv2, sls_lv3)

    print('There are ', len(cust_db), 'Unique Customer IDs')
    print()

    #
    # Output the Customer Objects to xlsx
    #

    output_list = []
    header_row = ['customer_id', 'customer_aliases', 'customer_id_aliases',
                  'fiscal_year', 'fiscal_qtr',
                  'sales_level_1', 'sales_level_2', 'sales_level_3',
                  'sku_type', 'service_type',
                  'prod_sku', 'prod_booking', 'service_booking']
    output_list.append(header_row)

    summary_list = []
    header_row = ['customer_id_aliases',
                  'fiscal_year', 'fiscal_qtr',
                  'sales_level_1', 'sales_level_2', 'sales_level_3',
                  'deal_size', 'prod_to_svc_ratio',
                  'total_prod_booking', 'total_svc_booking']
    summary_list.append(header_row)

    # Loop over all the Customer Objects
    for cust_id, cust_obj in cust_db.items():

        # Format the aliases for output
        aliases = ''
        for alias in cust_obj.aliases:
            aliases = alias + " : " + aliases
        aliases = aliases[:-3]

        # Find the best fit for sales level
        tmp_dict = {}
        for segment in cust_obj.segments:
            tmp_tuple = tuple(segment)
            if tmp_tuple in tmp_dict:
                tmp_dict[tmp_tuple] = tmp_dict[tmp_tuple] + 1
            else:
                tmp_dict[tmp_tuple] = 1

        # Use the most frequently occurring Sales Levels
        most_freq = 0
        best_segment = ''
        for segment, freq in tmp_dict.items():
            if freq >= most_freq:
                best_segment = segment

        sls_lv1 = best_segment[0]
        sls_lv2 = best_segment[1]
        sls_lv3 = best_segment[2]

        # Create a key of the cust_id & aliases
        cust_key = cust_id + ' - ' + aliases
        cust_key = cust_key[:50]

        deal_size = ''
        total_prod = 0
        for booking in cust_obj.prod_booking:
            fiscal_year = booking[0]
            fiscal_qtr = booking[1]
            prod_sku = booking[2]
            prod_rev = booking[3]
            total_prod = total_prod + prod_rev
            output_list.append([cust_id, aliases, cust_key, fiscal_year, fiscal_qtr,
                                sls_lv1, sls_lv2, sls_lv3,
                                'product', '', prod_sku, prod_rev, 0])

        total_svc = 0

        for booking in cust_obj.svc_booking:
            fiscal_year = booking[0]
            fiscal_qtr = booking[1]
            svc_sku = booking[2]
            svc_rev = booking[3]
            svc_type = booking[4]
            total_svc = total_svc + svc_rev
            output_list.append([cust_id, aliases, cust_key, fiscal_year, fiscal_qtr,
                                sls_lv1, sls_lv2, sls_lv3,
                                'service', svc_type, svc_sku, 0, svc_rev])

        my_summary = create_summary(total_prod, total_svc)
        summary_list.append([cust_key, fiscal_year, fiscal_qtr,
                        sls_lv1, sls_lv2, sls_lv3,
                        my_summary[0], my_summary[1], total_prod, total_svc])

        # print(summary_list)
        # time.sleep(.4)

    push_list_to_xls(output_list, 'detail.xlsx')
    push_list_to_xls(summary_list, 'summary.xlsx')
    exit()

