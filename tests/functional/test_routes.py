from iebank_api import app
import pytest

def test_root_endpoint(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_skull_endpoint(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/skull' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/skull')
    assert response.status_code == 200
    assert b'This is the BACKEND SKULL' in response.data

def test_get_accounts(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John Doe'
    assert data['currency'] == '€'
    assert data['country'] == 'Spain'

def test_get_account_by_id(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is requested (GET)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Alice',
        'currency': '€',
        'country': 'France'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, get the account by id
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Alice'
    assert data['currency'] == '€'
    assert data['country'] == 'France'
    assert data['id'] == account_id

def test_update_account(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Bob',
        'currency': '£',
        'country': 'UK'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, update the account
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Robert'
    })
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data['name'] == 'Robert'
    assert updated_data['currency'] == '£'
    assert updated_data['country'] == 'UK'
    assert updated_data['id'] == account_id

    # Verify that the account was updated
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    get_data = get_response.get_json()
    assert get_data['name'] == 'Robert'

def test_delete_account(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the response is valid and the account no longer exists
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Charlie',
        'currency': '$',
        'country': 'USA'
    })
    assert create_response.status_code == 200, (
        f"Failed to create account. Status: {create_response.status_code}, "
        f"Response: {create_response.data.decode('utf-8')}"
    )
    account_data = create_response.get_json()
    assert account_data is not None, "Create response didn't return JSON data"
    assert 'id' in account_data, f"'id' not found in create response. Data: {account_data}"
    account_id = account_data['id']

    # Now, delete the account
    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200, (
        f"Failed to delete account. Status: {delete_response.status_code}, "
        f"Response: {delete_response.data.decode('utf-8')}"
    )

    # Verify that the account was deleted by checking the list of accounts
    get_all_response = testing_client.get('/accounts')
    assert get_all_response.status_code == 200, (
        f"Failed to get all accounts. Status: {get_all_response.status_code}, "
        f"Response: {get_all_response.data.decode('utf-8')}"
    )

    accounts_data = get_all_response.get_json()
    assert accounts_data is not None, "Get all accounts response didn't return JSON data"
    account_ids = [account['id'] for account in accounts_data.get('accounts', [])]
    assert account_id not in account_ids, "Deleted account still present in accounts list"

def test_get_nonexistent_account(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN a non-existent account is requested (GET)
    """
    response = testing_client.get('/accounts/9999')  # Assuming this ID does not exist
    assert response.status_code == 500

def test_update_nonexistent_account(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN a non-existent account is updated (PUT)
    THEN check that a 500 is returned
    """
    response = testing_client.put('/accounts/9999', json={'name': 'DoesNotExist'})
    assert response.status_code == 500

def test_delete_nonexistent_account(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN a non-existent account is deleted (DELETE)
    THEN check that a 500 is returned
    """
    response = testing_client.delete('/accounts/9999')
    assert response.status_code == 500

def test_create_account_missing_fields(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN creating an account with missing fields (POST)
    THEN check that a 500 is returned
    """
    response = testing_client.post('/accounts', json={'name': 'Incomplete'})
    assert response.status_code == 500

def test_register_user(testing_client):
    """
    GIVEN a Flask application
    WHEN registering a new user
    THEN check the response is valid
    """
    response = testing_client.post('/register', json={
        'name': 'John Doe',
        'email': 'jdoe@email.com',
        'password': 'password',
        'country': 'Spain',
        'state': 'Madrid',
        'date_of_birth': '1980-01-01',
        'role': 'user',
        'status': 'Active'
    })
    assert response.status_code == 200

def test_login_user(testing_client):
    """
    GIVEN a Flask application
    WHEN logging in a user
    THEN check the response is valid
    """
    response = testing_client.post('/login', json={
        'email': 'jdoe@email.com',
        'password': 'password'
    })
    assert response.status_code == 200

def test_login_user_wrong_password(testing_client):
    """
    GIVEN a Flask application
    WHEN logging in a user with the wrong password
    THEN check the response is valid
    """
    response = testing_client.post('/login', json={
        'email': 'jdoe@email.com',
        'password': 'wrong_password'
    })
    assert response.status_code == 500

def test_login_user_wrong_email(testing_client):
    """
    GIVEN a Flask application
    WHEN logging in a user with the wrong email
    THEN check the response is valid
    """
    response = testing_client.post('/login', json={
        'email': 'wrong_email',
        'password': 'password'
    })
    assert response.status_code == 500

def test_create_transaction(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/transactions' page is posted to (POST)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Alice',
        'currency': '€',
        'country': 'France'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, create a transaction
    response = testing_client.post('/transactions', json={
        'account_id': account_id,
        'amount': 100.0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['account_id'] == account_id
    assert data['amount'] == 100.0

def test_get_transactions(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/transactions' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/transactions')
    assert response.status_code == 200

def test_send_money(testing_client, login_user):
    """
    GIVEN a Flask application
    WHEN the '/send_money' page is posted to (POST)
    THEN check the response is valid
    """
    # First, create two accounts
    create_response_1 = testing_client.post('/accounts', json={
        'name': 'Alice',
        'currency': '€',
        'country': 'France'
    })
    assert create_response_1.status_code == 200
    account_data_1 = create_response_1.get_json()
    account_id_1 = account_data_1['id']

    create_response_2 = testing_client.post('/accounts', json={
        'name': 'Bob',
        'currency': '£',
        'country': 'UK'
    })
    assert create_response_2.status_code == 200
    account_data_2 = create_response_2.get_json()
    account_id_2 = account_data_2['id']

    # Add balance to the first account
    update_response = testing_client.put(f'/accounts/{account_id_1}', json={
        'name': 'Alice',
        'balance': 200.0
    })
    assert update_response.status_code == 200

    # Now, send money from the first account to the second account
    response = testing_client.post('/send_money', json={
        'from_account_id': account_id_1,
        'to_account_id': account_id_2,
        'amount': 50.0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Transaction successful'