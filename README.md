Welcome to Capstone, a casting agency. We provide an API for various casting roles to manage movies and actors.

# Set up

There are two aspects to run the project locally, backend and frontend.

## Backend

`python3 -m venv env`
`source env/bin/activate`
`pip install -r requirements.txt`
`source env_file && python app.py`

## Frontend

`cd frontend`
Auth0 expects the redirect URI to run on port 8080 so run with a local server such as:
`php -S localhost:8080`

# Roles
There are three roles of worker at the agency, each with specific permissions as to what they can use the API for:

- Casting assistant: `get:movies get:actors`
- Casting director: `get:movies get:actors add:actor delete:actor update:movie update:actor`
- Executive producer: `get:movies get:actors add:actor delete:actor update:movie update:actor add:movie delete:movie`

# Tests
Run:

`source env_file && python test_app.py`