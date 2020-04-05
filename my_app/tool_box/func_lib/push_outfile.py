import os
from my_app.models import *
import csv


def push_outfile(table_name, filter_expression=None, col_names=None, col_headings=None,
                 run_dir='C:/ProgramData/MySQL/MySQL Server 8.0/Uploads'):

    # NOTE: table_name passed in MUST be the name used in models.py
    table_name_lc = table_name.lower()

    # path_to_my_app = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    # path_to_run_dir = (os.path.join(path_to_my_app, run_dir))
    # path_to_file = os.path.join(path_to_run_dir, csv_output)
    path_to_file = run_dir + '/' + table_name_lc + '.csv'
    path_to_tmp_file = run_dir + '/tmp_' + table_name_lc + '.csv'

    if os.path.exists(path_to_file):
        os.remove(path_to_file)

    if os.path.exists(path_to_tmp_file):
        os.remove(path_to_tmp_file)

    print()
    print('PUSHING A LOCAL CSV FILE IN DIRECTORY >>>>>>>>>> ', run_dir)
    print('PUSHING CSV FILE >>>>>>>>>> ', path_to_file)
    print()

    # Were the column names passed in ?
    # Else default to ALL fields for this table
    sql_col_names = ''
    if col_names is None:
        sql_col_names = "*"
        col_names = my_get_column_names(table_name)
    else:
        # Column Names were passed in so just format SQL stmt
        for col_name in col_names:
            sql_col_names = sql_col_names + col_name + ", "
        sql_col_names = sql_col_names[0:len(sql_col_names)-2]

    # If we passed in customer column headings use them else default to the sql names
    if col_headings is None:
        col_headings = []
        if sql_col_names == "*":
            col_headings = my_get_column_names(table_name)
        else:
            # Column Names were passed in so just
            for col_name in col_names:
                col_headings.append(col_name)

    # Was a filter expression passed in ?
    if filter_expression is None:
        my_filter = ''
    else:
        my_filter = "WHERE " + filter_expression + " "

    # Build the SQL Stmnt
    print("SQL Columns Selected >>>>", sql_col_names)
    print("CSV Heading Names >>>>", col_headings)
    print("SQL Filter Stmnt >>>>>>>", my_filter)
    sql = "SELECT " + sql_col_names + " FROM " + table_name + " " + my_filter + \
        "INTO OUTFILE '" + path_to_tmp_file + "' " + \
        "FIELDS ENCLOSED BY '\"' " \
        "TERMINATED BY ',' " \
        "ESCAPED BY '' " \
        "LINES TERMINATED BY '\r\n';"
    db.engine.execute(sql)

    # Read the CSV file of rows we just created
    # and Insert the col_names as Row 0
    with open(path_to_tmp_file, "r") as infile:
        reader = list(csv.reader(infile))
        reader.insert(0, col_headings)

    # Push the full list out as a proper CSV
    with open(path_to_file, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        for line in reader:
            writer.writerow(line)

    os.remove(path_to_tmp_file)
    return


def my_get_column_names(table_name, my_db_name="ta_adoption_db"):
    table_name_lc = table_name.lower()
    my_columns = []

    # Get column names
    sql = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS`" + \
          "WHERE `TABLE_SCHEMA`= '" + my_db_name + "' " + \
          "AND `TABLE_NAME`='" + table_name_lc + "';"
    sql_results = db.engine.execute(sql)
    for x in sql_results:
        my_columns.append(x[0])

    return my_columns

if __name__ == "__main__" and __package__ is None:
    # push_outfile('test_table')
    # push_outfile('Archive_Bookings_Repo', "date_added = '2020-02-03'")
    push_outfile('Archive_Telemetry_Repo', "date_added > '2020-01-01'", None,
                 ['id', 'type', 'My Customer', 'erp_cust_id', 'Sales Order', 'sub_id', 'start_date', 'name', 'vrf',
                  'licensed', 'installed', 'inactive', 'autoupg', 'windows', 'linux', 'aix', 'lightwt', 'legacy',
                  'deepvis', 'enforce', 'enforce_enabled', 'pid_enabled', 'forensics_enabled', 'inventory',
                  'anyconnect', 'anyproxy', 'erspan', 'f5', 'netflow', 'netscaler', 'others', 'hash_value',
                  'date_added'])
    # push_outfile('Archive_Bookings_Repo', 'date_added', '2019-06-27')
    # # push_outfile('Archive_Bookings_Repo')
    # push_outfile('Archive_Subscriptions_Repo')
    # push_outfile('Archive_Services_Repo')
    # push_outfile('Archive_Telemetry_Repo')
    # push_outfile('Bookings')
