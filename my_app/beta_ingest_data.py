import hashlib
from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Aliases, Sales_Orders, Subscriptions
import my_app.tool_box as tool
from datetime import datetime


now = datetime.now()

# sql = 'CREATE TABLE ta_adoption_db.archive_services_repo LIKE ta_adoption_db.services;'
# db.engine.execute(sql)
my_ingest_path = 'C:\\Users\jpisano\\my_app_data\\ta_adoption\\app_archives\\for_sql_ingest\\'

# my_ingest_file = 'tmp_TA Master Bookings as of 06-27-19.xlsx'
# my_ingest_file = 'tmp_TA Master Bookings as of 08-08-19.xlsx'
# my_ingest_file = 'tmp_TA Master Bookings as of 09-08-19.xlsx'
# my_ingest_file = 'tmp_TA Master Bookings as of 09-20-19.xlsx'
# my_ingest_file = 'tmp_TA Master Bookings as of 10-23-19.xlsx'
# my_ingest_file = 'tmp_TA Master Bookings as of 12-16-19.xlsx'

# my_ingest_file = 'tmp_ Master Subscriptions as of 06-27-19.xlsx'
# my_ingest_file = 'tmp_ Master Subscriptions as of 08-08-19.xlsx'
# my_ingest_file = 'tmp_ Master Subscriptions as of 09-08-19.xlsx'
# my_ingest_file = 'tmp_ Master Subscriptions as of 09-20-19.xlsx'
# my_ingest_file = 'tmp_ Master Subscriptions as of 10-23-19.xlsx'
# my_ingest_file = 'tmp_ Master Subscriptions as of 12-16-19.xlsx'

# my_ingest_file = 'tmp_AS Delivery as of 08-08-19.xlsx'
# my_ingest_file = 'tmp_AS Delivery as of 09-08-19.xlsx'
# my_ingest_file = 'tmp_AS Delivery as of 09-20-19.xlsx'
# my_ingest_file = 'tmp_AS Delivery as of 10-23-19.xlsx'
my_ingest_file = 'tmp_AS Delivery as of 12-16-19.xlsx'

date_tag = my_ingest_file[-13:-13 + 8]  # Grab the date if any
date_added = datetime.strptime(date_tag, "%m-%d-%y")
print(date_tag)

wb, ws = tool.open_wb(my_ingest_path+my_ingest_file)
my_csv = tool.xlrd_wb_to_csv(wb, ws)


my_new_list = []
last_col = len(my_csv[0])
for my_row in my_csv:
    my_row.insert(0, '')
    my_row.insert(last_col + 1, 'hash')
    my_row.insert(last_col + 2, date_added)
    my_new_list.append(my_row)

tool.push_list_to_csv(my_new_list, my_ingest_path+'csv_services.csv')

# tool.load_infile('archive_services_repo', my_ingest_path+'csv_services.csv', delete_rows=True)
tool.load_infile('archive_services_repo', my_ingest_path+'csv_services.csv', delete_rows=False)



exit()













my_subs = Subscriptions.query.all()
col_names = []

# Add the Hash Value for this output_row
for r in my_subs:
    hash_string = ''
    row_list = [str(r.bill_to_customer),
               str(r.reseller),
               str(r.end_customer),
               str(r.offer_name),
               str(r.consumption_health),
               str(r.over_consumed_tf_groups),
               str(r.next_true_forward),
               str(r.subscription_id),
               str(r.status),
               str(r.start_date),
               str(r.initial_term),
               str(r.renewal_date),
               str(r.currency),
               str(r.monthly_charge),
               str(r.auto_renewal_term),
               str(r.billing_model),
               str(r.purchase_order_number),
               str(r.weborderid),
               str(r.site_url),
               str(r.customer_success_manager),
               str(r.partner_success_manager),
               str(r.sales_owner),
               str(r.customer_success_manager_email),
               str(r.partner_success_manager_email),
               str(r.sales_owner_email),
               str(r.account_type),
               str(r.days_until_renewal)]

    for col_data in row_list:
        hash_string = hash_string + col_data

    hash_val = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    r.hash_value = hash_val

    # print(hash_string)
    #print('\t', hash_val,'    ', len(hash_string))
    # time.sleep(.5)

db.session.commit()
exit()











    #
    # for k, v in r.__dict__.items():
    #     if k.find('_', 0, 1) != -1:
    #         continue
    #     print(k)
    #     hash_string = hash_string + str(v)
    #
    # break

hash_val = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
print(hash_string)
print(hash_val)

# for r in my_subs:
#     for col_num, col_name in enumerate(col_names):
#         print(col_num, col_name, r.col_names[col_num])

exit()

    # for col in r:
    #     print(dir(col))
        # str_to_hash = r.subscription_id
        # hash_val = hashlib.md5(str_to_hash.encode('utf-8')).hexdigest()
        # print(r.subscription_id, hash_val)





















id = db.Column(db.Integer(), primary_key=True)
bill_to_customer = db.Column(db.String(50))
reseller = db.Column(db.String(50))
end_customer = db.Column(db.String(50))
offer_name = db.Column(db.String(50))
consumption_health = db.Column(db.String(50))
over_consumed_tf_groups = db.Column(db.String(50))
next_true_forward = db.Column(db.String(50))
subscription_id = db.Column(db.String(50))
status = db.Column(db.String(50))
start_date = db.Column(db.DateTime)
initial_term = db.Column(db.String(50))
renewal_date = db.Column(db.DateTime)
currency = db.Column(db.String(50))
monthly_charge = db.Column(db.String(50))
auto_renewal_term = db.Column(db.String(50))
billing_model = db.Column(db.String(50))
purchase_order_number = db.Column(db.String(50))
weborderid = db.Column(db.String(50))
site_url = db.Column(db.String(50))
customer_success_manager = db.Column(db.String(50))
partner_success_manager = db.Column(db.String(50))
sales_owner = db.Column(db.String(50))
customer_success_manager_email = db.Column(db.String(50))
partner_success_manager_email = db.Column(db.String(50))
sales_owner_email = db.Column(db.String(50))
account_type = db.Column(db.String(50))
days_until_renewal = db.Column(db.String(50))
