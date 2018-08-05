import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pprint import pprint
from googleapiclient import discovery

scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

service = discovery.build('sheets', 'v4', credentials=credentials)

# The ID of the spreadsheet containing the sheet to copy. It has to be a public one in this script (permission not defined).
spreadsheet_id = '1m-R6w15wyP_jt0F3Cw8dyhK8qlSLJ-j24wxvsD33sFU'  # TODO: Update placeholder value.
destination_spreadsheet_id = response['spreadsheetId']

# The ID of the sheet to copy.
sheet_id = 730266781  # TODO: Update placeholder value.

copy_sheet_to_another_spreadsheet_request_body = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': destination_spreadsheet_id,  # TODO: Update placeholder value.
      "deleteSheet": {
        "sheetId": 0
      }
    # TODO: Add desired entries to the request body.
}


request = service.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheet_id, sheetId=sheet_id, body=copy_sheet_to_another_spreadsheet_request_body)
response = request.execute()

# TODO: Change code below to process the `response` dict:
#pprint(response)
