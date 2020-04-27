import xlrd
from my_app.settings import app_cfg

import my_app.tool_box as tool


def gather_mailer_data(mailer_xlsx, job_title):
    mail_wb, mail_ws = tool.open_wb(mailer_xlsx)

    mailer_dict = {}
    rm_dict = {}
    emp_list = []
    nickname = "No Nickname"
    last_row = mail_ws.nrows
    row_skip = False

    for row in range(1, mail_ws.nrows):
        current_row = row
        next_row = current_row + 1

        if row_skip:
            row_skip = False
            continue

        if next_row == last_row:
            # Do NOT check for a nickname
            nickname_check = False
        else:
            # Check for a nickname
            nickname_check = True

        if nickname_check:
            if mail_ws.cell_value(row + 1, 0) == '':
                nickname = mail_ws.cell_value(row + 1, 3)
                row_skip = True
        else:
            nickname = "No Nickname"
            row_skip = False

        try:
            emp_id = str(int(mail_ws.cell_value(row, 2)))
        except:
            emp_id = mail_ws.cell_value(row, 2)

        username = mail_ws.cell_value(row, 1).rstrip()
        email = username+'@cisco.com'
        fname = mail_ws.cell_value(row, 3).capitalize()
        lname = mail_ws.cell_value(row, 4).capitalize()
        manager_id = mail_ws.cell_value(row, 7).rstrip()
        dept = mail_ws.cell_value(row, 9).rstrip()

        if nickname != "No Nickname":
            nickname = nickname.replace('(', '', 1)
            nickname = nickname.replace(')', '', 1).capitalize()

        # print(row, emp_id, username, email, '/', lname + ', ' + fname, '/', nickname, fname, lname, manager_id)

        if dept.find('Tetration') != -1 or dept.find('Workload') != -1:
            mailer_dict[emp_id] = {
                'username': username,
                'email': email,
                'job_title': job_title,
                'dept': dept,
                'fname': fname,
                'nickname': nickname,
                'lname': lname,
                'manager_id': manager_id,
            }

        rm_dict[manager_id] = emp_list.append([mailer_dict])
    # print(rm_dict)
    return (mailer_dict)


if __name__ == "__main__" and __package__ is None:
    ta_mailer = {}
    my_mailer = gather_mailer_data('jchristo-mailer as of 04-25-20.xlsx', 'TSA')
    ta_mailer.update(my_mailer)
    print(len(ta_mailer))
    print(my_mailer['2665'])

    my_mailer = gather_mailer_data('micashma-mailer as of 04-25-20.xlsx', 'PSS')
    ta_mailer.update(my_mailer)
    print(len(ta_mailer))
    print(my_mailer['164409'])

    my_mailer = gather_mailer_data('rhinson-mailer as of 04-25-20.xlsx', 'PSS')
    ta_mailer.update(my_mailer)
    print(len(ta_mailer))
    print(my_mailer['69741'])

    my_list = [['emp id', 'username', 'email', 'full name', 'manager', 'dept', 'job title']]
    for k, v in ta_mailer.items():
        print(k, v['username'], v['dept'], v['job_title'])
        my_list.append([k, v['username'], v['email'], v['lname']+', '+v['fname'], v['manager_id'], v['dept'], v['job_title']])

    tool.push_list_to_xls(my_list, 'mom.xlsx',)







exit()

# mai = ws.cell_value(0, 0)
# raw_len = len(raw)
# names = []
# name = ''
# for c in raw:
#     if c != ';':
#         name = name + c
#     else:
#         if name[0] == ' ':
#             name = name[1:]
#         names.append(name)
#         name = ''
#
#
# word = ''
# word_list = []
# scrubbed_names = [['fname', 'lname', 'full name', 'username', 'email']]
# for name in names:
#     for c in name:
#         if c == ' ' or c == '>':
#             word = word.replace('(', '')
#             word = word.replace(')', '')
#             word = word.replace('<', '')
#             word_list.append(word)
#             word = ''
#         else:
#             word = word + c
#
#     # In case we have a middle name consolidate
#     if len(word_list) != 4:
#         word_list = [word_list[0], word_list[1] + ' ' + word_list[2], word_list[3], word_list[4]]
#
#     # create and insert the full name ie Pisano, Jim
#     fname = word_list[0]
#     lname = word_list[1]
#     full_name = lname+', '+ fname
#     word_list.insert(2, full_name)
#
#     scrubbed_names.append(word_list)
#     word_list = []
#
# for user in scrubbed_names:
#     print(user)
#
#
# push_list_to_xls(scrubbed_names,'mailer_names.xlsx')
# # push_xls_to_ss('mailer_names.xlsx', 'CTUG mailer')
#
#
