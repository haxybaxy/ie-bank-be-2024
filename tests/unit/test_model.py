from iebank_api.models import Account, User
from werkzeug.security import generate_password_hash, check_password_hash
import pytest
from datetime import datetime

def test_create_account():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status, created_at, and user_id fields are defined correctly
    """
    user_id = 1  # Assuming a user with ID 1 exists
    account = Account('John Doe', '€', 'Spain', user_id)
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.country == 'Spain'
    assert account.account_number is not None
    assert account.balance == 0.0
    assert account.status == 'Active'
    assert account.user_id == user_id

def test_create_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, email, password, country, state, date_of_birth, role, 
    status, created_at, updated_at, last_login_at, failed_login_attempts fields are 
    defined correctly
    """
    plain_password = 'password'
    hashed_password = generate_password_hash(plain_password, method='sha256')
    
    user = User(
                'John Doe', 
                'email', 
                hashed_password, 
                'Spain', 
                'Madrid', 
                datetime.strptime('1980-01-01', '%Y-%m-%d'), 
                'user', 
                'Active'
                )
    assert user.name == 'John Doe'
    assert user.email == 'email'
    assert check_password_hash(user.password, plain_password)
    assert user.country == 'Spain'
    assert user.state == 'Madrid'
    assert user.date_of_birth == datetime.strptime('1980-01-01', '%Y-%m-%d')
    assert user.role == 'user'
    assert user.status == 'Active'
    assert user.failed_login_attempts == 0
    assert user.last_login_at is not None
    assert user.updated_at is not None
    assert user.created_at is not None
    