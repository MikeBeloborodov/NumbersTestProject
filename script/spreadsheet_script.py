import os.path
import requests
import math
import time
from typing import List
import xml.etree.ElementTree as elem_tree
from googleapiclient.discovery import build
from google.oauth2 import service_account


BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_FILE_NAME = "credentials.json"
CURRENCY_FILE_NAME = "currency.xml"
SLEEP_TIME = 3


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


def convert_spreadsheet_data_to_dict(spreadsheet_data: list) -> List[dict]:
    """
    Converts spreadsheet data of a list type into a dict type
    """
    try:
        save_currency_xml()
        conv_rate = get_usd_convertion_rate()

        converted_data = []
        for counter, value in enumerate(spreadsheet_data):
            if counter == 0:
                continue
            if not value:
                continue

            order_table_num = None
            order_num = None
            price_usd = None
            price_rub = None
            delivery_date = None

            for item in value:
                if not order_table_num:
                    order_table_num = item;
                elif not order_num:
                    order_num = item
                elif not price_usd:
                    price_usd = item
                elif not delivery_date:
                    delivery_date = item

            # check if price_usd is numeric
            if price_usd:
                if not price_usd.strip().replace(",", "").replace(".", "").isnumeric():
                    price_usd = None
                else: 
                    # if numeric convert usd to rub
                    price_rub = price_usd * conv_rate
                    price_rub = math.trunc(price_rub * 100.0) / 100.0


            prepared_data = {
                "order_table_num": order_table_num,
                "order_num": order_num,
                "price_usd": price_usd,
                "price_rub": price_rub,
                "delivery_date": delivery_date
            }

            converted_data.append(prepared_data)

    except Exception as error:
        print("Error while converting spreadsheet data to dict: ")
        raise error
    
    return converted_data


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


def send_data_to_server(spreadsheet_data: List[dict]) -> None:
    """
    Sends data to the backend Flask API
    """
    try:
        res = requests.post("http://backend:5000/orders", json=spreadsheet_data)

        if res.status_code != 201:
            print(f"Res status code is: {res.status_code}")
            raise Exception

    except Exception as error:
        print("Error while sending data to server: ")
        raise error


def delete_old_orders():
    """
    Sends a delete request to the backend Flask API
    Deletes all orders
    """
    try:
        res = requests.delete("http://backend:5000/orders")

        if res.status_code != 200:
            print(f"Res status code is: {res.status_code}")
            raise Exception

    except Exception as error:
        print("Error while trying to delete old orders: ")
        raise error


def main() -> None:
    """
    Every SLEEP_TIME seconds gets data from the google spreadsheet
    deletes old data from SQL database and rewrites it with the new data
    """
    print("Script is running...")
    while True:
        try:
            new_data = get_spreadsheet_data()
            new_data = convert_spreadsheet_data_to_dict(new_data)

            delete_old_orders()
            send_data_to_server(new_data)

            time.sleep(SLEEP_TIME)

        except Exception as error:
            print(error)


if __name__ == '__main__':
    main()