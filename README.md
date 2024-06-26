Checkbox API


### Description: 
Checkbox API allows to create and authenticate users,
create, get and filter checks, generate text representation of the check.


## Installation:

Clone the project and then go to the root directory and create .env and .env.test files like in .env.examples 
(You might want to change the credentials). Then you can install app:


### 1. Installation with docker:

Go to the root dir, build and start containers:

```commandline
docker-compose up
```

Then apply migrations:

```commandline
docker-compose exec backend alembic upgrade head
```

### 2. Manual installation:

First install the dependencies from the pyproject.toml file 
(you will need poetry, so if you don't have it, install it using the 'pip install poetry' command):

```commandline
poetry install
```
Run app:
```commandline
uvicorn app.main:app
```

Then apply migrations:

```commandline
alembic upgrade head
```

## Usage:

Endpoints description is available in Checkbox.postman_collection.json

Swagger documentation is available at http://127.0.0.1:8000/docs#/


## Testing:

To run tests:

```commandline
docker-compose -f docker-compose-test.yml up --abort-on-container-exit
```

Note, sometimes the application starts before the database and the tests 
may not run, in that case just run this command again