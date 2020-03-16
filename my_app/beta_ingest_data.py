import hashlib
from my_app import db
from my_app.models import Bookings, Customer_Ids, Customer_Aliases, Sales_Orders, Subscriptions
import my_app.tool_box as tool
from datetime import datetime
import time

tool.create_row_hash('Archive_Telemetry_Repo')

exit()

#
#
#
# now = datetime.now()
#
# # sql = 'CREATE TABLE ta_adoption_db.archive_services_repo LIKE ta_adoption_db.services;'
# # db.engine.execute(sql)
# my_ingest_path = 'C:\\Users\jpisano\\my_app_data\\ta_adoption\\app_archives\\for_sql_ingest\\'
#
# # my_ingest_file = 'tmp_TA Master Bookings as of 06-27-19.xlsx'
# # my_ingest_file = 'tmp_TA Master Bookings as of 08-08-19.xlsx'
# # my_ingest_file = 'tmp_TA Master Bookings as of 09-08-19.xlsx'
# # my_ingest_file = 'tmp_TA Master Bookings as of 09-20-19.xlsx'
# # my_ingest_file = 'tmp_TA Master Bookings as of 10-23-19.xlsx'
# # my_ingest_file = 'tmp_TA Master Bookings as of 12-16-19.xlsx'
#
# # my_ingest_file = 'tmp_ Master Subscriptions as of 06-27-19.xlsx'
# # my_ingest_file = 'tmp_ Master Subscriptions as of 08-08-19.xlsx'
# # my_ingest_file = 'tmp_ Master Subscriptions as of 09-08-19.xlsx'
# # my_ingest_file = 'tmp_ Master Subscriptions as of 09-20-19.xlsx'
# # my_ingest_file = 'tmp_ Master Subscriptions as of 10-23-19.xlsx'
# # my_ingest_file = 'tmp_ Master Subscriptions as of 12-16-19.xlsx'
#
# # my_ingest_file = 'tmp_AS Delivery as of 08-08-19.xlsx'
# # my_ingest_file = 'tmp_AS Delivery as of 09-08-19.xlsx'
# # my_ingest_file = 'tmp_AS Delivery as of 09-20-19.xlsx'
# # my_ingest_file = 'tmp_AS Delivery as of 10-23-19.xlsx'
# my_ingest_file = 'tmp_AS Delivery as of 12-16-19.xlsx'
#
# date_tag = my_ingest_file[-13:-13 + 8]  # Grab the date if any
# date_added = datetime.strptime(date_tag, "%m-%d-%y")
# print(date_tag)
#
# wb, ws = tool.open_wb(my_ingest_path+my_ingest_file)
# my_csv = tool.xlrd_wb_to_csv(wb, ws)
#
#
# my_new_list = []
# last_col = len(my_csv[0])
# for my_row in my_csv:
#     my_row.insert(0, '')
#     my_row.insert(last_col + 1, 'hash')
#     my_row.insert(last_col + 2, date_added)
#     my_new_list.append(my_row)
#
# tool.push_list_to_csv(my_new_list, my_ingest_path+'csv_services.csv')
#
# # tool.load_infile('archive_services_repo', my_ingest_path+'csv_services.csv', delete_rows=True)
# tool.load_infile('archive_services_repo', my_ingest_path+'csv_services.csv', delete_rows=False)
#
#
# exit()