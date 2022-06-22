import sys
import os
sys.path.append(os.path.join(sys.path[0],'schemas'))
sys.path.append(os.path.join(sys.path[0],'database'))

from schemas import post_order_request
from database.models import Order
from sqlalchemy.orm import Session
from database.database_logic import engine
from flask import Response


def handle_save_orders(order_data: post_order_request):
    try:
        with Session(engine) as db:
            order_to_save = Order(**order_data)
            db.add(order_to_save)
            db.commit()
    except Exception as execution_error:
        print(f"Error while saving order: {execution_error}")
        return Response("Internal Server Error.", status=500)

    return Response("Order saved.", status=201)


def handle_delete_all_orders():
    try:
        with Session(engine) as db:
            all_orders_query = db.query(Order)
            all_orders_query.delete()
            db.commit()

    except Exception as error:
        print(f"Error while saving order: {error}")
        return Response("Internal Server Error.", status=500)

    return Response("Orders deleted", status=200)