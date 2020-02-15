import xlsxwriter
import datetime
import os
from my_app.settings import app_cfg


def push_list_to_xls(my_list, excel_file, run_dir=app_cfg['UPDATES_SUB_DIR'], tbl_name='table1'):
    path_to_my_app = os.path.join(app_cfg['HOME'], app_cfg['MOUNT_POINT'], app_cfg['MY_APP_DIR'])
    path_to_run_dir = (os.path.join(path_to_my_app, run_dir))
    path_to_file = os.path.join(path_to_run_dir, excel_file)
    print()
    print('CREATING IN DIRECTORY >>>>>>>>>> ', path_to_run_dir)
    print('CREATING SHEET >>>>>>>>>> ', excel_file)
    print()

    # def push_list_to_xls(my_list, xls_file, xls_time=app_cfg['PROD_DATE']):
    #
    # Get settings for file locations and names
    #

    #
    # Write the Excel File
    #
    workbook = xlsxwriter.Workbook(path_to_file)
    worksheet = workbook.add_worksheet()

    # cell_format = workbook.add_format()
    # cell_format.set_bold()
    # cell_format.set_bg_color('#B7FFF9')
    #
    # cell_format.set_bg_color('#B7D9FF')
    # cell_format.set_bg_color('#FFFEB7')
    # # cell_format.set_font_color('red')

    xls_money = workbook.add_format({'num_format': '$#,##0'})
    xls_pct = workbook.add_format({'num_format': '0.0%'})
    xls_date = workbook.add_format({'num_format': 'mm / dd/ yyyy'})

    for row_num, my_row in enumerate(my_list):
        for col_num, cell_val in enumerate(my_row):
            # What type of cell are we writing ?
            if type(cell_val) is float:
                # ANY float will be written as a dollar format
                worksheet.write(row_num, col_num, cell_val, xls_money)
            elif type(cell_val) is int:
                # Just a plain old int
                worksheet.write(row_num, col_num, cell_val)
            elif isinstance(cell_val, datetime.datetime):
                # A python datetime
                worksheet.write(row_num, col_num, cell_val, xls_date)
            else:
                # Looks like we have a string type
                # Look for a format indicator (_%_ for pct)
                # Generic format to write a cell worksheet.write(row_num, col_num, cell_val, cell_format)
                if cell_val.find('_%_') != -1:
                    cell_val = float(cell_val.replace('_%_', '',))
                    worksheet.write(row_num, col_num, cell_val, xls_pct)
                elif cell_val.find('_non$_') != -1:
                    # Looks like we have a non dollar float
                    cell_val = float(cell_val.replace('_non$_', '',))
                    worksheet.write(row_num, col_num, cell_val)
                else:
                    # Just write whatever string we have no format specified
                    worksheet.write(row_num, col_num, cell_val)

    # Prep the header row for our table
    header_row = my_list[0]
    col_list = []
    for col_name in header_row:
        col_desc = {'header': col_name}
        col_list.append(col_desc)

    # Make a table of our data (handy for PowerBI
    worksheet.add_table(0, 0, row_num, col_num, {'header_row': True,
                                                     'name': tbl_name,
                                                     'columns': col_list})

    workbook.close()
    return
