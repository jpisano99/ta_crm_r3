import csv
import os
# from my_app.func_lib.db_tools import create_tables
# from my_app.func_lib.open_wb import open_wb
# from my_app.func_lib.xlrd_wb_to_csv import xlrd_wb_to_csv
# from my_app.func_lib.xlrd_wb_to_list import xlrd_wb_to_list
# from my_app.func_lib.push_list_to_xls import push_list_to_xls

from my_app.settings import app_cfg


def push_list_to_csv(my_list, csv_output, run_dir=app_cfg['UPDATES_SUB_DIR'], tbl_name='table1'):
    path_to_my_app = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    path_to_run_dir = (os.path.join(path_to_my_app, run_dir))
    path_to_file = os.path.join(path_to_run_dir, csv_output)
    print()
    print('CREATING IN DIRECTORY >>>>>>>>>> ', path_to_run_dir)
    print('CREATING SHEET >>>>>>>>>> ', csv_output)
    print()

    # for x, my_row in enumerate(my_list):
    with open(path_to_file, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(my_list)

    writeFile.close()
    return


if __name__ == "__main__" and __package__ is None:
    # wb, ws = open_wb(app_cfg['XLS_BOOKINGS'])
    # # wb, ws = open_wb(app_cfg['XLS_AS_DELIVERY_STATUS'])
    # # wb, ws = open_wb(app_cfg['XLS_SUBSCRIPTIONS'])
    # create_tables('Bookings')
    #
    # my_csv_list = xlrd_wb_to_csv(wb, ws)
    # my_list = xlrd_wb_to_list(wb, ws)
    #
    # print(len(my_csv_list))
    # print(len(my_list))
    #
    # push_list_to_xls(my_list, 'my_xls.xlsx')
    # push_list_to_csv(my_csv_list, 'my_csv.csv')

    exit()

