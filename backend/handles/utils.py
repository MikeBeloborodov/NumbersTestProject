from typing import List
import requests
import csv


def filter_orders_for_valid_dates(orders: List[dict]) -> List[dict]:
    """
    Checks all orders for valid dates and returns them in a list
    """
    # TODO finish filtering logic
    return orders


def filter_orders_for_expired_dates(orders: List[dict]) -> List[dict]:
    """
    Checks all orders for expired dates and returns them in a list
    """
    # TODO finish filtering logic
    return orders


def send_expired_orders_telegram(orders: List[dict]) -> bool:
    """
    Sends expired orders to telegram
    Returns True if data was sent and False if not
    """
    telegram_bot_key = "5591323334:AAFP0uESxFkUKTPSkK8B39jls3V0paHAYIk"
    base_telegram_url = "https://api.telegram.org/bot"

    res = requests.get(base_telegram_url + telegram_bot_key + "/getUpdates")
    result = res.json()['result']
    message = result[0]['message']
    chat = message['chat']
    chat_id = chat['id']

    save_as_csv(orders)

    payload = {'document': open('expired_orders.csv', "rb")}
    res = requests.post(base_telegram_url + telegram_bot_key + f"/sendDocument?chat_id={chat_id}",
                            files=payload)
                             
    if res.status_code == 200:
        return True
    else:
        return False


def save_as_csv(orders: List[dict]):
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