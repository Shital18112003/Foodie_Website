
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database
menu = [
    {"id": 1, "name": "Pizza", "price": 250},
    {"id": 2, "name": "Burger", "price": 120},
    {"id": 3, "name": "Pasta", "price": 200},
]

orders = []

@app.route("/menu", methods=["GET"])
def get_menu():
    """
    Returns the menu items.

    Returns:
        jsonify: A JSON response with the menu items.
    """
    return jsonify(menu), 200

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    """
    Adds an item to the cart.

    Expects a JSON payload with the following fields:
    - food_id (int): The ID of the food item
    - quantity (int): The quantity of the food item (default: 1)

    Returns:
        jsonify: A JSON response with the added order item.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    food_id = data.get("food_id")
    quantity = data.get("quantity", 1)

    food = next((item for item in menu if item["id"] == food_id), None)
    if not food:
        return jsonify({"error": "Food item not found"}), 404

    order_item = {
        "food_id": food["id"],
        "name": food["name"],
        "quantity": quantity,
        "price": food["price"] * quantity,
    }

    orders.append(order_item)
    return jsonify({"message": "Item added to cart", "order_item": order_item}), 201

@app.route("/place_order", methods=["POST"])
def place_order():
    """
    Places an order.

    Expects a JSON payload with the following fields:
    - payment_method (str): The payment method used (UPI, Card, or Cash on Delivery)
    - address (str): The delivery address

    Returns:
        jsonify: A JSON response with the order details.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    payment_method = data.get("payment_method")
    valid_payment_methods = ["UPI", "Card", "Cash on Delivery"]
    if payment_method not in [method.lower() for method in valid_payment_methods]:
        return jsonify({"error": "Invalid payment method"}), 400

    address = data.get("address")
    if not address or len(address) < 10:
        return jsonify({"error": "Invalid address"}), 400

    final_order = {
        "items": orders,
        "total": sum(item["price"] for item in orders),
        "payment_method": payment_method,
        "address": address,
        "status": "Order placed",
    }

    orders.clear()
    return jsonify({"message": "Order placed successfully", "order": final_order}), 200

if __name__ == "__main__":
    app.run(debug=True)
