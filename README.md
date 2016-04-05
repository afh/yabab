# Yet Another Build A Bank

A backend banking API for the fictional YaBaB Savings Bank.

## TL;DR

1. Setup a [Python 3.5](https://www.python.org) virtual environment to run the application using:

        % pyvenv ~/Library/Python/YaBaB
        % source ~/Library/Python/YaBaB/bin/activate

2. Install the needed requirements with:

        % pip install -r requirements.txt

3. Run the application locally using [heroku-toolbelt](https://toolbelt.heroku.com):

        % heroku local

    or [gunicorn](https://toolbelt.heroku.com):

        % gunicorn -c gunicorn_conf.py yabab:app

4. Access the application according to [Specification](#apidesign) below:

        % curl -sL http://localhost:5000/ | json_reformat
        {
        "yabab.api": "v0.0.1"
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
||`404`|`{"status": "error", "reason": "Invalid customer id customer_id"}`

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
||`200`|`{"status": "error", "Amount exceeds transaction limit"}`
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
||`404`|`{"status": "error", "reason": "Invalid account number :account_number"}`

|Retrieve transfer history for a given account|||
|---|---|---|
|URL|`/transactions/:account_number`||
|Method|`GET`||
|Request Parameters|||
||*None*||
|Response Codes|||
||`200`|An account with `account_number` was found and its transactions are returned in the response
||`404`|An account with `account_number` does not exist
|Response JSON|||
||`200`|`{"account_number": "1234567890", "transactions": [{"date": "2016-04-05", "amount": 1000.00", "reference": "Initial deposit", "?"] }`
||`404`|`{"status": "error", "reason": "Invalid account number :account_number"}`
