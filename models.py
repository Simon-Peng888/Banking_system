import csv
import uuid
from typing import List, Dict
import os

class BankAccount:
    def __init__(self, name: str, balance: float = 0.0):
        """Initialize a bank account with a unique account ID."""
        self.account_id = str(uuid.uuid4())  # Generate a unique account ID
        self.name = name
        self.balance = balance
        self.transactions: List[str] = []  # Record of transaction history

    def deposit(self, amount: float) -> None:
        """Deposit a certain amount into the account and record the transaction."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self._record_transaction(f"Deposit: {amount}")

    def withdraw(self, amount: float) -> None:
        """Withdraw a certain amount from the account and record the transaction."""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self._record_transaction(f"Withdraw: {amount}")

    def transfer(self, recipient_account: 'BankAccount', amount: float) -> None:
        """Transfer a certain amount to another account and record the transaction."""
        self.withdraw(amount)
        recipient_account.deposit(amount)
        self._record_transaction(f"Transfer to {recipient_account.name}: {amount}")
        recipient_account._record_transaction(f"Transfer from {self.name}: {amount}")

    def _record_transaction(self, transaction: str) -> None:
        """Record a transaction in the account's transaction history."""
        self.transactions.append(transaction)

    @staticmethod
    def save_accounts(accounts: Dict[str, 'BankAccount'], filepath: str) -> None:
        """Save the current state of all accounts to a CSV file."""
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['account_id', 'name', 'balance', 'transactions'])
            for account in accounts.values():
                writer.writerow([
                    account.account_id, 
                    account.name, 
                    f"{account.balance:.2f}",  
                    ';'.join(account.transactions)
                ])

    @staticmethod
    def load_accounts(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: '{filepath}'")
        accounts = {}
        with open(filepath, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                account_id = row['account_id']
                name = row['name']
                balance = float(row['balance'])
                transactions = row['transactions'].split(';')
                account = BankAccount(name, balance)
                account.account_id = account_id  
                account.transactions = transactions
                accounts[name] = account
        return accounts