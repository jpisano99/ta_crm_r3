import xlrd
import datetime


def xlrd_wb_to_csv(wb, ws):
    #
    # This takes an xlrd worksheet object (wb & ws)
    # and converts it to a simple list for ready to export to csv
    # It takes all XL_CELL_DATE objects and changes to string (MM/DD/YY)
    # It takes all XL_CELL_NUMBER and changes to string
    # It also strips out all Unicode characters above 127
    #
    #
    my_csv_list = []
    # Skip the header
    for my_row in range(1, ws.nrows):
        my_csv_row = []

        for my_col in range(ws.ncols):
            my_cell = ws.cell(my_row, my_col)

            if my_cell.ctype == xlrd.XL_CELL_DATE:
                tmp_val = datetime.datetime(*xlrd.xldate_as_tuple(my_cell.value, wb.datemode))
                my_csv_row.append(tmp_val)

            elif my_cell.ctype == xlrd.XL_CELL_NUMBER:
                tmp_val = str(my_cell.value)
                my_csv_row.append(tmp_val)

            else:
                # Strip out Unicode characters above value 127
                # Make it all ASCII
                cell_bytes = my_cell.value.encode('ascii', 'ignore')
                tmp_val = cell_bytes.decode('utf-8')
                my_csv_row.append(tmp_val)

        my_csv_list.append(my_csv_row)

    return my_csv_list
