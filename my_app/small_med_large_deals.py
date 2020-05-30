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

    def add_prod_booking(self, sku, booking_amt):
        # as_pid_info is a full list of tuples (as_pid, as_cust_name, as_sku)
        # with ALL PIDs for this SO for this cust_id
        self.prod_booking.append([sku, booking_amt])

    def add_svc_booking(self, sku, booking_amt):
        # as_pid_info is a full list of tuples (as_pid, as_cust_name, as_sku)
        # with ALL PIDs for this SO for this cust_id
        self.svc_booking.append([sku, booking_amt])

    def add_sls_levels(self, sls_lv1, sls_lv2):
        # as_pid_info is a full list of tuples (as_pid, as_cust_name, as_sku)
        # with ALL PIDs for this SO for this cust_id
        self.segments.append([sls_lv1, sls_lv2])

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
        sls_lv1 = ws_prod.cell_value(row, 3)
        sls_lv2 = ws_prod.cell_value(row, 4)
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
        cust_obj.add_prod_booking(sku, prod_booking)
        cust_obj.add_sls_levels(sls_lv1, sls_lv2)

    #
    # Loop over the services sheet
    #
    for row in range(1, ws_svc.nrows):
        sls_lv1 = ws_svc.cell_value(row, 11)
        sls_lv2 = ws_svc.cell_value(row, 12)
        sku = ws_svc.cell_value(row, 7)
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
        cust_obj.add_svc_booking(sku, svc_booking)
        cust_obj.add_sls_levels(sls_lv1, sls_lv2)

    print('There are ', len(cust_db), 'Unique Customer IDs')
    print()

    # for cust_id, cust_obj in cust_db.items():
    #     print(cust_id, '\t', cust_obj.aliases)
    #     print('\t\t', cust_obj.prod_booking)
    #     print('\t\t', cust_obj.svc_booking)
    #     print('\t\t', cust_obj.segments)
    #     print()

    output_list = []
    header_row = ['customer_id', 'customer_aliases',
                  'sales_level_1', 'sales_level_2', 'sku_type',
                  'prod_sku', 'prod_booking',
                  'svc_sku', 'svc_booking']
    output_list.append(header_row)

    for cust_id, cust_obj in cust_db.items():

        aliases = ''
        for alias in cust_obj.aliases:
            aliases = alias + " : " + aliases

        sls_lv1 = cust_obj.segments[0][0]
        sls_lv2 = cust_obj.segments[0][1]
        print(aliases)

        for booking in cust_obj.prod_booking:
            prod_sku = booking[0]
            prod_rev = booking[1]
            output_list.append([cust_id, aliases, sls_lv1, sls_lv2, 'product', prod_sku, prod_rev, '', 0])
            # print(booking)

        for booking in cust_obj.svc_booking:
            svc_sku = booking[0]
            svc_rev = booking[1]
            output_list.append([cust_id, aliases, sls_lv1, sls_lv2, 'service', svc_sku, 0, '', svc_rev])
            # print(booking)

    push_list_to_xls(output_list, 'stan.xlsx')
    exit()

