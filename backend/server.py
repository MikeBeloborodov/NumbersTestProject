from flask import Flask, request
from schemas import post_order_request
from handles.order_handles import handle_save_orders
from handles.order_handles import handle_delete_all_orders

app = Flask(__name__)

@app.route("/")
def index():
    return {"Message": "Hello world"}


@app.post("/orders")
def post_order():
    order_data = request.json
    return handle_save_orders(order_data)


@app.delete("/orders")
def delete_all_orders():
    return handle_delete_all_orders()


if __name__ == "__main__":
    app.run(debug=True)