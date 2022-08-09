# toy-redis
Basic Version of Redis implementing core features

## How to Use

1. Run Server in command line -> Add command
2. Run Client(s) in command line -> Add command
3. Input commands into client command line

## Features
See below the features included in this implementation of Redis

### Ping
Ping the server to check if responsive
```
PING
```

### Echo
Get response from the server
```
ECHO <value>
```

### Get
Get the value corresponding to the key in the data store
```
GET <key>
```

### Set
Insert into the data store a key value pair with optional expiration time. EX donotes seconds and PX milliseconds.
```
SET <key> <value> [EX|PX <time>]
```

### Expire
Set an expiry time on a key in currently in the data store. Default unit is EX.
```
EXPIRE <key> [EX|PX]
```

## Run Tests
Below are the commands to run the tests to verify the code is functioning properly

Insert commands here
