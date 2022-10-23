# Description
Service for reading and writing user reactions. 

# Architecture

Requirements are following:

- The server will receive many more GET requests (95%) for the current hour than for hours in the past (5%).
- Most POST requests received by the server will contain a timestamp that matches the current timestamp (95%)
- Additional servers should be able to be spun up, at any time, without effecting the correctness of our metrics.

I've made following assumptions:

- There will be not many post request
- Availability and scalability of get requests are the most important,
    service can return outdated info for some time.

> **_NOTE:_** If it is not true, contact me to change the approach.

The system contains the followings parts:
- reader
- writer
- storage

Because there will be a lot of read requests and info are grouped by hour,
the reader service keeps data in the memory.
Usual year has 365 solar days + 5 hours 48 minutes 46 seconds.
So we will have *(~365 * 24 + 6)* * *number_of_years* * *message_size* 
it is not big number, so all the data can be placed in memory.

Reader services get the data at the startup. To keep the cache up-to-date reader
will request data from the storage in background task.

It could possibly lead to outdated data in get requests, but not more than
background task period. And because we make 
*number_of_reader_instances* / *update_period* request to db. And amount of the data
is small we can keep all the data in one instance of db. 
PostgreSQL were chosen, because it is quite good baseline.

Both services were implemented with abstract reader/writer class,
and dependency injections.
so in case PostgreSQL isn't suit requirements, there will be not many code
changes.

Writer service will write user reaction to the storage. 
The storage will not have any indexes, as we will read to the db more often
than read from it and writing operations should take as little time as possible.

Unfortunately, I have no time to add nginx for 
sharding/routing requests and path rewriting
as well as implement performance/integration tests.

There could be another approach: several writer sharded by username
(as it seems to be more evenly spread across request than timestamp)
and readers which collect data from all the writers (or its storages) 
and return sum of data in every writer. But such approach lead to big 
amount of network requests and big latency at get requests.
They can be decreased by using cache, but it will lead to the same
possibility of outdated info. So this approach wasn't implemented.

## Data definition

Data is organized in the table in the DB:

## user_reaction

```sql
CREATE TABLE user_reaction (
    id SERIAL, username VARCHAR(20) NOT NULL, 
    reaction VARCHAR(10) NOT NULL, 
    timestamp timestamp(3) without time zone NOT NULL, 
    PRIMARY KEY(id),
)
```

| id  | username | reaction    | timestamp |
|-----|----------|-------------|-----------|
| 1   | alex     | click       | x         |
| 2   | aleale   | impression  | x         |
| 3   | bob      | click       | x         |
| 4   | gleb     | impression  | x         |

No triggers or validations were added due to the lack of time 
(probably reaction require some).

# API

## Reader service

```shell
$ curl http://127.0.0.1:8000/analytics?timestamp={timestamp}
"unique_users,3\nclicks,3\nimpressions,0\n"
```

## Writer service

```shell
$ curl -X POST http://127.0.0.1:8000/analytics/{timestamp}/{username}/{click|impression}
```

# Initial setup

Docker containers are provided for running services. To build it you should run

```sh
docker build -t reaction-writer .
```

This will create a container with the name *reaction-writer*

# Running Containers

## API Service

### Docker container

You can start api container in the following way (assuming it called rates_api_service):

```sh
docker run -it -p 8000:8000 --name reaction-reader reaction-reader
```

### Run without docker

The service uses requirements.txt file for describing items necessary to run api.
Basic installation can be done with:

```sh
pip install requirements.txt
```

```sh
python main.py
```
