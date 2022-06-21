import os.path

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIRECTORY, 'credentials.json')
SPREADSHEET_ID = '1k-AmgFGbBmuZTJOsjsk6HiHuU3RBapctOQq_p4W8Uuc'
RANGE_NAME = 'Лист1'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def main():
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])


if __name__ == '__main__':
    main()