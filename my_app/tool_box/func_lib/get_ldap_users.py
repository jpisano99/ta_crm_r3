import ldap
import json
# from csv import DictWriter
# import my_app.tool_box as tool
import pandas as pd
from my_app.my_secrets import passwords
import time

# import keyring
# import argparse
# import os

# ====================================================================================
# GLOBALS
# ------------------------------------------------------------------------------------
# uri = "ldaps://{ldapServer}".format(os.environ['LDAP_SERVER'])
# ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
# ldapClient = ldap.initialize(uri)
# ldapClient.set_option(ldap.OPT_REFERRALS, 0)

uri = "ldaps://ds.cisco.com"
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
ldapClient = ldap.initialize(uri)
ldapClient.set_option(ldap.OPT_REFERRALS, 0)

'''
====================================================================================
A bind account is required to search ldap.  Pass either keyring credentials or a
credentials file or default to an interactive prompt
------------------------------------------------------------------------------------
'''

LDAP_USER = 'jpisano'
LDAP_PASSWORD = passwords['LDAP_PASSWORD']

LDAP_GROUPS = ['group.sgomann', 'group.joebucha']
# LDAP_GROUPS = ['group.joebucha']
# LDAP_GROUPS = ['group.jpisano']

TETRATION_MGRS = ['jpisano', 'chmchenr', 'lpomelli']
SWATCH_MGRS = ['mimoriar', 'kennmill', 'joebucha']

print('Groups I am searching', LDAP_GROUPS)

# CN=jpisano,OU=Employees,OU=Cisco Users,DC=cisco,DC=com
# LDAP_USER = os.environ['LDAP_BIND_USER']
# LDAP_PASSWORD = os.environ['LDAP_BIND_PASSWORD']
# LDAP_GROUPS = ("".join(os.environ['LDAP_GROUPS'].split())).split(',')

# LDAP_USER = keyring.get_password('auslabBot', 'ldap_bind_user')
# LDAP_PASSWORD = keyring.get_password('auslabBot', 'ldap_bind_pwd')
# LDAP_GROUPS = ['group.seanmcge']

ldap.initialize(uri, bytes_mode=False)
ldapClient.bind_s('CN=jpisano,OU=Employees,OU=Cisco Users,DC=cisco,DC=com', LDAP_PASSWORD)
print('LDAP Bind Successful !!')

#
# ====================================================================================
# GetGroupMembers
#
# Description:  Function used to find all members of a provided group distinguished name
# and return a list of member employees and member groups
# ------------------------------------------------------------------------------------
#


def GetGroupMembers(groupDn):
    employees = []
    groups = []
    results = ldapClient.search_s(groupDn, ldap.SCOPE_SUBTREE, '(objectClass=*)', ['member'])

    for member in results[0][1]['member']:
        member = member.decode('utf-8')
        if 'Mailer' in member:
            continue
        if 'group' in member:
            groups.append(member)
        else:
            employees.append(member)
    return {
        'employees': employees,
        'groups':groups
    }


if __name__ == "__main__" and __package__ is None:
    #
    # ====================================================================================
    # Get members of parent group then iterate through all nested groups to get all member
    # employees
    # ------------------------------------------------------------------------------------
    #

    ldap_users = []
    for group in LDAP_GROUPS:
        employees = []
        groups = []

        results = GetGroupMembers("CN=%s,OU=Organizational,OU=Cisco Groups,DC=cisco,DC=com" % group)

        employees.extend(results["employees"])
        groups.extend(results["groups"])

        while True:
            if len(groups) > 0:
                for group in groups:
                    # group = group.decode('utf-8')
                    # print(group, type(group))
                    results = GetGroupMembers(group)
                    # print("GROUPS", results)
                    groups.remove(group)
                    groups.extend(results["groups"])
                    employees.extend(results["employees"])
            else:
                break

        '''
        ====================================================================================
        Iterate through all member employees and extract email address, first name, and
        last name
        ------------------------------------------------------------------------------------
        '''
        # ldap_users = []
        ldap_emails = set()
        for member in employees:
            try:
                target = ldapClient.search_s(member, ldap.SCOPE_SUBTREE, '(objectClass=*)',
                                             ['mail', 'description', 'sAMAccountName',
                                              'ciscoITDescription', 'st', 'l', 'title',
                                              'department', 'employeeID', 'manager'])

                person = {}
                person['email'] = target[0][1]['mail'][0].decode('utf-8')
                fullName = str(target[0][1]['description'][0].decode('utf-8')).split(' ')
                person['cec'] = target[0][1]['sAMAccountName'][0].decode('utf-8')
                person['fullName'] = str(target[0][1]['description'][0].decode('utf-8'))
                person['firstName'] = fullName[0]

                tmp_last_name = " ".join(fullName[1:])
                person['lastName'] = tmp_last_name.split()[0]  # Correct for names like Whitlock II

                person['title'] = target[0][1]['title'][0].decode('utf-8')
                person['dept name'] = target[0][1]['ciscoITDescription'][0].decode('utf-8')
                person['dept number'] = target[0][1]['department'][0].decode('utf-8')
                person['employeeID'] = target[0][1]['employeeID'][0].decode('utf-8')

                str_end = target[0][1]['manager'][0].decode('utf-8').find(',')
                person['manager'] = target[0][1]['manager'][0].decode('utf-8')[3:str_end]

                if person['manager'] in TETRATION_MGRS:
                    speciality = 'Tetration'
                elif (person['manager'] in SWATCH_MGRS) and \
                        (person['title'].find('TECHNICAL') != -1):
                    speciality = 'StealthWatch'
                else:
                    speciality = ''

                person['speciality'] = speciality

                ldap_users.append(person)
            except:
                print('Incomplete:', member)

    #
    # Create DataFrame for output
    #
    user_data = {'email': [],
                 'cec': [],
                 'fullName': [],
                 'firstName': [],
                 'lastName': [],
                 'title': [],
                 'dept name': [],
                 'dept number': [],
                 'employeeID': [],
                 'manager': [],
                 'speciality': []
                 }

    for user in ldap_users:
        for k, v in user.items():
            user_data[k].append(v)

    df_users = pd.DataFrame(user_data)
    df_users.to_excel('users.xlsx', index=False)

    ldapClient.unbind_s()