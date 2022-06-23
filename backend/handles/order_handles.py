import sys
import os
sys.path.append(os.path.join(sys.path[0],'schemas'))
sys.path.append(os.path.join(sys.path[0],'database'))

from database.models import Order
from sqlalchemy.orm import Session
from database.database_logic import engine
from flask import Response, jsonify
from typing import List
from handles.utils import filter_orders_for_valid_dates
from handles.utils import filter_orders_for_expired_dates
from handles.utils import send_expired_orders_telegram


def handle_save_orders(order_data: List[dict]):
    """
    Saves all orders in db
    """
    try:
        with Session(engine) as db:
            for data in order_data:
                order_to_save = Order(**data)
                db.add(order_to_save)
                db.commit()
    except Exception as execution_error:
        print(f"Error while saving order: {execution_error}")
        return Response("Internal Server Error.", status=500)

    return Response("Order saved.", status=201)


def handle_send_all_orders():
    """
    Takes all orders from db and sends it back
    """
    try:
        with Session(engine) as db:
            all_orders_query = db.query(Order)
            all_orders_raw = all_orders_query.all()

            all_orders_clean = [order.as_dict() for order in all_orders_raw]

    except Exception as error:
        print(f"Error while retrieving all orders {error}")
        return Response("Internal Server Error.", status=500)

    return jsonify(all_orders_clean)


def handle_delete_all_orders():
    """
    Deletes all items in the orders table
    """
    try:
        with Session(engine) as db:
            all_orders_query = db.query(Order)
            all_orders_query.delete()
            db.commit()

    except Exception as error:
        print(f"Error while saving order: {error}")
        return Response("Internal Server Error.", status=500)

    return Response("Orders deleted", status=200)


def handle_check_order_dates():
    """
    Checks all order dates for expiration
    """
    try:
        # Return all orders from db
        with Session(engine) as db:
            all_orders_query = db.query(Order)
            all_orders_raw = all_orders_query.all()
            all_orders = [order.as_dict() for order in all_orders_raw]

        # Filter orders for valid dates
        valid_date_orders = filter_orders_for_valid_dates(all_orders)
        
        # Filter expired orders
        expired_orders = filter_orders_for_expired_dates(valid_date_orders)

        # Sends expired orders to telegram
        res = send_expired_orders_telegram(expired_orders)
        if res:
            return Response("Message with expired dates is sent", status=200)
        else:
            return Response("Error while sending to telegram", status=500)

    except Exception as error:
        print(f"Error while checking order dates: {error}")
        return Response("Internal Server Error.", status=500)




