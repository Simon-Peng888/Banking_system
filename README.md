# Simple Banking System API

This project implements a simple banking system using Flask for the API backend. It allows users to create accounts, perform deposits, withdrawals, and transfers, and save or load the system state to/from a CSV file.

## Features

- Create a new bank account
- Retrieve account details
- Deposit money into an account
- Withdraw money from an account
- Transfer money between accounts
- Save the system state to a CSV file
- Load the system state from a CSV file

## Setup and Installation

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Running the Application
Run the Flask Application
To start the Flask application, navigate to the project directory and run:
```bash
$ python app.py
```
The application will be available at http://127.0.0.1:5000.

Running Tests
To run the tests for the application, use pytest. The tests are located in the tests/ directory.
```bash
$ pytest tests/
```

API Endpoints
1. Create an Account
Endpoint: /account
Method: POST
Description: Creates a new account with a specified name and an optional initial balance.
```bash
curl -s -X POST http://127.0.0.1:5000/account -H "Content-Type: application/json" -d '{"name": "AccountName", "balance": 100}'

Response:
{
  "balance": 100,
  "name": "AccountName",
}
```
2. Get Account Details
Endpoint: /account/<name>
Method: GET
Description: Retrieves details of the specified account.
```bash
curl -s -X GET http://127.0.0.1:5000/account/AccountName

Response:
{
  "balance": 100,
  "name": "AccountName",
  "transactions": []
}

```
3. Deposit Money
Endpoint: /account/<name>/deposit
Method: POST
Description: Deposits a specified amount of money into the specified account.
```bash
curl -s -X POST http://127.0.0.1:5000/account/AccountName/deposit -H "Content-Type: application/json" -d '{"amount": 50}'


Response:
{
  "balance": 150,
  "name": "AccountName"
}

```
4. Withdraw Money
Endpoint: /account/<name>/withdraw
Method: POST
Description: Withdraws a specified amount of money from the specified account.
```bash
curl -s -X POST http://127.0.0.1:5000/account/AccountName/withdraw -H "Content-Type: application/json" -d '{"amount": 50}'

Response:
{
  "balance": 100,
  "name": "AccountName"
}

```
5. Transfer Money
Endpoint: /transfer
Method: POST
Description: Transfers a specified amount of money from one account to another.
```bash
curl -s -X POST http://127.0.0.1:5000/account -H "Content-Type: application/json" -d '{"name": "AccountName1", "balance": 100}'

curl -s -X POST http://127.0.0.1:5000/account -H "Content-Type: application/json" -d '{"name": "AccountName2", "balance": 50}'

curl -s -X POST http://127.0.0.1:5000/transfer -H "Content-Type: application/json" -d '{"from": "AccountName1", "to": "AccountName2", "amount": 50}'


Response:
{
  "amount": 50,
  "from": "AccountName1",
  "to": "AccountName2"
}

```
6. Save System State
Endpoint: /save
Method: POST
Description: Saves the current state of all accounts to a CSV file.
```bash
curl -s -X POST http://127.0.0.1:5000/save

Response:
{
  "message": "System state saved successfully"
}
```
7. Load System State
Endpoint: /load
Method: POST
Description: Loads the system state from a CSV file.
```bash
curl -s -X POST http://127.0.0.1:5000/load

Response:
{
  "message": "System state loaded successfully"
}
```
8. Error Handling
```bash
Duplicate Account Creation:
{
  "error": "Account already exists"
}

Account Not Found:
{
  "error": "Account not found"
}

Insufficient Funds:
{
  "error": "Insufficient funds"
}

Invalid Amount:
{
  "error": "Deposit amount must be positive"
}
```
Notes :
1. The system state is saved in a CSV file located in the data/ directory.
2. The project includes comprehensive unit tests that can be executed with pytest.
3. The tests ensure that all functionalities, including error handling, are working as expected.