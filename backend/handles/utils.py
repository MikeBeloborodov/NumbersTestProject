from typing import List
import requests
import csv
import time
import datetime
import re


def filter_orders_for_valid_dates(orders: List[dict]) -> List[dict]:
    """
    Checks all orders for valid dates and returns them in a list
    """
    filtered_orders = []
    for order in orders:
        date = order['delivery_date']

        if len(re.findall("\.", date)) != 2:
            continue
        if not date.replace(".", "").isnumeric():
            continue
        day, month, year = date.split(".")
        if len(day) != 2:
            continue
        if len(month) != 2:
            continue
        if len(year) != 4:
            continue

        filtered_orders.append(order)

    return filtered_orders


def filter_orders_for_expired_dates(orders: List[dict]) -> List[dict]:
    """
    Checks all orders for expired dates and returns them in a list
    """
    curr_date_raw = time.strftime("%d.%m.%Y")
    curr_day, curr_month, curr_year = curr_date_raw.split('.')
    curr_date_clean = datetime.datetime(int(curr_year), int(curr_month), int(curr_day))

    filtered_orders = []
    for order in orders:

        order_day, order_month, order_year = order['delivery_date'].split(".")
        delivery_date_clean = datetime.datetime(int(order_year), int(order_month), int(order_day)) 

        if curr_date_clean > delivery_date_clean:
            filtered_orders.append(order)

    return filtered_orders


def send_expired_orders_telegram(orders: List[dict]) -> bool:
    """
    Sends expired orders to telegram
    Returns True if data was sent and False if not
    """
    telegram_bot_key = "5591323334:AAFP0uESxFkUKTPSkK8B39jls3V0paHAYIk"
    base_telegram_url = "https://api.telegram.org/bot"

    res = requests.get(base_telegram_url + telegram_bot_key + "/getUpdates")
    result = res.json()['result']
    last_message = result[-1]['message']
    chat = last_message['chat']
    chat_id = chat['id']

    save_as_csv(orders)

    payload = {'document': open('expired_orders.csv', "rb")}
    res = requests.post(
        base_telegram_url + telegram_bot_key + f"/sendDocument?chat_id={chat_id}",
        files=payload)
                             
    if res.status_code == 200:
        return True
    else:
        return False


def save_as_csv(orders: List[dict]):
    """
    Saves expired orders in csv format
    """
    with open("expired_orders.csv", "w") as file:
        writer = csv.writer(file)

        title_row = ["№ Заказа", "Срок поставки"]
        writer.writerow(title_row)

        data_to_save = []
        for item in orders:
            row = [item['order_num'], item['delivery_date']]
            data_to_save.append(row)

        for item in data_to_save:
            writer.writerow(item)

