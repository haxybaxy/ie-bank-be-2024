from iebank_api.models import Account, User
from werkzeug.security import generate_password_hash, check_password_hash
import pytest

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', 'Spain')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.country == 'Spain'
    assert account.account_number != None
    assert account.balance == 0.0
    assert account.status == 'Active'
    

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
                '1980-01-01', 
                'user', 
                'Active'
                )
    assert user.name == 'John Doe'
    assert user.email == 'email'
    assert check_password_hash(user.password, plain_password)
    assert user.country == 'Spain'
    assert user.state == 'Madrid'
    assert user.date_of_birth == '1980-01-01'
    assert user.role == 'user'
    assert user.status == 'Active'
    assert user.failed_login_attempts == 0
    assert user.last_login_at is not None
    assert user.updated_at is not None
    assert user.created_at is not None
    
    
    def test_login():
        """
        GIVEN a User model
        WHEN a user is logged in
        THEN check the last_login_at field is updated
        """
        plain_password = 'password'
        hashed_password = generate_password_hash(plain_password, method='sha256')
        
        user = User(
                    'John Doe', 
                    'email', 
                    hashed_password, 
                    'Spain', 
                    'Madrid', 
                    '1980-01-01', 
                    'user', 
                    'Active'
                    )
        
        last_login_at = user.last_login_at
        user.login()
        assert user.last_login_at > last_login_at
        assert user.failed_login_attempts == 0
        
        user.failed_login_attempts = 3
        user.login()

    