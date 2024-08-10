
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app, banking_service
from models import BankAccount
from unittest.mock import patch

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_create_account(client):
    """Test creating a new account."""
    response = client.post('/account', json={"name": "Alice", "balance": 100})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "Alice"
    assert data['balance'] == 100

def test_create_account_no_initial_balance(client):
    """Test creating a new account with no initial balance."""
    banking_service.accounts.clear()
    response = client.post('/account', json={"name": "Alice"})
    assert response.status_code == 201

def test_create_duplicate_account(client):
    """Test creating an account with a duplicate name."""
    client.post('/account', json={"name": "Alice", "balance": 100})
    response = client.post('/account', json={"name": "Alice", "balance": 200})
    assert response.status_code == 400  # Duplicate names should not be allowed

def test_get_account(client):
    """Test retrieving an existing account."""
    client.post('/account', json={"name": "Bob", "balance": 200})
    response = client.get('/account/Bob')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Bob"
    assert data['balance'] == 200

def test_get_nonexistent_account(client):
    """Test retrieving a non-existent account."""
    response = client.get('/account/NonExistent')
    assert response.status_code == 404

def test_deposit(client):
    """Test depositing money into an account."""
    client.post('/account', json={"name": "Charlie", "balance": 50})
    response = client.post('/account/Charlie/deposit', json={"amount": 50})
    assert response.status_code == 200
    data = response.get_json()
    assert data['balance'] == 100

def test_deposit_invalid_amount(client):
    """Test depositing an invalid amount (negative)."""
    client.post('/account', json={"name": "Charlie", "balance": 50})
    response = client.post('/account/Charlie/deposit', json={"amount": -50})
    assert response.status_code == 400  # Negative deposits should not be allowed

def test_withdraw(client):
    """Test withdrawing money from an account."""
    client.post('/account', json={"name": "Dave", "balance": 100})
    response = client.post('/account/Dave/withdraw', json={"amount": 50})
    assert response.status_code == 200
    data = response.get_json()
    assert data['balance'] == 50

def test_withdraw_insufficient_funds(client):
    """Test withdrawing money with insufficient funds."""
    client.post('/account', json={"name": "Eve", "balance": 100})
    response = client.post('/account/Eve/withdraw', json={"amount": 150})
    assert response.status_code == 400

def test_withdraw_invalid_amount(client):
    """Test withdrawing an invalid amount (negative)."""
    client.post('/account', json={"name": "Dave", "balance": 100})
    response = client.post('/account/Dave/withdraw', json={"amount": -50})
    assert response.status_code == 400  # Negative withdrawals should not be allowed

def test_transfer(client):
    """Test transferring money between accounts."""
    client.post('/account', json={"name": "Frank", "balance": 100})
    client.post('/account', json={"name": "Grace", "balance": 100})
    response = client.post('/transfer', json={"from": "Frank", "to": "Grace", "amount": 50})
    assert response.status_code == 200
    frank_balance = client.get('/account/Frank').get_json()['balance']
    grace_balance = client.get('/account/Grace').get_json()['balance']
    assert frank_balance == 50
    assert grace_balance == 150

def test_transfer_insufficient_funds(client):
    """Test transferring money with insufficient funds."""
    client.post('/account', json={"name": "Frank", "balance": 50})
    client.post('/account', json={"name": "Grace", "balance": 100})
    response = client.post('/transfer', json={"from": "Frank", "to": "Grace", "amount": 100})
    assert response.status_code == 400  # Transfer should fail due to insufficient funds

def test_transfer_invalid_amount(client):
    """Test transferring an invalid amount (negative)."""
    client.post('/account', json={"name": "Frank", "balance": 100})
    client.post('/account', json={"name": "Grace", "balance": 100})
    response = client.post('/transfer', json={"from": "Frank", "to": "Grace", "amount": -50})
    assert response.status_code == 400  # Negative transfers should not be allowed

def test_save_system(client):
    """Test saving the system state to a CSV file."""
    response = client.post('/save')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "System state saved successfully"

def test_load_system(client):
    """Test loading the system state from a CSV file."""
    client.post('/account', json={"name": "Hank", "balance": 300})
    client.post('/save')

    # Clear current state and reload from the saved state
    banking_service.accounts.clear()
    response = client.post('/load')
    assert response.status_code == 200

    # Verify the account was loaded
    hank_balance = client.get('/account/Hank').get_json()['balance']
    assert hank_balance == 300

def test_load_nonexistent_system_state(client):
    """Test loading a system state from a nonexistent CSV file."""
    banking_service.accounts.clear()

    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        response = client.post('/load')
        
        assert response.status_code == 404 