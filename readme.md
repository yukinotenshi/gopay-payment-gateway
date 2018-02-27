[Gojek] Gopay Payment Gateway
-----

> Microservice for handling payments received with Gopay written in Python 3 using Flask microframework.

## Installation

* Install the requirements first
    ```sh
    pip install -r requirements.txt
    ```
    
* Run setup.py
    ```sh
    python setup.py
    ```
    You will be asked about your Gojek account credentials and SMS OTP

* Run the app!
    Dev mode :
    ```sh
    python app.py
    ```
    or in production using gunicorn and gevent :
    ```sh
    gunicorn app:app -k gevent -b 0.0.0.0:80
    ```
    

## Usage

*   Take note of your private key, which is randomized from setup. The key is located in `config.py` as `API_KEY`

* Generate a transaction :
    Endpoint :
    `http(s)://[host]/generate`
    Method :
    `POST`
    Data:
    ```javascript
    {
        "amount" : INTEGER,
        "key" : API_KEY
    }
    ```
    
    Amount represent base amount
    
    Response :
    ```javascript
    {
        "status" : "success",
        "amount" : BASE_AMOUNT + RANDOM INTEGER,
        "id" : INTEGER
    }
    ```
    
    Random integer will be added to BASE_AMOUNT to make the payment unique. Id is the transaction ID on database.
    
* Check a transaction
    Endpoint :
    `http(s)://[host]/confirm`
    Method :
    `POST`
    Data :
    ```javascript
    {
        "limit" : INTEGER,
        "id" : INTEGER,
        "key" : API_KEY
    }
    ```
    Where ID is the transaction ID and limit is the number of transaction on gopay history that will be checked.
    Return:
    ```javascript
    {
        "confirmed" : BOOLEAN,
        "status" : "success" or "fail"
    }
    ```
    Confirmed will be `True` if the payment already received.
    
## Additional Info
1. Transaction only last for the day it was created.
2. The API used is not officially publicated by GOJEK
