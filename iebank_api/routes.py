from flask import Flask, request, abort
from iebank_api import db, app
from iebank_api.models import Account, User
# imports hash funtion to encrypt the password
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '

    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text


@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    required_fields = ['name', 'currency', 'country']
    if not data or not all(field in data for field in required_fields):
        abort(500)  # Abort with 500 Internal Server Error if any field is missing

    name = data['name']
    currency = data['currency']
    country = data['country']

    account = Account(name, currency, country)
    db.session.add(account)
    db.session.commit()
    return format_account(account)


@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    if not account:
        abort(500)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    if not account:
        abort(500)
    account.name = request.json['name']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    if not account:
        abort(500)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'status': account.status,
        'created_at': account.created_at,
        'country': account.country
    }
    

def format_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'country': user.country,
        'state': user.state,
        'date_of_birth': user.date_of_birth,
        'role': user.role,
        'status': user.status
    }

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'country', 'state', 'date_of_birth', 'role', 'status']
    if not data or not all(field in data for field in required_fields):
        abort(500)
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        country=data['country'],
        state=data['state'],
        date_of_birth=data['date_of_birth'],
        role=data['role'],
        status=data['status']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return format_user(new_user)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['email', 'password']
    if not data or not all(field in data for field in required_fields):
        abort(500)
    
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        abort(500)
    
    if check_password_hash(user.password, data['password']):
        return format_user(user)
    else:
        abort(500)
