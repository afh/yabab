# Yet Another Build A Bank

A backend banking API for the fictional YaBaB Savings Bank.

## TL;DR

### Testing the deployed application

* Access the application deployed at [http://yabab.herokuapp.com/api](http://yabab.herokuapp.com/api) according to [Specification](#apidesign) below:

        % export API_HOST=http://yabab.herokuapp.com/
        ## Retrieve API information
        % curl -sL ${API_HOST}/api | json_reformat
        {
          "message": "Welcome to the YaBaB API",
          "version": "v0.0.1"
        }
        ## Retrieve balance for account 0821788037 
        % curl -sL ${API_HOST}api/accounts/0821788037 | json_reformat
        {
          "balance": 600.0
        }
        ## Create new account with initial deposit of ¤2,000.00 for customer with id 1
        % curl -sL -XPOST -F'customer_id=1' -F'initial_deposit=2000.00' ${API_HOST}api/accounts | json_reformat
        {
          "account_number": "0384723632"
        }
        ## Create new transaction from account 0738654399 to account 0821788037 with an amount of ¤100.00 and the payment reference "Reimbursement"
        % curl -sL -XPOST -H'Content-Type: application/json' -d'{"amount":100.00, "reference":"Reimbursement", "beneficiary":"0821788037", "originator":"0738654399"}' ${API_HOST}/api/transactions
        {
          "transaction": 10
        }


### Running locally

0. Necessary Prerequisites:

    * [Homebrew](http://brew.sh) (only when on Mac OS X)
    * [Python 3.5](https://www.python.org) `% brew install python3`
    * [PostgreSQL](http://www.postgresql.org) `% brew cask install postgres`
    * [yajl](https://lloyd.github.io/yajl/) (optional) `% brew install yajl`

* Setup a Python 3.5 virtual environment to run the application using:

        % pyvenv ~/Library/Python/YaBaB
        % source ~/Library/Python/YaBaB/bin/activate

* Configure your environment to install and run the application:

        % export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin
        % export DATABASE_URL='postgresql://localhost/yabab'

* Install the needed requirements with:

        % pip install -r requirements.txt

* Create, initialize, and pre-populate the database named `yabab`:

        % psql < db.sql
        % python manage.py db init
        % python manage.py db migrate
        % python manage.py db update
        % psql < pre-populate.sql

* Run the application locally using [heroku-toolbelt](https://toolbelt.heroku.com):

        % heroku local

    or [gunicorn](http://gunicorn.org)

        % gunicorn -c gunicorn_conf.py yabab:app

* Access the application according to [Specification](#apidesign) below:

        % export API_HOST=http://localhost:500
        % curl -sL ${API_HOST}/api | json_reformat
        {
          "message": "Welcome to the YaBaB API",
          "version": "v0.0.1"
        }


## Database Design

|Customers||
|---|---|
|**ID**|Internal customer id
|**NAME**|The name of the customer

|Accounts||
|---|---|
|**ID**|Internal account id
|**ACCOUNT_NUMBER**|The account number used for transactions
|**CUSTOMER_ID**|Reference to the customer

|Transactions||
|---|---|
|**ID**|Internal account id
|**DATETIME**|The date and time of the transaction
|**ORIGINATOR_ID**|Reference to the account of the transaction originator
|**BENEFICIARY_ID**|Reference to the account of the transaction beneficiary
|**REFERENCE**|The purpose of the transaction|
|**AMOUNT**|The amount of the transaction


## API Design

|Create a new bank account for a customer, with an initial deposit amount|||
|---|---|---|
|URL|`/accounts`||
|Method|`POST`||
|Request Parameters|||
||`customer_id`|The customer_id to which the new account with be created for
||`initial_deposit`|The initial amount in the new account
|Response Codes|||
||`201`|An account belonging to `customer_id` with the number `account_number` and an initial deposit of `initial_deposit` was created
||`404`|A customer with `customer_id` does not exist
|Response JSON|||
||`201`|`{"account_number": "1234567890"}`
||`404`|`{"status": "error", "reason": "No customer with id customer_id found"}`

|Transfer amounts between any two accounts|||
|---|---|---|
|URL|`/transactions`||
|Method|`POST`||
|Request Parameters|||
||`amount`|The amount of the transaction
||`reference`|The purpose of the payment
||`originator`|The account number of the originator of the transaction
||`beneficiary`|The account number of the beneficiary of the transaction
|Response Codes|||
||`201`|The given `amount` was transferred from originator account_number to the beneficiary account_number
||`200`|There was an issue with the transaction, check
||`404`|An originator or beneficiary account with account_number does not exist
|Response JSON|||
||`201`|`{"transaction_id": "13243546"}`
||`200`|`{"status": "error", "reason": "Amount exceeds transaction limit"}`
||`404`|`{"status": "error", "reason": "Invalid originator account number :account_number"}`

|Retrieve balances for a given account|||
|---|---|---|
|URL|`/accounts/:account_number`||
|Method|`GET`||
|Request Parameters|||
||*None*||
|Response Codes|||
||`200`|An account with `account_number` was found and its balance is returned in the response
||`404`|An account with `account_number` does not exist
|Response JSON|||
||`200`|`{"amount": 1234.56}`
||`404`|`{"status": "error", "reason": "No account with number :account_number found"}`

|Retrieve transfer history for a given account|||
|---|---|---|
|URL|`/account/:account_number/transactions`||
|Method|`GET`||
|Request Parameters|||
||*None*||
|Response Codes|||
||`200`|An account with `account_number` was found and its transactions are returned in the response
||`404`|An account with `account_number` does not exist
|Response JSON|||
||`200`|`{"account_number": "1234567890", "transactions": [{"date": "2016-04-05", "amount": 1000.00", "reference": "Initial deposit", "originator": "1234567890", "beneficiary": "0987654321"] }`

|List available accounts|||
|---|---|---|
|URL|`/accounts`||
|Method|`GET`||
|Request Parameters|||
||`None`||
|Response Codes|||
||`200`|The list of available accounts is returned
|Response JSON|||
||`200`|`{"accounts": [{"customer": "Jane Woods", "customer_id": 1, "id": 5, number:"1234567890"}]}`
