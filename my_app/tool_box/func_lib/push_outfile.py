from my_app import db
from my_app.models import Telemetry, Archive_Telemetry_Repo, Archive_Bookings_Repo
import os
from my_app import db
from my_app.settings import app_cfg, db_config
from my_app.models import *
import csv


def load_infile(table_name, csv_output, filter_field=None, filter_value=None, run_dir='C:/ProgramData/MySQL/MySQL Server 8.0/Uploads'):

    # path_to_my_app = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    # path_to_run_dir = (os.path.join(path_to_my_app, run_dir))
    # path_to_file = os.path.join(path_to_run_dir, csv_output)
    path_to_file = run_dir + '/' + csv_output
    path_to_file1 = run_dir + '/headers.csv'

    print()
    print('PUSHING A LOCAL CSV FILE IN DIRECTORY >>>>>>>>>> ', run_dir)
    print('PUSHING CSV FILE >>>>>>>>>> ', csv_output)
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
        "INTO OUTFILE '" + path_to_file + "' " + \
        "FIELDS ENCLOSED BY '\"' " \
        "TERMINATED BY ',' " \
        "ESCAPED BY '' " \
        "LINES TERMINATED BY '\r\n';"
    sql_results = db.engine.execute(sql)

    with open(path_to_file, "r") as infile:
        reader = list(csv.reader(infile))
        reader.insert(0, col_names)

    with open(path_to_file1, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        for line in reader:
            writer.writerow(line)

    return


if __name__ == "__main__" and __package__ is None:
    # load_infile('archive_bookings_repo', 'my_csv.csv', 'date_added', '2019-06-27')
    # load_infile('Archive_Bookings_Repo', 'my_csv.csv')
    load_infile('Archive_Telemetry_Repo', 'my_csv1.csv')

