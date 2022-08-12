# Redis in Python
Basic version of Redis implementing core features such as get, set, and expire.

See my medium article on my process here: https://medium.com/me/notifications

See my demo video here: <Add>

## How to Use

1. Create two command line terminals in the main project directory (/toy-redis)
1. Run Server in a command line -> ```python -m app.client.client```
2. Run Client(s) in another command line -> ```python app/server/main.py```
3. Input commands into client command line (see below)

## Features
See below the features included in this implementation of Redis.

### Ping
Ping the server to check if it is responsive.
```
PING
```

### Echo
Get response from the server.
```
ECHO <value>
```

### Get
Get the value corresponding to the key in the data store.
```
GET <key>
```

### Set
Insert into the data store a key value pair with optional expiration time. EX donotes seconds and PX milliseconds.
```
SET <key> <value> [EX|PX <time>]
```

### Expire
Set an expiry time on a key in currently in the data store. Default unit is PX.
```
EXPIRE <key> [EX|PX] <time>
```

## Run Tests
Below are the commands to run the tests to verify the code is functioning properly. 

### RESP Encoder Test
To ensure the Redis Protocol (RESP) encoding is still working according to plan.
```
python -m unittest -v tests.test_resp_encoder
```

### App Test
Intergration testing the entire app by testing all the commands in an end-to-end style. Note that the server must be running in a separate command line first.
```
python -m unittest -v tests.test_app
```


