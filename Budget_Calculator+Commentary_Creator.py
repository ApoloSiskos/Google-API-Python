import pandas as pd
import os
import csv
import time
import dateutil.parser as dparser
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from googleapiclient import discovery
from datetime import datetime, timedelta

#Read Bionic CSV export
def get_csv():
    df = pd.read_csv('input.csv', encoding = "ISO-8859-1",mangle_dupe_cols=True, parse_dates=['Start Date', 'End Date'])
    df = df[df['Line Type'].str.contains('Placement')]

    return df

def main():
    df = get_csv()

    varA      = 'Campaign ID';
    dfGrouped = df.groupby(varA, as_index=False).agg({'Start Date': 'min', 'End Date': 'max'}).copy()

    varsToKeep = ['Campaign ID', 'Campaign Name', 'Site', 'Inventory Type', 'Advertiser Name', 'Line Type', 'Start Date_grp', 'End Date_grp', 'Total Media Cost', 'Agency Comp', ]
    dfTemp = pd.merge(df, dfGrouped, how='inner', on='Campaign ID', suffixes=(' ', '_grp'), copy=True)[varsToKeep]

    dfBreakDown = dfTemp.groupby(['Campaign ID', 'Campaign Name', 'Site', 'Advertiser Name','Inventory Type', 'Start Date_grp','End Date_grp']).sum()

    dfTemp['Net Cost'] = (dfTemp['Total Media Cost'] - dfTemp['Agency Comp'])

    groupedBy = dfTemp.groupby(['Campaign ID', 'Campaign Name', 'Site', 'Advertiser Name','Inventory Type']).agg({'Start Date_grp': 'min', 'End Date_grp': 'max', 'Total Media Cost': 'sum', 'Agency Comp': 'sum', 'Net Cost': 'sum'})


    groupedBy.to_csv(path_or_buf='test111.csv', sep=',', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.')
    df = pd.read_csv("test111.csv")

    #If there are Sites set to "facebook & instagram" then we need the Total Cost only and not separated by platform (e.g. Instagram, Facebook etc)
    for row in groupedBy.itertuples():
        if row[0][2] == "facebook & instagram":
            ids = df['Campaign ID'][df.Site == 'facebook & instagram'].unique()
            df.loc[df['Campaign ID'].isin(ids) & df.Site.isin(['facebook', 'instagram']), 'Site'] = 'facebook & instagram'

    N_N = ""
    End_Date = ""
    Start_Date = ""
    Site_Name = ""
    Advertiser = ""
    Sheet_Title = ""
    facebook_budget = 0
    instagram_budget = 0
    twitter_budget = 0
    youtube_budget = 0
    programmatic_budget = 0
    twitter_budget = 0
    total_budget = 0
    Id_list = [64327] 
    #[62443,62433,62222,62221,62281]

    df = df.groupby(['Campaign ID', 'Campaign Name', 'Site','Inventory Type','Advertiser Name']).agg({'Start Date_grp': 'min', 'End Date_grp': 'max', 'Total Media Cost': 'sum', 'Agency Comp': 'sum', 'Net Cost': 'sum'})

    for Id_Number in Id_list:
        for row in df.itertuples():
            if row[0][0] == Id_Number:
                if row[0][3] == "social":
                    Start_Date = row[1]
                    End_Date = row[2]
                    N_N = row[0][1]
                    Site_Name = row[0][2]
                    Advertiser = row[0][4]
                    if row[0][2] == "facebook":
                        facebook_budget = round(row[5], 0)
                    if row[0][2] == "instagram":
                        instagram_budget = round(row[5],    0)
                    if row[0][2] == "twitter":
                        twitter_budget = round(row[5], 0)
                    if row[0][2] == "youtube":
                        youtube_budget = round(row[5], 0)
                    #If Site = "facebook & instagram" apply this Site to every line. Get the values for the commentary. 
                    if row[0][2] == "facebook & instagram":
                        total_budget = round(row[5], 0)
                        print(total_budget)
                    Sheet_Title = str(Advertiser) + " - Social - " + str(Id_Number)
                if row[0][3] == "programmatic":
                    Start_Date = row[1]
                    End_Date = row[2]
                    N_N = row[0][1]
                    Site_Name = row[0][2]
                    Advertiser = row[0][4]
                    if row[0][2] == "adwords":
                        programmatic_budget += round(row[5], 0)
                    if row[0][2] == "dbm":
                        if N_N[:2].lower() ==  "us":
                            programmatic_budget += round(row[3], 0)
                        else:
                            programmatic_budget += round(row[5], 0)
                    if row[0][2] == "youtube":
                        if N_N[:2].lower() ==  "us":
                            youtube_budget += round(row[3], 0)
                        else:
                            youtube_budget += round(row[5], 0)
                    Sheet_Title = str(Advertiser) + " - Programmatic - " + str(Id_Number)

    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    gc = gspread.authorize(credentials)

    service = discovery.build('sheets', 'v4', credentials=credentials)

    spreadsheet_body = {
    "properties": {
        "title": Sheet_Title
    }
    }

    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()

    # The ID of the spreadsheet containing the sheet to copy.
    spreadsheet_id = '1m-R6w15wyP_jt0F3Cw8dyhK8qlSLJ-j24wxvsD33sFU'  # TODO: Update placeholder value.
    destination_spreadsheet_id = response['spreadsheetId']

    yesterday = datetime.now() - timedelta(days=1)

    # The ID of the sheet to copy.
    if N_N[:2].lower() ==  "us":
        tabTitle = "US"
        sheet_id = 701427508
        yesterday = yesterday.strftime('%m/%d/%Y') 
    else:
        tabTitle = "RoW"
        sheet_id = 730266781  
        yesterday = yesterday.strftime('%d/%m/%Y')



    copy_sheet_to_another_spreadsheet_request_body = {
        # The ID of the spreadsheet to copy the sheet to.
        "destination_spreadsheet_id": destination_spreadsheet_id,  # TODO: Update placeholder value.
    }

    request = service.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheet_id, sheetId=sheet_id, body=copy_sheet_to_another_spreadsheet_request_body)
    response = request.execute()
    
    #Delete first sheet (tab) 
    batch_update_spreadsheet_request_body = {
    "requests": [{
        "deleteSheet": {
        "sheetId": 0
        }
    }]
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=destination_spreadsheet_id, body=batch_update_spreadsheet_request_body)
    response = request.execute()

    #Get sheet ID
    include_grid_data = False

    request = service.spreadsheets().get(spreadsheetId=destination_spreadsheet_id, includeGridData=include_grid_data)
    response = request.execute()
    tabID = response['sheets'][0]['properties']['sheetId']

    #Update sheet name
    batch_update_spreadsheet_request_body = {
    "requests": [
        {
        "updateSheetProperties": {
            "properties": {
            "sheetId": tabID,
            "title": tabTitle
            },
            "fields": "title"
        }
        }
    ]
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=destination_spreadsheet_id, body=batch_update_spreadsheet_request_body)
    response = request.execute()


    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    #Update google sheet cells

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(Sheet_Title).worksheet(tabTitle)  
        
    #Update Campaign Name
    sheet.update_cell(1, 3, N_N)

    #Update Start Date
    sheet.update_cell(3, 3, Start_Date)

    #Update End Date
    sheet.update_cell(3, 5, End_Date)

    #Update Facebook Budget
    sheet.update_cell(5, 18, facebook_budget)

    #Update Instagram Budget
    sheet.update_cell(5, 20, instagram_budget)

    #Update Twitter Budget
    sheet.update_cell(5, 19, twitter_budget)

    #Update Youtube Budget
    sheet.update_cell(5, 23, youtube_budget)

    #Update Programmatic Budget
    sheet.update_cell(5, 24, programmatic_budget)

    #Update Total Budget
    if total_budget > 0:
        sheet.update_cell(5, 17, total_budget)

    #Update Day field with yesterday's date
    sheet.update_cell(5, 1, yesterday)


    gc.insert_permission(response['spreadsheetId'], 'apolo-not@not-182311.iam.gserviceaccount.com', perm_type='user', role='owner') #Add a valid username
    gc.insert_permission(response['spreadsheetId'], 'not.not@not.com', perm_type='user', role='owner') #Add a valid username

    return

if __name__ == "__main__":
        #Main
        main()