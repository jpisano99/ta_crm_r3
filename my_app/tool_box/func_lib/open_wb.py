import xlrd
import os
from my_app.settings import app_cfg


def open_wb(excel_file, run_dir=app_cfg['UPDATES_SUB_DIR']):
    path_to_my_app = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    path_to_run_dir = (os.path.join(path_to_my_app, run_dir))
    path_to_file = os.path.join(path_to_run_dir, excel_file)
    print()
    print('OPENING >>>>>>>>>> ', path_to_file)
    print()

    #
    # Open up excel workbook
    #
    my_wb = xlrd.open_workbook(path_to_file)
    my_ws = my_wb.sheet_by_index(0)

    return my_wb, my_ws


if __name__ == "__main__":
    my_excel = open_wb(app_cfg['BOOKINGS'])
    print('We have: ', my_excel[0], my_excel[1])
