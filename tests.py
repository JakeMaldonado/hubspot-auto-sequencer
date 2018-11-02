from main import get_driver, wait_for_element, login, search_emails, get_emails, get_dynamic_list, send_template
from datetime import timedelta
import datetime
import requests
import smtplib
import json
import csv

api_key = 'YOUR KEY'

# url = 'https://api.hubapi.com/contacts/v1/lists/' + list_id + '/contacts/all?hapikey=' + api_key
# print(url)
# contacts = get_dynamic_list(url)


# hubspot login info
credentials = ['ACCOUNT EMAIL', 'ACCOUNT PASSWORD']

# # sequence_info = [start_date, start_time, am/pm, days_until_followup, time_follow_up, am/pm]
sequence_info = ['02/23/2018', '3:30', 'pm', '5', '8:00', 'am']
#
# #emails to sequence
# test_contacts = [['jake', 'maldo', 'text company', 'https://app.hubspot.com/contacts/12345/contact/12345/?interaction=note']]

#template for the sequences

driver = get_driver(True)
print('******** Driver created ********')
login(credentials, driver)
print('******** Login completed ********')

# 
# with open('Sasha_Sequence_proper.csv', 'r') as f:
#     reader = csv.reader(f)
#     contact_list = list(reader)
# 
# get_emails(contact_list, template, sequence_info, driver)
# for contact in contact_list:
#     contact_id = contact[0]
#     contact_json = json.loads(requests.get(
#         'https://api.hubapi.com/contacts/v1/contact/vid/' + contact_id + '/profile?hapikey=' + api_key).text)
#     print('https://api.hubapi.com/contacts/v1/contact/vid/' + contact_id + '/profile?hapikey=' + api_key)
#     last_emailed = int(contact_json['properties']['hs_email_last_send_date']['value'].strip())
#     last_emailed_datetime = datetime.datetime.fromtimestamp(int(last_emailed) / 1e3)
#     if last_emailed_datetime < datetime.datetime.today() - timedelta(days=3):
#         print(contact)
#         print('Last emailed on:', last_emailed_datetime)
#         send_template(contact, template, sequence_info, driver)

#testing


with open('YOUR CONTACTS.csv', 'r') as f:
    reader = csv.reader(f)
    contact_list = list(reader)

while not contact_list == []:
    test = contact_list.pop(0)
    test_contact_id = test[0]
    print('https://api.hubapi.com/contacts/v1/contact/vid/' + test_contact_id + '/profile?hapikey=' + api_key)

    res = send_template(test, ['TEMPLATE SUBJECT'], driver)

    print(res)


