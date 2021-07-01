from my_app.tool_box.ss_lib.Ssheet_class import Ssheet
from my_app.settings import app_cfg

#
# Create a dict called team_dict from the coverage smartsheet
#


def build_coverage_dict():
    # Create an object from SmartSheets
    coverage = app_cfg['SS_COVERAGE']
    my_coverage = Ssheet(coverage)
    team_dict = {}

    # Get Col Names for SmartSheet Coverage map as keys
    # Iterate across each SmartSheet row
    for row in my_coverage.rows:
        swan_css = ''
        tetration_tsa = ''
        my_sales_level = ''

        for col_name, row_data in zip(my_coverage.col_name_idx.keys(), row['cells']):
            this_cell_value = ''

            # Check if the SmartSheet cell has a value
            if 'value' in row_data.keys():
                this_cell_value = row_data['value']

                if col_name == 'swan_css':
                    swan_css = row_data['value']
                elif col_name == 'tetration_tsa':
                    tetration_tsa = row_data['value']

            if col_name.find('sales_level_') != -1:
                my_sales_level = my_sales_level + this_cell_value + ','

        my_sales_level = my_sales_level.rstrip(',')
        team_dict[my_sales_level] = {'swan_css': swan_css, 'tetration_tsa': tetration_tsa}

    print(len(team_dict))
    return team_dict
