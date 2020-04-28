import my_app.tool_box as tool


def gather_mailer_data(mailer_xlsx):
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

        # Skip a row that contains a nickname
        # We set this when / if we find a nickname
        if row_skip:
            row_skip = False
            continue

        # Quick check to make sure a nickname check does not throw an error
        # This only happens when we are on the last row
        if next_row == last_row:
            # Do NOT check for a nickname
            nickname_check = False
        else:
            # Check for a nickname
            nickname_check = True

        # Only check for a nickname if it is "safe" to
        # nickname_check is set when it we are not on the last row
        if nickname_check:
            # if col 0 is blank this indicates we have a nickname row
            if mail_ws.cell_value(row + 1, 0) == '':
                nickname = mail_ws.cell_value(row + 1, 3)
                row_skip = True  # skip this row on our next loop since it's a nickname row
            else:
                # There is no nickname so just set nickname to the same as fname
                nickname = mail_ws.cell_value(row, 3).capitalize()
        else:
            nickname = mail_ws.cell_value(row, 3).capitalize()
            row_skip = False

        # We need since every row does not have an emp_id
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
        job_title = mail_ws.cell_value(row, 10).rstrip()

        if job_title.find("MANAGER-REGIONAL") >= 0:
            job_title = "RM"
        elif job_title.find("DIRECTOR-REGIONAL") >= 0:
            job_title = "OD"
        elif job_title.find("DIRECTOR SYSTEMS ENGINEER") >= 0:
            job_title = "SED"
        elif job_title.find("MANAGER SYSTEMS ENGINEER") >= 0:
            job_title = "SEM"
        elif job_title.find("ARCHITECT") >= 0:
            job_title = 'TSA'
        elif job_title.find("SALES") >= 0:
            job_title = "PSS"

        if nickname != "No Nickname":
            nickname = nickname.replace('(', '', 1)
            nickname = nickname.replace(')', '', 1).capitalize()

        # Check Dept names and only include TA related departments
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
    return mailer_dict


if __name__ == "__main__" and __package__ is None:
    # my_ss = tool.Ssheet('Data Collection Test1',False)
    # print (my_ss.id)
    # # exit()
    # my_columns = [{'primary': True, 'title': 'ERP Customer Name', 'type': 'TEXT_NUMBER'},
    #               {'title': 'End Customer Ultimate Name', 'type': 'TEXT_NUMBER'},
    #               {'title': 'col1', 'type': 'CHECKBOX', 'symbol': 'STAR'}]
    #
    # my_ss.create_sheet('stan', my_columns)
    # print(my_ss.id)
    # exit()


    # my_ss.create_sheet()
    # exit()
    ta_mailer = {}
    my_mailer = gather_mailer_data('jchristo-mailer as of 04-25-20.xlsx')
    ta_mailer.update(my_mailer)

    my_mailer = gather_mailer_data('micashma-mailer as of 04-25-20.xlsx')
    ta_mailer.update(my_mailer)

    my_mailer = gather_mailer_data('rhinson-mailer as of 04-25-20.xlsx')
    ta_mailer.update(my_mailer)

    my_list = [['emp id', 'username', 'email', 'full name', 'manager',
                'dept', 'role', 'fname', 'nickname', 'lname']]

    for k, v in ta_mailer.items():
        # print(k, v['username'], v['dept'], v['job_title'])
        my_list.append([k, v['username'], v['email'], v['lname']+', '+v['nickname'],
                        v['manager_id'], v['dept'], v['job_title'],
                        v['fname'], v['nickname'], v['lname']])

    tool.push_list_to_xls(my_list, 'tmp_global_ta_team.xlsx',)

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
