# Casting-Agent-API

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

##### Key Dependencies

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
  * View Movies (get:movies)
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

#### GET /api/categories
* General
  * Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  * Request Arguments: None
  * Returns: JSON with a single key, categories, that contains a object of id: category_string key:value pairs. 
* Sample request:
  `curl http://localhost:5000/api/categories`
* Sample return:
    ```json
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "success": true
    }
    ```

#### GET /api/questions
* General
  * Fetches the questions to display on the main page
  * Request Qrguments: None
  * Returns: JSON consists of a list of questions, a dicionary of category object, success value, current category, total number of questions
* Sample request:
  `curl http://localhost:5000/api/questions`
* Sample return:
    ```json
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "current_category": "History", 
        "questions": [
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            ...
        ], 
        "success": true, 
        "total_questions": 29
    }
    ```

#### POST /api/questions
* General
  * Create a new question
  * Request Arguments: JSON
    * question - String, stating the content of question
    * answer - String, answer to the question
    * category - String, which category does this question belong to
    * difficulty - Integer, the difficult level of this question ranging from 1-5
  * Returns: JSON with a single key, categories, that contains a object of id: category_string key:value pairs. 
* Sample request
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"question":"q","answer":"a","category":"1","difficulty":1}' http://localhost:5000/api/questions
  ```
* Sample return
    ```json
    {
        "created": 35, 
        "questions": [
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            ...
        ], 
        "success": true, 
        "total_questions": 30
    }
    ```
#### DELETE /api/questions/<question_id>
* General
  * Delete a specific question
  * Request Arguments: question id
  * Returns: JSON with success value, deleted question id, a list of questions, the number of total questions
* Sample request
  `CURL -X DELETE http://localhost:5000/questions/34`
* Sample return
    ```json
    {
        "deleted": "34", 
        "questions": [
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            ... 
        ], 
        "success": true, 
        "total_questions": 28
    }

    ```
#### POST /api/search
* General
  * Search related questions based on a keyword
  * Request Arguments: JSON
    * searchTerm: String, the search term a user wants to use
  * Returns: JSON consists of success value, related questions, total of search results, current category
* Sample request
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"What"}' http://localhost:5000/api/search
  ```
* Sample return
    ```json
    {
        "current_category": "History", 
        "questions": [
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Edward Scissorhands", 
            "category": 5, 
            "difficulty": 3, 
            "id": 6, 
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }, 
            {
            "answer": "Muhammad Ali", 
            "category": 4, 
            "difficulty": 1, 
            "id": 9, 
            "question": "What boxer's original name is Cassius Clay?"
            }, 
            {
            "answer": "Lake Victoria", 
            "category": 3, 
            "difficulty": 2, 
            "id": 13, 
            "question": "What is the largest lake in Africa?"
            }, 
            {
            "answer": "The Liver", 
            "category": 1, 
            "difficulty": 4, 
            "id": 20, 
            "question": "What is the heaviest organ in the human body?"
            }
        ], 
        "success": true, 
        "total_questions": 5
    }

    ```

#### GET /api/categories/<id>/questions
* General
  * Fetches the questions based on category
  * Request Qrguments: None
  * Returns a JSON consists of a list of questions, a dicionary of category object, success value, current category, total number of questions
* Sample request:
  `curl http://localhost:5000/api/categories/5/questions`
* Sample return:
    ```json
    {
        "current_category": "Entertainment", 
        "questions": [
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Edward Scissorhands", 
            "category": 5, 
            "difficulty": 3, 
            "id": 6, 
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }
        ], 
        "success": true, 
        "total_questions": 2
    }
    ```

#### POST /api/quizzes
* General
  * Get one question based on category and previous answerd question
  * Request Arguments: JSON
    * previous_questions: String, the previous questions appeared before current question
    * quiz_category: String, the category of the question
  * Returns: JSON consists of success value, one random choosen question
* Sample request
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}' http://localhost:5000/api/quizzes
  ```
* Sample return
    ```json
    {
        "question": {
            "answer": "easy answer", 
            "category": 1, 
            "difficulty": 1, 
            "id": 28, 
            "question": "Test Question"
        }, 
        "success": true
    }
    ```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```