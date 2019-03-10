from flask import Flask, request, jsonify
from model import db, Transaction
from random import randint
from datetime import date, timedelta
import json
from base import Gopay
from config import TOKEN, API_KEY


app = Flask(__name__)


def protected(func):
    def wrapper(*args, **kwargs):
        try:
            if request.form["key"] == API_KEY:
                return func(*args, **kwargs)
            else:
                return jsonify({"status": "error", "message": "API key mismatch"})
        except:
            return jsonify(
                {"status": "error", "message": "API key parameter not found"}
            )

    wrapper.__name__ = func.__name__
    return wrapper


@app.before_request
def connect_db():
    """Connect to db before request made"""
    if db.is_closed():
        db.connect()


@app.after_request
def disconnect_db(response):
    """Disconnect from db after handling request"""
    if not db.is_closed():
        db.close()

    return response


@app.route("/generate", methods=["POST"])
@protected
def generate():
    """Generate a transaction from value"""
    value = int(request.form["amount"])
    today = date.today().strftime("%Y-%m-%d")
    not_assigned = True

    while not_assigned:
        # Making sure there isn't any duplicate value
        add_value = randint(0, 999)  # Random 3 digit number for verification
        not_assigned = (
            Transaction.select()
            .where(
                Transaction.created_at == date.today(),
                Transaction.amount == value + add_value,
            )
            .exists()
        )

    transaction = Transaction(amount=value + add_value)
    transaction.save()
    print(transaction.created_at)

    return jsonify(
        {
            "transaction_id": transaction.id,
            "amount": value + add_value,
            "status": "success",
        }
    )


@app.route("/confirm", methods=["POST"])
@protected
def confirm():
    """Check a transaction confirmation status"""
    gopay = Gopay.load(TOKEN)
    transaction_id = int(request.form["id"])
    limit = int(request.form["limit"])

    try:
        transaction = Transaction.get(
            Transaction.id == transaction_id, Transaction.created_at == date.today()
        )
    except:
        return jsonify({"status": "error", "detail": "transaction not found"})

    if transaction.status is True:
        # Already confirmed
        return jsonify({"status": "success", "confirmed": True})

    history = gopay.history(limit)
    found = False
    i = 0

    while not found and i < len(history):
        trx = history[i]
        if (trx["amount"] == (transaction.amount)) and (trx["type"] == "credit"):
            found = True

        i += 1

    if not found:
        return jsonify({"status": "fail", "confirmed": False})

    transaction.status = True
    transaction.save()

    return jsonify({"status": "success", "confirmed": True})


if __name__ == "__main__":
    app.run(debug=True)
