from flask import Flask, request
from flask_cors import CORS
from handles.order_handles import handle_save_orders
from handles.order_handles import handle_delete_all_orders
from handles.order_handles import handle_send_all_orders
from handles.order_handles import handle_check_order_dates

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return {"Message": "Orders API."}


@app.get("/orders")
def send_all_orders():
    return handle_send_all_orders()


@app.post("/orders")
def post_order():
    order_data = request.json
    return handle_save_orders(order_data)


@app.delete("/orders")
def delete_all_orders():
    return handle_delete_all_orders()


@app.get("/orders/check_dates")
def check_order_dates():
    return handle_check_order_dates()


if __name__ == "__main__":
    app.run(debug=True)