from flask import Flask, request, jsonify
from schemas import post_order_request
from database.database_logic import get_db
from sqlalchemy.orm import Session
from handles.order_handles import handle_save_orders

app = Flask(__name__)

@app.route("/")
def index():
    return {"Message": "Hello world"}


@app.post("/orders")
def post_order(db: Session = get_db):
    order_data = request.json
    return handle_save_orders(order_data, db)


if __name__ == "__main__":
    app.run(debug=True)