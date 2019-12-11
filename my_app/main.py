import my_app.tool_box as tools


# Use this file to place scripts that are called from views.py
def get_customer():
    print('Hello from main.py')

    # Try creating a Test_Table in the mySQL DB from Models.py
    tools.create_tables("Test_Table")

    # Try retrieving a SmartSheet
    ss_test_list = tools.get_list_from_ss('Tetration SKUs')
    print('Rows in my SmartSheet', len(ss_test_list))

    # Try writing an xlsx file to local storage
    tools.push_list_to_xls(ss_test_list, 'my_test_sheet.xlsx')

    # Try opening an xlsx file from local storage
    xws, wb = tools.open_wb('my_test_sheet.xlsx')
    return ('Hello from Main.py: I read: '+ str(len(ss_test_list)) + ' rows from SmartSheets',ss_test_list)
