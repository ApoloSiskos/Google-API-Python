"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pprint import pprint
from googleapiclient import discovery

#Change placeholder below to generate authentication credentials. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample

# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/spreadsheets'


scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

service = discovery.build('sheets', 'v4', credentials=credentials)

spreadsheet_body = {
"properties": {
    "title": "xxGoogleAPIMasterTemplatexx"
  }
}

request = service.spreadsheets().create(body=spreadsheet_body)
response = request.execute()

gc.insert_permission(response['spreadsheetId'], 'apolo-not@not-182311.iam.gserviceaccount.com', perm_type='user', role='owner') #Add a valid username
gc.insert_permission(response['spreadsheetId'], 'not.not@not.com', perm_type='user', role='owner') #Add a valid username

# Rename a cell
    #campaign_name = sheet.cell(1, 3).value
    #sheet.update_cell(1, 1, "BBB")

