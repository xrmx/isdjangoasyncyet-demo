# isdjangoasyncyet-demo

This is a demo for the talk *Is Django async yet?*.

## Requirements

A Docker Compose V2 file is provided to run the Postgresql database.

You can start the database with:

```
docker compose up
```

On another shell you can create the virtual environment and install the requirements:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## How to run the sync demo

This assumes the environment has been created and is activated.

You can start the async application with the following command:

```
cd demo
gunicorn demo:wsgi --workers 1 --bind 0.0.0.0:8000
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## How to run the async demo

This assumes the environment has been created and is activated.

You can start the async application with the following command:

```
cd ademo
gunicorn ademo.asgi:application --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

The API will be available at [http://localhost:8080](http://localhost:8080).
