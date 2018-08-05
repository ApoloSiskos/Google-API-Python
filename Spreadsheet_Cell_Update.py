import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("APIv4 Spreadsheet Test").sheet1
 	
# Extract and print all of the values
campaign_name = sheet.cell(1, 3).value
print(campaign_name)

campaign_name = sheet.cell(1, 3).value
print(campaign_name)

campaign_title = sheet.cell(2, 3).value
print(campaign_title)

start_date = sheet.cell(3, 3).value
print(start_date)

end_date = sheet.cell(3, 5).value
print(end_date)

social_overview = sheet.cell(5, 5).value
print(social_overview)

social_highlights = sheet.cell(5, 6).value
print(social_highlights)

social_improvements = sheet.cell(5, 8).value
print(social_improvements)

programmatic_overview = sheet.cell(5, 9).value
print(programmatic_overview)

programmatic_highlights = sheet.cell(5, 10).value
print(programmatic_highlights)

programmatic_improvements = sheet.cell(5, 11).value
print(programmatic_improvements)


#sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")

 
