import gspread
from google.oauth2.service_account import Credentials

SPREADSHEET_NAME = '민원데이터시트'
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def connect_sheet():
    credentials = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
    client = gspread.authorize(credentials)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

def append_minwon_to_sheet(minwon_obj):
    sheet = connect_sheet()
    sheet.append_row(minwon_obj.to_list())

def get_all_minwons():
    sheet = connect_sheet()
    return sheet.get_all_records()
