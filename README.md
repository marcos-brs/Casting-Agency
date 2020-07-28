# Casting Agency

Here I had the chance to use all my knowledge acquired during the nanodegree to create an application from scratch.

This project is a Casting Agency and have two entities: actors and movies. It is possible to Create, Read, Update and Delete (CRUD) both the entities, as long as you have the permissions.

**Application URL to Heroku**: https://casting-agency-zerocoolbr.herokuapp.com/

### How setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `get:movies`
    - `post:actors`
    - `post:movies`
    - `patch:actors`
    - `patch:movies`
    - `delete:actors`
    - `delete:movies`
6. Create new roles for:
    - Casting Assistant
        - can `get:actors`
        - can `get:movies`
    - Casting Director
        - can perform all Casting Assistant
        - can `post:actors`
        - can `delete:actors`
        - can `patch:actors`
        - can `patch:movies`
    - Executive Producer
        - can perform all Casting Director
        - can `post:movies`
        - can `delete:movies`
        
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Casting Assistant, Casting Director and Executive Producer roles.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `casting-agency.postman_collection.json`
    - Right-clicking the collection folder for Casting Assistant, Casting Director and Executive Producer, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    
8. For the tests, update the tokens on `tests.py`

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

After update the database config on `models.py` file and the Auth0 config on `auth.py` file, follow the steps bellow

1. Set the environment variables

    ```bash
    export FLASK_APP=app.py;
    ```

2. Run the migrations

    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
   ```
   
3. Run the server

    ```bash
    flask run
   ```
   
4. If you want to run the tests
     ```bash
    python tests.py
   ```
   
   
### REST Endpoints

GET '/actors'
- Permission required: 'get:actors'
- Request parameters: None 
- Request body: None
- Returns an object with actors array
```json
{
    "actors": [
    {
        "age": 22,
        "gender": "male",
        "id": 2,
        "name": "Marcos"
    }]
}
```

GET '/movies'
- Permission required: 'get:movies'
- Request parameters: None 
- Request body: None
- Returns an object with movies array
```json
{
    "movies": [
    {
      "id": 4,
      "release_date": "Tue, 28 Jul 2020 12:06:17 GMT",
      "title": "Udacity - the movie"
    }]
}
```

POST '/actors'
- Permission required: 'post:actors'
- Request parameters: None 
- Request body: Object with the items to create a new actor
```json
{
    "name": "Marcos Santana",
    "age": 22,
    "gender": "male"
}
```
- Returns an object
```json
{
  "created": 10,
  "success": true
}
```

POST '/movies'
- Permission required: 'post:movies'
- Request parameters: None 
- Request body: Object with the items to create a new movie
```json
{
    "title": "Udacity - the movie",
    "release_date": "2020-07-28T12:06:17+00:00"
}
```
- Returns an object
```json
{
  "created": 5,
  "success": true
}
```

PATCH '/actors/<int:actor_id>'
- Permission required: 'patch:actors'
- Request parameters: None 
- Request body: Object with the items to update an actor
```json
{
    "name": "Marcos BR Santana",
}
```
- Returns an object
```json
{
  "updated": actor_id,
  "success": true
}
```

PATCH '/movies/<int:movie_id>'
- Permission required: 'patch:movies'
- Request parameters: None 
- Request body: Object with the items to update a movie
```json
{
    "title": "Udacity - the movie",
}
```
- Returns an object
```json
{
  "updated": movie_id,
  "success": true
}
```

DELETE '/actors/<int:actor_id>'
- Permission required: 'delete:actors'
- Request parameters: None 
- Request body: None
- Returns an object
```json
{
  "deleted": actor_id,
  "success": true
}
```

DELETE '/movies/<int:movie_id>'
- Permission required: 'delete:movies'
- Request parameters: None 
- Request body: None
- Returns an object
```json
{
  "deleted": movie_id,
  "success": true
}
```

If you have no token, you will receive the following response:
````json
{
  "code": "authorization_header_missing",
  "description": "Authorization header is expected."
}
````

If you have no permission to access an route, you will receive the following response:
````json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
````

If you token was already expired, you will receive the following response:
```json
{
  "code": "token_expired",
  "description": "Token expired."
}
```

to check for other errors due to authentication errors, check the `auth.py` file