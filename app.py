from flask import Flask, request, jsonify
from services import BankingService
from models import BankAccount

app = Flask(__name__)
banking_service = BankingService()

@app.route('/')
def home():
    return "Welcome to the Simple Banking System API!"

@app.route('/account', methods=['POST'])
def create_account():
    data = request.json
    print(f"Received data: {data}")  
    name = data.get('name')
    balance = data.get('balance', 0) 
    try:
        account = banking_service.create_account(name, balance)
        return jsonify({"name": account.name, "balance": account.balance}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/account/<name>', methods=['GET'])
def get_account(name):
    """Retrieve the details of an account."""
    try:
        account = banking_service.get_account(name)
        return jsonify({
            "name": account.name,
            "balance": account.balance,
            "transactions": account.transactions
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/account/<name>/deposit', methods=['POST'])
def deposit(name):
    """Deposit an amount to a specific account."""
    amount = request.json.get('amount')
    try:
        account = banking_service.get_account(name)
        account.deposit(amount)
        return jsonify({"name": account.name, "balance": account.balance})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/account/<name>/withdraw', methods=['POST'])
def withdraw(name):
    """Withdraw an amount from a specific account."""
    amount = request.json.get('amount')
    try:
        account = banking_service.get_account(name)
        if amount <= 0: 
            raise ValueError("Withdrawal amount must be positive")
        account.withdraw(amount)
        return jsonify({"name": account.name, "balance": account.balance}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/transfer', methods=['POST'])
def transfer():
    """Transfer an amount from one account to another."""
    data = request.json
    from_name = data.get('from')
    to_name = data.get('to')
    amount = data.get('amount')
    try:
        from_account = banking_service.get_account(from_name)
        to_account = banking_service.get_account(to_name)
        from_account.transfer(to_account, amount)
        return jsonify({"from": from_name, "to": to_name, "amount": amount})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/save', methods=['POST'])
def save_system():
    """Save the current state of all accounts to a CSV file."""
    filepath = 'data/accounts.csv'
    BankAccount.save_accounts(banking_service.accounts, filepath)
    return jsonify({"message": "System state saved successfully"}), 200

@app.route('/load', methods=['POST'])
def load_system():
    filepath = 'data/accounts.csv'
    print(f"Attempting to load accounts from {filepath}")  
    try:
        banking_service.accounts = BankAccount.load_accounts(filepath)
        return jsonify({"message": "System state loaded successfully"}), 200
    except FileNotFoundError:
        print("FileNotFoundError caught, returning 404")  
        return jsonify({"error": "No saved state found"}), 404



if __name__ == '__main__':
    app.run(debug=True)
