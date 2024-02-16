# University rating system

A fully functional dummy application to be used for a grade grading system for the National University..


# Prerequisites

## Python

This project uses python 3.12. Make sure you install the correct version of python before proceeding.

# Running the project

Dependency management is done using [Virtualenv Enviorenment]. For local development, the recommended way is to create virtual environment:
```shell
$ python3 -m venv env
```

You will also have to activate the virtual environment:

```shell
/venv/bin/activate
```

Install both the development dependencies and the deployment dependencies (fastapi, uvicorn, etc).

```shell
pip install requirements.txt
```

The project can be run with the command:

```shell
uvicorn main:app --reload
```


## Documentation

By default, FastAPI provides basic documentation for your endpoints in http://localhost:8000/docs

## Creating new migrations

```shell
alembic init alembic
```

Generate migration

 ```shell
alembic revision --autogenerate -m "name_migration"
 ```
Apply migration:
 ```shell
alembic upgrade head
 ```

## TODO
* Add jwt authentication to endpoints
* Unit test
* Linters (pytest, mypy, pylint)