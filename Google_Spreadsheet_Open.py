import gspread
from oauth2client.service_account import ServiceAccountCredentials

from pprint import pprint
from googleapiclient import discovery
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("dbbbbb").sheet1
print(sheet)


src = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("dbbbbb");
print(src)

#sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")

 
 
