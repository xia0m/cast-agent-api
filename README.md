# Casting-Agent-API

This project is a backend API developed using Flask. At the moment, this API contians 2 models, Movie and Actor, and it consists of 4 movie, 4 actor API end points. An authenticated user is able to view, add, update, delete a movie or actor. Anyone can extend this project by add more models in models.py or add more API end points in routes folder.

Table of contents
=================
- [Casting-Agent-API](#casting-agent-api)
- [Table of contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Installing Dependencies](#installing-dependencies)
      - [Python 3.7](#python-37)
      - [Virtual Enviornment](#virtual-enviornment)
      - [PIP Dependencies](#pip-dependencies)
  - [Database Setup](#database-setup)
  - [Running the server](#running-the-server)
  - [API Reference](#api-reference)
    - [Getting Started](#getting-started-1)
    - [Error Handling](#error-handling)
    - [Authorization](#authorization)
    - [Endpoints](#endpoints)
      - [GET /movies](#get-movies)
      - [GET /movies/<id>](#get-moviesid)
      - [POST /movies](#post-movies)
      - [DELETE /movies/<id>](#delete-moviesid)
      - [UPDATE /movies/<id>](#update-moviesid)
      - [GET /actors](#get-actors)
      - [GET /actors/<id>](#get-actorsid)
      - [POST /actors](#post-actors)
      - [DELETE /actors/<id>](#delete-actorsid)
      - [UPDATE /actors/<id>](#update-actorsid)
  - [Testing](#testing)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
This project is using [Postgresql](https://www.postgresql.org/download/) as database. After install postgresql, [start](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html) the PostgreSQL Server.

Create a new database named **cast_test**
```bash
createdb cast_test
```

## Running the server

To run the Flask server, ensure you are working using your created virtual environment and execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 


## API Reference

### Getting Started
* Base URL: If you want to run your app locally, the app is hosted at the default, `http://localhost:5000`.
* Authentication: This version of the application is using [Auth0](https://auth0.com/) as authentication method.

### Error Handling
Errors are returned as JSON object in the following format:
```json
{
    "success":False,
    "error":400,
    "message":"Bad Request"
}
```
The API will return five error types when requests fail:
* 404: resource not found
* 405: Method Not Allowed
* 422: unprocessable
* 500: Internal Server Error
* AuthError:
  * The Authentication token is expired
  * The claims is invalid
  * the token is invalid
  * the JWT doesnt' contain the proper action

### Authorization
RBAC(Role-based access control) are enabled by default. There are three roles:
* Casting Assistant
  * View actors (get:actors)
  * View movies (get:movies)
* Casting Director
  * All permissions a Casting Assistant has had
  * Add actor (add:actor)
  * Delete actor (delete:actor)
  * Update actor (modify:actor)
  * Update movie (modify:movie)
* Executive Producer
  * All permissions a Casting Director has had
  * Add movie (add:movie)
  * Delete movie (delete:movie)

### Endpoints

#### GET /movies
* General
  * Fetches a list of movies
  * Request Arguments: JWT Authorization token that has permission 'view:movies'
  * Returns: JSON with a list of serialized movie object
* Sample request:
  `curl -H "Authorization: Bearer <JWT Token>" http://localhost:5000/movies`
* Sample return:
    ```json
    {
    "movies": [
        {
            "id":1,
            "title":"2012"
        },{
            "id": 2,
            "title": "Random Movie"
        }
    ], 
    "success": true
    }
    ```

#### GET /movies/<id>
* General
  * Fetches a specific movie based on id
  * Request Qrguments: JWT Authorization token that has permission 'view:movie'
  * Returns: JSON consists of a serialized movie object
* Sample request:
  `curl -H "Authorization: Bearer <JWT Token>" http://localhost:5000/movies/<id>`
* Sample return:
    ```json
    {
        "success": true,
        "movies": {
            "id":1,
            "title":"Sally",
            "release_date":"Fri, 21 Feb 2020 00:00:00 GMT",
            "actors":[{
                "id":1,
                "name":"Tom Hanks",
                "gender":"Male",
                "age":65,
                "movie_id":1
            }]
        }
        
    }
    ```

#### POST /movies
* General
  * Create a new movie
  * Request Arguments: JSON
    * title - String, the title of the new movie
    * release_date - Date, the release date of the new movie
    * JWT Authorization token that has permission 'add:movie'
  * Returns: JSON with a list of serialized movie object
* Sample request
  ```bash
  curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <JWT Token>" -d '{"title":"Sally","release_date":"01/01/2016"}' http://localhost:5000/movies
  ```
* Sample return
    ```json
    {
        "movies": [
        {
            "id":1,
            "title":"2012"
        },{
            "id": 2,
            "title": "Random Movie"
        }
    ], 
        "total_movies":1,
        "success": true, 
    }
    ```
#### DELETE /movies/<id>
* General
  * Delete a specific movie
  * Request Arguments: movie id, JWT Authorization token that has permission 'delete:movie'
  * Returns: JSON with success value, deleted movie id, a list of serialized movie object
* Sample request
  `CURL -X DELETE  -H "Authorization: Bearer <JWT Token>" http://localhost:5000/movies/2`
* Sample return
    ```json
    {
        "deleted": "2", 
        "movies": [
        {
            "id":1,
            "title":"2012"
        },{
            "id": 2,
            "title": "Random Movie"
        }
    ], 
        "success": true, 
    }

    ```

#### UPDATE /movies/<id>
* General
  * Update a specific movie
  * Request Arguments: movie id, Authorization Header contains JWT token that has 'modify:movie' permission, JSON format of movie attritube that needs to be updated
  * Returns: JSON with success value, updated movie id, a list of serialized movie object
* Sample request
  ```bash
  curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <JWT Token>" -d '{"title":"Sally 2","release_date":"01/01/2021"}' http://localhost:5000/movies/2
  ```
* Sample return
    ```json
    {
        "updated": "2", 
        "movies": [
        {
            "id":1,
            "title":"2012"
        },{
            "id": 2,
            "title": "Random Movie"
        }
    ], 
        "success": true, 
    }

    ```

#### GET /actors
* General
  * Fetches a list of actors
  * Request Arguments: JWT Authorization token that has permission 'view:actors'
  * Returns: JSON with a list of serialized actor object
* Sample request:
  `curl -H "Authorization: Bearer <JWT Token>" http://localhost:5000/actors`
* Sample return:
    ```json
    {
    "actors": [
        {
            "id":1,
            "name":"Tom Hanks",
            "age":57,
            "gender":"Male",
            "movie_id":1
        }
    ], 
    "success": true
    }
    ```

#### GET /actors/<id>
* General
  * Fetches a specific actor based on id
  * Request Qrguments: actor id, JWT Authorization token that has permission 'view:actor'
  * Returns: JSON consists of a serialized actor object
* Sample request:
  `curl -H "Authorization: Bearer <JWT Token>" http://localhost:5000/actors/<id>`
* Sample return:
    ```json
   {
    "actor": {
        "age": 65,
        "gender": "Male",
        "id": 1,
        "movie_id": 1,
        "name": "new_test_name"
    },
    "success": true
}
    ```

#### POST /actors
* General
  * Create a new actor
  * Request Arguments: JSON
    * title - String, the title of the new actor
    * release_date - Date, the release date of the new actor
    * JWT Authorization token that has permission 'add:actor'
  * Returns: JSON with a list of serialized actor object
* Sample request
  ```bash
  curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <JWT Token>" -d '{"name":"Tom Hankds", "age":57, "gender":"Male","movie_id":1}' http://localhost:5000/actors
  ```
* Sample return
    ```json
    {
    "actors": [
        {
            "id":1,
            "name":"Tom Hanks",
            "age":57,
            "gender":"Male",
            "movie_id":1
        }
    ], 
    "total_actors":1,
    "success": true
    }
    ```
#### DELETE /actors/<id>
* General
  * Delete a specific actor
  * Request Arguments: actor id, JWT Authorization token that has permission 'delete:actor'
  * Returns: JSON with success value, deleted actor id, a list of serialized actor object
* Sample request
  `CURL -X DELETE  -H "Authorization: Bearer <JWT Token>" http://localhost:5000/actors/2`
* Sample return
    ```json
    {
        "deleted": "2", 
        "actors": [
        {
            "id":1,
            "name":"Tom Hanks",
            "age":57,
            "gender":"Male",
            "movie_id":1
        }
    ], 
        "success": true, 
    }

    ```

#### UPDATE /actors/<id>
* General
  * Update a specific actor
  * Request Arguments: actor id, Authorization Header contains JWT token that has 'modify:actor' permission, JSON format of actor attritube that needs to be updated
  * Returns: JSON with success value, updated actor id, a list of serialized actor object
* Sample request
  ```bash
  curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <JWT Token>" -d '{"name":"Tom Holland","release_date":"01/01/2021"}' http://localhost:5000/actors/1
  ```
* Sample return
    ```json
    {
        "updated": "2", 
        "actors": [
        {
            "id":1,
            "name":"Tom Holland",
            "age":57,
            "gender":"Male",
            "movie_id":1
        }
    ], 
        "success": true, 
    }

    ```




## Testing
To run the tests, run
```
dropdb cast_test
createdb cast_test
python test_app.py
```