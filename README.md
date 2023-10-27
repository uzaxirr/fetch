Demo Video 
https://www.loom.com/share/20ef5492b1bd4738a20185b1a70f997a?sid=b5ceaa66-b2be-4f6b-bfd9-26544fdd7295

# Setup
This assumes that you have a postgres DB on port 5432 and a redis server running on 6379. I didn't dockerized the project.
**Set up a Virtual Environment**
```
# Install virtualenv if not installed 
pip install virtualenv 

# Create a virtual environment 
virtualenv venv 

# Activate the virtual environment  
# On macOS and Linux:  source venv/bin/activate
```

**Install Dependencies**
Navigate to the project directory (if not already) and install the required packages using the `requirements.txt` file.
```
pip install -r requirements.txt
```

**Database Setup** run  initialisation or migration scripts.
```
python manage.py migrate
```

**Run the Server and celery task**
in two different terminal sessions run the below cmds

`python manage.py runserver`

and 


`celery -A fetch worker --loglevel=info`

# Optimisation in reading from Database

## Using Read Replica DB
Another way to optimize reading from DB is to use a read replica. We can offload all the reading operation to a replica DB which will specifically used for reading while the primary DB will be used for all the major write operations and this ensures that those writes are not slowed down by concurrent read.
This also reduces network latency if application serves from various geographical locations

### Drawbacks
This replication is not always a smooth process there may be a lag btwn the master & slave DB. Thus we need to have a robust data sync pipeline to sync data from primary to read replica and mantaining this sync is again a overhead for the master DB.
And there may be instances where there may be issues with the replicated data this can be due to various reasons – network glitches, disk errors, bugs, or issues with the replication configuration.

Also if any migrations are made they needed to be executed on both the DBs.

## Key Features

### IP Based throttling
Both the APIs have an IP Based throttling of 10req/min

### Queuing
When an POST request is received to populate data into DB it is not directly inserted instead a task is fired up and that task populate the data into DB

###  Insert Query Optimisation
Instead of using INERT INTO for each transaction. All the transactions are created at once using the multirow values syntax that Postgres supports
https://www.postgresql.org/docs/9.4/sql-insert.html

I've optimized it further by making it insert in batches of 100.
This will create records in batches of 100. If you have, for instance, 500 transactions are to be insterted then it will perform 5 separate insert operations with 100 records each.

### Pagination
The list API is fully paginated with a default page size of 10. This prevents fetching all results from the DB at once. Helpful when the list API have to get a lot of transactions.

### Caching
The list API supports caching via Redis and TTL is 300sec for it.

### DB Pooling
I've also added DB pooling so that server may not make a new DB connection for every request instead use the old connection from pool.
The default pool size is 5 connections. I've implement it using a custom class for pooling called `ConnectionPool`  (can be found in `fetch/pooling.py`)

## API Specs

For your convinence i've also created a script that would generate some dummy payload for testing purpose.
In the project root run `python payload.py` and enter the number of transactions you want in the payload when prompted in your terminal session.
this will create a `payload.json` file in the root dir itself. You can use it's content for testing purpose. 

### Create Transactions

The below cURL will create a Transaction in DB


```
curl --location 'http://127.0.0.1:8000/api/txn/' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "payer": "0x12345ExamplePayerAddress00001",
        "receiver": "dummy@pay1",
        "action": [
            {
                "transaction": {
                    "tx": "0xabcdef000000000001",
                    "chain": 2,
                    "type": "OTHER"
                }
            },
            {
                "type": "PAYMENT",
                "data": {
                    "token": "0x98765ExampleTokenAddress00001",
                    "chain": 2,
                    "receiver": "0x67890ExampleReceiverAddress00001",
                    "amount": {
                        "amount": "251",
                        "currency": "CRYPTO"
                    }
                }
            }
        ],
        "message": "Hello World1",
        "label": "451",
        "signature": "0xabcdef000001"
    }
]'
```

### Get Transactions

The below cURL will list all the Transactions available in the DB in a paginated manner.

```
curl --location 'http://127.0.0.1:8000/api/txn/list/' \
--data ''
```

