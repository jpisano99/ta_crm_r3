import os
from my_app.models import *
import csv


def push_outfile(table_name, filter_field=None, filter_value=None,
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

    # Collect the column names for this table
    col_names = []
    for x in eval(table_name).__table__.columns:
        col_names.append(x.name)

    if filter_field is None:
        my_filter = ''
    else:
        my_filter = "WHERE " + filter_field + "='" + filter_value + "' "

    sql = "SELECT * FROM " + table_name + " " + my_filter + \
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
        reader.insert(0, col_names)

    # Push the full list out as a proper CSV
    with open(path_to_file, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        for line in reader:
            writer.writerow(line)

    os.remove(path_to_tmp_file)
    return


if __name__ == "__main__" and __package__ is None:
    push_outfile('Archive_Bookings_Repo', 'date_added', '2019-06-27')
    # push_outfile('Archive_Bookings_Repo')
    push_outfile('Archive_Subscriptions_Repo')
    push_outfile('Archive_Services_Repo')
    push_outfile('Archive_Telemetry_Repo')
    push_outfile('Bookings')
