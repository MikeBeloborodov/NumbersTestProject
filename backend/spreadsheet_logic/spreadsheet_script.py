import os.path
import requests
import json
import math
import xml.etree.ElementTree as elem_tree
from googleapiclient.discovery import build
from google.oauth2 import service_account


BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_FILE_NAME = "credentials.json"
CURRENCY_FILE_NAME = "currency.xml"
JSON_DATA_FILE_NAME = "gathered_data.json"


def get_spreadsheet_data() -> list:
    """
    Returns data from a google spreadsheet as a list.
    """
    try:
        # Authentication in google to get permission for using service
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials_file_path = os.path.join(BASE_DIRECTORY, CREDENTIALS_FILE_NAME)
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file_path, scopes=scopes)

        # With this service we can interact with google spreadsheets API
        service = build('sheets', 'v4', credentials=credentials)

        # Get data from a spreadsheet with this id and this name range 
        spreadsheet_id = '1k-AmgFGbBmuZTJOsjsk6HiHuU3RBapctOQq_p4W8Uuc'
        spreadsheet_name_range = 'Лист1'
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=spreadsheet_name_range).execute()

        # All the values from this spreadsheet
        values = result.get('values', [])

    except Exception as error:
        print("Error while trying to get spreadsheet data: ")
        raise error

    return values


def save_currency_xml() -> None:
    """
    Saves currency data from cbr.ru API in xml format in the current folder.
    """
    try:
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        res = requests.get(url)

        path = os.path.join(BASE_DIRECTORY, CURRENCY_FILE_NAME)
        with open(path, 'wb') as file:
            file.write(res.content)

    except Exception as error:
        print("Error while saving currency xml: ")
        raise error


def get_usd_convertion_rate() -> float:
    """
    Returns current USD to RUB convertion rate.
    """
    try:
        path = os.path.join(BASE_DIRECTORY, CURRENCY_FILE_NAME)
        tree = elem_tree.parse(path)
        root = tree.getroot()
        currencies = root.findall('Valute')

        # Iterates trough all currencies and if finds USD
        # returns rate value
        for item in currencies:
            name = item.find('CharCode')
            if name.text == 'USD':
                usd_rate = item.find('Value').text.replace(",", ".")

    except Exception as error:
        print("Error while trying to get USD convertion rate: ")
        raise error
    
    return float(usd_rate)


def save_gathered_data_json() -> None:
    """
    Prepares and saves all gathered data from the spreadsheet
    as a json format file.
    """
    try:
        spreadsheet_data = get_spreadsheet_data()
        conv_rate = get_usd_convertion_rate()
        data_to_save_as_json = []

        for counter, value in enumerate(spreadsheet_data):
            if counter == 0:
                continue

            order_table_num = value[0]
            order_num = value[1]
            price_usd = float(value[2])
            price_rub = price_usd * conv_rate
            price_rub = math.trunc(price_rub * 100.0) / 100.0
            delivery_date = value[3]

            prepared_data = {
                "order_table_num": order_table_num,
                "order_num": order_num,
                "price_rub": price_rub,
                "price_usd": price_usd,
                "delivery_date": delivery_date
            }

            data_to_save_as_json.append(prepared_data)

        path = os.path.join(BASE_DIRECTORY, JSON_DATA_FILE_NAME)
        with open(path, "w") as file:
            file.write(json.dumps(data_to_save_as_json))
        
    except Exception as error:
        print("Error while saving gathered data as json: ")
        raise error


def send_data_to_server():
    try:
        path = os.path.join(BASE_DIRECTORY, JSON_DATA_FILE_NAME)
        with open(path, "r") as file:
            data_raw = file.read()
            json_data = json.loads(data_raw)

        res = requests.post("http://localhost:5000/orders", json=json_data[0])
        print(res.status_code)

    except Exception as error:
        print("Error while sending data to server: ")
        raise error


def main() -> None:
    try:
        save_currency_xml()
        save_gathered_data_json()
        send_data_to_server()

    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()