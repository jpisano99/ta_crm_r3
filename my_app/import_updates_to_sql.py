from my_app.settings import app_cfg
import datetime
import my_app.tool_box as tool
import time
import os
import json


def import_updates_to_sql():
    # tool.create_tables("Customer_Ids")
    # tool.create_tables("Sales_Orders")

    tool.create_tables()

    # Fetch Time Stamp info
    home = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    run_dir = app_cfg['UPDATES_SUB_DIR']
    path_to_run_dir = (os.path.join(home, run_dir))

    # Read the config_dict.json file
    with open(os.path.join(path_to_run_dir, app_cfg['META_DATA_FILE'])) as json_input:
        config_dict = json.load(json_input)
    date_tag = config_dict['data_time_stamp']
    now = datetime.datetime.strptime(date_tag, "%m-%d-%y")

    #
    # Import Delivery
    #
    wb, ws = tool.open_wb(app_cfg['XLS_AS_DELIVERY_STATUS'])
    my_csv = tool.xlrd_wb_to_csv(wb, ws)

    my_new_list = []
    last_col = len(my_csv[0])
    for my_row in my_csv:
        my_row.insert(0, '')
        my_row.insert(last_col+1, 'hash')
        my_row.insert(last_col+2, now)

        my_new_list.append(my_row)

    tool.push_list_to_csv(my_new_list, 'csv_services.csv')
    tool.load_infile('services', 'csv_services.csv', delete_rows=True)

    #
    # Import Subscriptions
    #
    wb, ws = tool.open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
    my_csv = tool.xlrd_wb_to_csv(wb, ws)

    my_new_list = []
    last_col = len(my_csv[0])
    for my_row in my_csv:
        my_row.insert(0, '')
        my_row.insert(last_col+1, 'jim')
        my_row.insert(last_col+2, now)
        my_new_list.append(my_row)

    tool.push_list_to_csv(my_new_list, 'csv_subscriptions.csv')
    tool.load_infile('subscriptions', 'csv_subscriptions.csv', delete_rows=True)

    #
    # Import Telemetry
    #
    # CREATE TABLE ta_adoption_db.telemetry_repo  LIKE ta_adoption_db.telemetry;
    wb, ws = tool.open_wb(app_cfg['XLS_TELEMETRY'])
    my_csv = tool.xlrd_wb_to_csv(wb, ws)

    my_new_list = []
    last_col = len(my_csv[0])
    for my_row in my_csv:
        my_row.insert(0, '')
        my_row.insert(last_col+1, 'hash')
        my_row.insert(last_col+2, now)
        my_new_list.append(my_row)

    tool.push_list_to_csv(my_new_list, 'csv_telemetry.csv')
    tool.load_infile('telemetry', 'csv_telemetry.csv', delete_rows=True)

    #
    # Import Bookings
    #
    wb, ws = tool.open_wb(app_cfg['XLS_BOOKINGS'])
    my_csv = tool.xlrd_wb_to_csv(wb, ws)

    my_new_list = []
    last_col = len(my_csv[0])

    for my_row in my_csv:
        # Add some useful columns
        my_row.insert(0, '')
        my_row.insert(last_col+1, 'hash')
        my_row.insert(last_col+2, now)

        my_new_list.append(my_row)

    tool.push_list_to_csv(my_new_list, 'csv_bookings.csv')
    tool.load_infile('bookings', 'csv_bookings.csv', delete_rows=True)

    return "SQL Data Loaded"


if __name__ == "__main__" and __package__ is None:
    import_updates_to_sql()