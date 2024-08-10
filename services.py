from models import BankAccount

class BankingService:
    """Service layer responsible for managing bank accounts and operations."""

    def __init__(self):
        self.accounts = {}

    def create_account(self, name, balance=0):
        """Create a new account with a specified name and starting balance. Raises an error if the account already exists."""
        if name in self.accounts:
            raise ValueError("Account already exists")
        account = BankAccount(name, balance)
        self.accounts[name] = account
        return account

    def get_account(self, name):
        """Retrieve an account by name. Raises an error if the account does not exist."""
        if name not in self.accounts:
            raise ValueError("Account not found")
        return self.accounts[name]
