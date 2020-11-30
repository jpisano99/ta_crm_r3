import my_app.tool_box as tool
import os
from my_app.settings import app_cfg


def scrub_fy20_coverage():
    # Get the Tetration Specialists
    wb, ws = tool.open_wb('ldap_users.xlsx')
    tet_tsa_list = []
    for x in range(1, ws.nrows):
        ws.cell_value(x, 10)
        if ws.cell_value(x, 10) == 'Tetration':
            tet_tsa_list.append(ws.cell_value(x, 4))

    # file_name = "TA Services Bookings with SO as of 11-23-20"

    file_name = 'global_coverage'
    home = (app_cfg['UPDATES_SUB_DIR'])
    my_dir = "FY20_Coverage"
    my_path = os.path.join(home, my_dir)
    print('my path >>> ', os.path.join(home, my_dir))

    my_wb, my_ws = tool.open_wb(file_name + '.xlsx', my_path)

    ws_americas = my_wb.sheet_by_name('Americas')
    ws_emear = my_wb.sheet_by_name('EMEAR')

    print(ws_americas.nrows)
    print(ws_emear.nrows)

    coverage_dict = {}

    for row in range(1, ws_americas.nrows):
        if ws_americas.cell_value(row, 27) != '':

            node_id = str(int(ws_americas.cell_value(row, 0)))
            sls_lev_1 = ws_americas.cell_value(row, 9)
            sls_lev_2 = ws_americas.cell_value(row, 10)
            sls_lev_3 = ws_americas.cell_value(row, 11)
            sls_lev_4 = ws_americas.cell_value(row, 12)
            sls_lev_5 = ws_americas.cell_value(row, 13)
            sls_lev_6 = ws_americas.cell_value(row, 14)

            css = ws_americas.cell_value(row, 20)
            tsa = ws_americas.cell_value(row, 21)
            swan_css = ws_americas.cell_value(row, 27)
            swan_tsa = ws_americas.cell_value(row, 28)

            tet_tsa = ''
            for tet_tsa in tet_tsa_list:
                if swan_tsa.find(tet_tsa) != -1:
                    break
                else:
                    tet_tsa = ''

            coverage_dict[node_id]=[sls_lev_1, sls_lev_2, sls_lev_3, sls_lev_4, sls_lev_5, sls_lev_6,
                                    css, tsa,
                                    swan_css, swan_tsa, tet_tsa]

            # print(node_id, coverage_dict[node_id])

    for row in range(1, ws_emear.nrows):
        if ws_emear.cell_value(row, 26) != '':

            node_id = str(int(ws_emear.cell_value(row, 1)))
            sls_lev_1 = ws_emear.cell_value(row, 4)
            sls_lev_2 = ws_emear.cell_value(row, 5)
            sls_lev_3 = ws_emear.cell_value(row, 6)
            sls_lev_4 = ws_emear.cell_value(row, 7)
            sls_lev_5 = ws_emear.cell_value(row, 8)
            sls_lev_6 = ws_emear.cell_value(row, 9)

            css = ws_emear.cell_value(row, 19)
            tsa = ws_emear.cell_value(row, 20)
            swan_css = ws_emear.cell_value(row, 26)
            swan_tsa  = ws_emear.cell_value(row, 27)

            tet_tsa = ''
            for tet_tsa in tet_tsa_list:
                if swan_tsa.find(tet_tsa) != -1:
                    break
                else:
                    tet_tsa = ''

            coverage_dict[node_id]=[sls_lev_1, sls_lev_2, sls_lev_3, sls_lev_4, sls_lev_5, sls_lev_6,
                                    css, tsa,
                                    swan_css, swan_tsa, tet_tsa]

    coverage_list = [['node_id',
                      'sales_level_1', 'sales_level_2', 'sales_level_3',
                      'sales_level_4', 'sales_level_5', 'sales_level_6',
                      'css', 'tsa', 'swan_css', 'swan_tsa', 'tetration tsa']]

    for k, v in coverage_dict.items():
        tmp_list = v
        tmp_list.insert(0, k)
        coverage_list.append(tmp_list)

    tool.push_list_to_xls(coverage_list, 'swan_coverage.xlsx')
    print (len(coverage_dict))
    print(my_path)
    return


if __name__ == "__main__" and __package__ is None:
    scrub_fy20_coverage()
    exit()
