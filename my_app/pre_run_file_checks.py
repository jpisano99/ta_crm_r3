import os
import json
import time
import xlrd
import pprint
from datetime import datetime
from my_app.settings import app_cfg
import my_app.tool_box as tool


def get_cust_name(ws, short_name):

    return


def pre_run_file_checks(run_dir=app_cfg['UPDATES_SUB_DIR']):
    pp = pprint.PrettyPrinter(indent=4, depth=2)
    home = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    working_dir = app_cfg['WORKING_SUB_DIR']
    update_dir = app_cfg['UPDATES_SUB_DIR']
    archive_dir = app_cfg['ARCHIVES_SUB_DIR']

    # Check that all key directories exist
    path_to_main_dir = (os.path.join(home))
    if not os.path.exists(path_to_main_dir):
        print(path_to_main_dir, "MAIN_DIR does NOT Exist !")
        exit()

    path_to_run_dir = (os.path.join(home, run_dir))
    if not os.path.exists(path_to_run_dir):
        print(path_to_run_dir, " WORKING_DIR does NOT Exist !")
        exit()

    path_to_updates = (os.path.join(home, update_dir))
    if not os.path.exists(path_to_updates):
        print(path_to_updates, "UPDATES_SUB_DIR does NOT Exist !")
        exit()

    path_to_archives = (os.path.join(home, archive_dir))
    if not os.path.exists(path_to_archives):
        print(path_to_archives, "ARCHIVE_SUB_DIR does NOT Exist !")
        exit()

    # OK directories are there any files ?
    if not os.listdir(path_to_run_dir):
        print('Directory', path_to_run_dir, 'contains NO files')
        exit()

    #  Get the required Files to begin processing from app_cfg (settings.py)
    files_needed = {}
    # Do we have RAW files to process ?
    for var in app_cfg:
        if var.find('RAW') != -1:
            # Look for any config var containing the word 'RAW' and assume they are "Missing'
            files_needed[app_cfg[var]] = 'Missing'

    # See if we have the files_needed are there and they have consistent dates (date_list)
    run_files = os.listdir(path_to_run_dir)
    date_list = []
    for file_needed, status in files_needed.items():
        for run_file in run_files:
            date_tag = run_file[-13:-13 + 8]  # Grab the date if any
            run_file = run_file[:len(run_file)-14]  # Grab the name without the date
            if run_file == file_needed:
                date_list.append(date_tag)  # Grab the date
                files_needed[file_needed] = 'Found'
                break

    # All time stamps the same ?
    base_date = date_list[0]
    for date_stamp in date_list:
        if date_stamp != base_date:
            print('ERROR: Inconsistent date stamp(s) found')
            exit()

    # Do we have all the files we need ?
    for file_name, status in files_needed.items():
        if status != 'Found':
            print("ERROR: Filename ", "'"+file_name, "MM-DD-YY'  is missing from directory", "'"+run_dir+"'")
            exit()

    # Read the config_dict.json file
    try:
        with open(os.path.join(path_to_run_dir, app_cfg['META_DATA_FILE'])) as json_input:
            config_dict = json.load(json_input)
        print(config_dict)
        print(type(config_dict))
        print(config_dict['last_run_dir'])
    except:
        print('No config_dict file found.')

    # Since we have a consistent date then Create the json file for config_data.json.
    # Put the time_stamp in it
    config_dict = {'data_time_stamp': base_date,
                   'last_run_dir': path_to_run_dir,
                   'files_scrubbed': 'never'}
    with open(os.path.join(path_to_run_dir, app_cfg['META_DATA_FILE']), 'w') as json_output:
        json.dump(config_dict, json_output)

    # Delete all previous tmp_ files
    for file_name in run_files:
        if file_name[0:4] == 'tmp_':
            os.remove(os.path.join(path_to_run_dir, file_name))

    # Here is what we have - All things should be in place
    print('Our directories:')
    print('\tPath to Main Dir:', path_to_main_dir)
    print('\tPath to Updates Dir:', path_to_updates)
    print('\tPath to Archives Dir:', path_to_archives)
    print('\tPath to Run Dir:', path_to_run_dir)

    # Process the RAW data (Renewals and Bookings)
    # Clean up rows, combine multiple Bookings files, add custom table names
    processing_date = date_list[0]
    file_paths = []
    bookings = []
    bookings_header_flag = False
    subscriptions_header_flag = False
    subscriptions = []
    as_status = []
    telemetry_spock = []
    telemetry_strom = []
    saas_lookup = {}
    print()
    print('We are processing files:')

    # We need to make a sku_filter_dict here
    tmp_dict = tool.build_sku_dict()
    sku_filter_dict = {}
    for key, val in tmp_dict.items():
        if val[0] == 'Service':
            sku_filter_dict[key] = val

    # Main loop to process files
    for file_name in files_needed:
        file_path = file_name + ' ' + processing_date + '.xlsx'
        file_path = os.path.join(path_to_run_dir, file_path)

        file_paths.append(file_path)

        my_wb, my_ws = tool.open_wb(file_name + ' ' + processing_date + '.xlsx', run_dir)
        print('\t\t', file_name + '', processing_date + '.xlsx', ' has ', my_ws.nrows,
              ' rows and ', my_ws.ncols, 'columns')

        if file_name.find('Bookings') != -1:
            # For the Bookings start_row is here
            # This header flag tells us we have been here once already
            # So we need to skip the header row
            if bookings_header_flag is False:
                start_row = 3
                bookings_header_flag = True
            else:
                start_row = 4
            start_col = 1
            for row in range(start_row, my_ws.nrows):
                bookings.append(my_ws.row_slice(row, start_col))

        elif file_name.find('Subscriptions') != -1:
            # # For the Subscriptions start_row is here
            # # We are merging the EA's and Regular Subscriptions
            # # This header flag tells us we have been here once already
            # # So we need to skip the header row
            if subscriptions_header_flag is False:
                start_row = 0
                subscriptions_header_flag = True
            else:
                start_row = 1
            start_col = 0
            for row in range(start_row, my_ws.nrows):
                subscriptions.append(my_ws.row_slice(row, start_col))

        elif file_name.find('SPOCK_sensor_sum') != -1:
            # This raw sheet starts on row num 0
            for row in range(0, my_ws.nrows):
                # Look for these rows and strip out
                if (my_ws.cell_value(row, 0).find('spock') != -1)or \
                   (my_ws.cell_value(row, 0) == 'Default'):
                    continue
                else:
                    telemetry_spock.append(my_ws.row_slice(row))

        elif file_name.find('STROM_sensor_sum') != -1:
            # This raw sheet starts on row num 0
            for row in range(0, my_ws.nrows):
                # Look for these rows and strip out
                if (my_ws.cell_value(row, 0).find('strom') != -1) or (my_ws.cell_value(row, 0) == 'Default'):
                    continue
                else:
                    telemetry_strom.append(my_ws.row_slice(row))

        elif file_name.find('AS Delivery Status') != -1:
            # This AS-F raw sheet starts on row num 0
            # Grab the header row
            as_status.append(my_ws.row_slice(0))
            for row in range(1, my_ws.nrows):
                # Check to see if this is a TA SKU
                if my_ws.cell_value(row, 14) in sku_filter_dict:
                    as_status.append(my_ws.row_slice(row))

        elif file_name.find('SaaS Customer Tracking') != -1:
            # Build this index for matching the SaaS Tracker with telemetry data
            for row in range(1, my_ws.nrows):
                tmp_cust_name = my_ws.cell_value(row, 2)
                tmp_cust_id = my_ws.cell_value(row, 3)
                tmp_saas_name = my_ws.cell_value(row, 4)
                tmp_saas_vrf = my_ws.cell_value(row, 5)
                tmp_saas_so = my_ws.cell_value(row, 6)
                tmp_saas_start_date = my_ws.cell_value(row, 7)
                if tmp_saas_name == '':
                    tmp_saas_name = 'Not Yet Provisioned'
                saas_lookup[tmp_saas_name] = [tmp_cust_name, tmp_saas_vrf, tmp_cust_id,
                                              tmp_saas_so, tmp_saas_start_date]

    #
    # All raw data now read in
    #

    # Start scrubbing the raw data
    # Scrub Subscriptions
    # For the Subscriptions sheet we need to convert
    # col 9 & 11 to DATE from STR
    # col 13 (monthly rev) to FLOAT from STR
    #
    subscriptions_scrubbed = []
    for row_num, my_row in enumerate(subscriptions):
        my_new_row = []

        for col_num, my_cell in enumerate(my_row):
            if row_num == 0:
                # Is this the header row ?
                my_new_row.append(my_cell.value)
                continue
            if col_num == 9 or col_num == 11:
                tmp_val = datetime.strptime(my_cell.value, '%d %b %Y')
                # tmp_val = datetime.strptime(my_cell.value, '%m/%d/%Y')
            elif col_num == 13:
                tmp_val = my_cell.value
                try:
                    tmp_val = float(tmp_val)
                except ValueError:
                    tmp_val = 0
            else:
                tmp_val = my_cell.value

            my_new_row.append(tmp_val)
        subscriptions_scrubbed.append(my_new_row)

    #
    # Now Scrub AS Delivery Info
    #
    as_status_scrubbed = []
    for row_num, my_row in enumerate(as_status):
        my_new_row = []
        for col_num, my_cell in enumerate(my_row):
            if row_num == 0:
                # Is this the header row ?
                my_new_row.append(my_cell.value)
                continue
            if col_num == 0:  # PID
                tmp_val = str(int(my_cell.value))
            elif col_num == 19:  # SO Number
                tmp_val = str(int(my_cell.value))
            elif col_num == 26 and my_cell.ctype == xlrd.XL_CELL_DATE:  # Project Start Date
                tmp_val = datetime(*xlrd.xldate_as_tuple(my_cell.value, my_wb.datemode))
            elif col_num == 27 and my_cell.ctype == xlrd.XL_CELL_DATE:  # Scheduled End Date
                tmp_val = datetime(*xlrd.xldate_as_tuple(my_cell.value, my_wb.datemode))
            elif col_num == 28 and my_cell.ctype == xlrd.XL_CELL_DATE:  # Project Creation Date
                tmp_val = datetime(*xlrd.xldate_as_tuple(my_cell.value, my_wb.datemode))
            else:
                tmp_val = my_cell.value

            my_new_row.append(tmp_val)
        as_status_scrubbed.append(my_new_row)

    #
    # Now Scrub Bookings Data
    #
    bookings_scrubbed = []
    for row_num, my_row in enumerate(bookings):
        my_new_row = []
        for col_num, my_cell in enumerate(my_row):
            if row_num == 0:
                # Is this the header row ?
                my_new_row.append(my_cell.value)
                continue

            if col_num == 0 or col_num == 2 or \
                    col_num == 11:  # Fiscal Year / Fiscal Period / SO Num
                tmp_val = str(int(my_cell.value))
            elif col_num == 15:  # Customer ID
                try:
                    tmp_val = str(int(my_cell.value))
                except ValueError:
                    tmp_val = '-999'
            elif col_num == 12:  # Web Order Num
                try:
                    tmp_val = str(int(my_cell.value))
                except ValueError:
                    tmp_val = 'UNKNOWN'
            else:
                tmp_val = my_cell.value

            my_new_row.append(tmp_val)
        bookings_scrubbed.append(my_new_row)

    #
    # Scrub the Telemetry sheets
    # Merge the telemetry sheets and ADD a column
    # First the DR SPOCK List
    #
    telemetry_scrubbed = []
    time_stamp = datetime.strptime(processing_date, '%m-%d-%y')
    for row_num, my_row in enumerate(telemetry_spock):
        my_new_row = []
        tmp_cust_name = ''
        tmp_cust_id = ''
        tmp_saas_start_date = ''
        tmp_saas_so = ''
        tmp_sub_id = ''
        for col_num, my_cell in enumerate(my_row):
            if row_num == 0:
                tmp_val = my_cell.value
            else:
                if col_num >= 1:
                    tmp_val = int(my_cell.value)
                else:
                    # This is column 0 which has the SaaS platform customer short name
                    tmp_val = my_cell.value
                    if tmp_val in saas_lookup:
                        tmp_cust_name = saas_lookup[tmp_val][0]
                        try:
                            tmp_saas_so = str(int(saas_lookup[tmp_val][3]))
                        except:
                            tmp_saas_so = str(saas_lookup[tmp_val][3])

                        # Format the Customer ID and Start Date
                        if saas_lookup[tmp_val][2] != '':
                            tmp_cust_id = int(saas_lookup[tmp_val][2])
                        else:
                            tmp_cust_id = saas_lookup[tmp_val][2]

                        if saas_lookup[tmp_val][4] != '':
                            tmp_saas_start_date = saas_lookup[tmp_val][4]
                            tmp_saas_start_date = datetime(*xlrd.xldate_as_tuple(tmp_saas_start_date, my_wb.datemode))
                        else:
                            tmp_saas_start_date = saas_lookup[tmp_val][4]

            my_new_row.append(tmp_val)

        # saas_lookup[tmp_saas_name] = [tmp_cust_name, tmp_saas_vrf, tmp_cust_id,
        #                               tmp_saas_so, tmp_saas_start_date]

        # Put in a header row
        if row_num == 0:
            # my_new_row.insert(0, 'As_of')
            my_new_row.insert(1, 'Type')
            my_new_row.insert(2, 'Customer Name')
            my_new_row.insert(3, 'Customer ID')
            my_new_row.insert(4, 'Sales Order')
            my_new_row.insert(5, 'Subscription ID')
            my_new_row.insert(6, 'Start Date Requested')

        else:
            # my_new_row.insert(0, time_stamp)
            my_new_row.insert(0, 'DR')
            my_new_row.insert(1, tmp_cust_name)
            my_new_row.insert(2, tmp_cust_id)
            my_new_row.insert(3, tmp_saas_so)
            my_new_row.insert(4, tmp_sub_id)
            my_new_row.insert(5, tmp_saas_start_date)
        telemetry_scrubbed.append(my_new_row)

    # Now do the Non-DR STROM list
    for row_num, my_row in enumerate(telemetry_strom):
        if row_num == 0:
            continue
        my_new_row = []
        tmp_cust_name = ''
        tmp_cust_id = ''
        tmp_saas_start_date = ''
        tmp_sub_id = ''
        tmp_saas_so = ''
        for col_num, my_cell in enumerate(my_row):
            if col_num >= 1:
                tmp_val = int(my_cell.value)
            else:
                # This is column 0 which has the SaaS platform customer short name
                tmp_val = my_cell.value
                if tmp_val in saas_lookup:
                    tmp_cust_name = saas_lookup[tmp_val][0]
                    try:
                        tmp_saas_so = str(int(saas_lookup[tmp_val][3]))
                    except:
                        tmp_saas_so = str(saas_lookup[tmp_val][3])

                    # Format the Customer ID and Start Date
                    if saas_lookup[tmp_val][2] != '':
                        tmp_cust_id = int(saas_lookup[tmp_val][2])
                    else:
                        tmp_cust_id = saas_lookup[tmp_val][2]

                    if saas_lookup[tmp_val][4] != '':
                        tmp_saas_start_date = saas_lookup[tmp_val][4]
                        tmp_saas_start_date = datetime(*xlrd.xldate_as_tuple(tmp_saas_start_date, my_wb.datemode))
                    else:
                        tmp_saas_start_date = saas_lookup[tmp_val][4]
            my_new_row.append(tmp_val)

        # my_new_row.insert(0, time_stamp)
        my_new_row.insert(0, 'Non-DR')
        my_new_row.insert(1, tmp_cust_name)
        my_new_row.insert(2, tmp_cust_id)
        my_new_row.insert(3, tmp_saas_so)
        my_new_row.insert(4, tmp_sub_id)
        my_new_row.insert(5, tmp_saas_start_date)
        telemetry_scrubbed.append(my_new_row)

    #
    # Push the lists out to an Excel File
    #
    tool.push_list_to_xls(telemetry_scrubbed, app_cfg['XLS_TELEMETRY'], run_dir, 'ta_telemetry')
    tool.push_list_to_xls(bookings_scrubbed, app_cfg['XLS_BOOKINGS'], run_dir, 'ta_bookings')
    tool.push_list_to_xls(subscriptions_scrubbed, app_cfg['XLS_SUBSCRIPTIONS'], run_dir, 'ta_subscriptions')
    tool.push_list_to_xls(as_status_scrubbed, app_cfg['XLS_AS_DELIVERY_STATUS'], run_dir, 'ta_delivery')
    # push_xlrd_to_xls(as_status, app_cfg['XLS_AS_DELIVERY_STATUS'], run_dir, 'ta_delivery')

    print('We have ', len(bookings), 'bookings line items')
    print('We have ', len(telemetry_scrubbed), 'telemetry line items')
    print('We have ', len(as_status), 'AS-Fixed SKU Delivery line items')
    print('We have ', len(subscriptions), 'subscription line items')
    msg = 'We have ' + str(len(bookings)) + ' bookings line items'

    with open(os.path.join(path_to_run_dir, app_cfg['META_DATA_FILE'])) as json_input:
        config_dict = json.load(json_input)
    config_dict['files_scrubbed'] = 'phase_1'
    with open(os.path.join(path_to_run_dir, app_cfg['META_DATA_FILE']), 'w') as json_output:
        json.dump(config_dict, json_output)

    print('pre run file checks DONE!')
    return msg


if __name__ == "__main__" and __package__ is None:
    pre_run_file_checks()
    exit()
