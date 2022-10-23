# Description
HTTP-based API returns a list with the average prices for each day on 
a route between two destinations (ports or regions)

The project consist of two folders: db and routes_api_service.

# Getting started

Both service and db can be started with docker compose

```sh
docker compose up
```

to check the service, you can run following command:

```sh
curl "http://localhost:8080/rates?date_from=2016-01-02&date_to=2016-01-10&origin=china_main&destination=north_europe_main"
```

or just open this link in your browser.

In case of any problem, please check you env settings,
you can check list of env setting for api in `routes_api_service/settings.py`.
And do not hesitate to ask me `kaltovichartyom@gmail.com` :). 

# Data definition

Data is organized in two tables:

## Destinations

|name|slug|path|is_port|
|----|----|----|-------|
|China Main|china_main|china_main|false|
|Northern Europe|northern_europe|northern_europe|false|
|Reykjavík|ISREY|northern_europe.scandinavia.ISREY|true|
|Bilbao|ESBIO|northern_europe.north_europe_sub.ESBIO|true|

It contains routes destinations, which can be either port, or regions
containing several ports or other regions.

``path`` column defines destination hierarchy, 
while ``is_port`` flag is used to differentiate ports and regions.
``name`` and ``slug`` seems to be self-explanatory.


## Prices

|orig_code|dest_code|day|price|
|---------|---------|---|-----|
|CNGGZ|EETLL|2016-01-01|1244|
|CNGGZ|EETLL|2016-01-01|1140|

## Other

The db contains 3 indexes for now: for ``path`` column of ``Destinations``
and for ``orig_code`` and ``dest_code`` of ``Prices``.
No triggers, procedures or constraints presented for now.

> **_NOTE:_**  You can see db creating scrypt in `rates.sql` file.

# HTTP-based API

`routes_api_service` contains HTTP-based API capable of handling the GET 
request described below:

API endpoint takes the following parameters:

* date_from
* date_to
* origin
* destination

and returns a list with the average prices for each day on a route between port codes 
*origin* and *destination*. 
Return an empty value (JSON null) for days on which there are less than 
*3* prices in total.

Both the *origin, destination* params accept either port codes or region slugs, 
making it possible to query for average prices per day between geographic 
groups of ports.

## Usage

    curl "http://127.0.0.1/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"

    [
        {
            "day": "2016-01-01",
            "average_price": 1112
        },
        {
            "day": "2016-01-02",
            "average_price": 1112
        },
        {
            "day": "2016-01-03",
            "average_price": null
        },
        ...
    ]

## Extra details

The api service is implemented in python with usage of Flask framework.
It also contains integration and performance tests in `tests\integration_tests`
and `tests\perf_test` folders.

# Initial setup

Docker containers are provided for running services. To build it you should run

```sh
docker build -t ratestask .
```

This will create a container with the name *ratestask*

# Running Containers

## DB container

You can start db container in the following way (assuming it called ratestask):

```sh
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```

It is started with the default user `postgres` and `ratestask` password.

```sh
PGPASSWORD=ratestask psql -h 127.0.0.1 -U postgres
```

alternatively, use `docker exec` if you do not have `psql` installed:

```sh
docker exec -e PGPASSWORD=ratestask -it ratestask psql -U postgres
```

Keep in mind that any data written in the Docker container will
disappear when it shuts down. The next time you run it, it will start
with a clean state.

## API Service

### Docker container

You can start api container in the following way (assuming it called rates_api_service):

```sh
docker run -it -p 8080:8080 --name rates_api_container rates_api_service
```

### Run without docker

The service uses requirements.txt file for describing items necessary to run api.
Basic installation can be done with:

```sh
pip install requirements.txt
```

If you want to run tests, you should install dev dependencies:

```sh
pip install requirements-dev.txt
```

The service can be started with following command:

```sh
python routes_api_service/main.py
```

### nox

[nox](https://nox.thea.codes/en/stable/) is used for running test and formatters.

- to check existed commands run:

```sh
nox -l
```

- to run any session type:

```sh
nox -s black
```

> **_NOTE:_**  nox create separated virtual environment for every command
> at every run. To avoid to add `-r` flag to your commands e.g.:

```sh
nox -s black -r
```

To run all checks type:

```sh
nox
```

> **_NOTE:_** Integration and performance tests execute
> http requests to API, and
> for now nox doesn't support shared virtual environments,
> so every check will use their own ones.
> So such command can take some time.