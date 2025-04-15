# Superhero Code API

## Description
The *Superhero Code API* is a Flask-based RESTful API that allows users to manage heroes, their powers, and the relationbaships between them. The API supports CRUD operations for heroes and powers, as well as validations to ensure data integrity.

## Features
- Retrieve a list of all heroes and their details
- Fetch details of a specific hero by ID
- Retrieve a list of all powers
- Fetch and update details of a specific power
- Create hero-power relationships with strength validation

## Technologies Used
- *Python 3*
- *Flask*
- *Flask-SQLAlchemy*
- *Flask-Migrate*
- *SQLite* (or any SQL database)

## Installation & Setup
### Prerequisites
Ensure you have Python installed on your machine. You can check by running:
bash
python --version


### Clone the Repository
bash
```
git clone git@github.com:geekirui120/Superhero-Code-API.git
cd Superhero-Code-API
```

### Create a Virtual Environment
bash
```
python -m venv env
source env/bin/activate
```

### Install Dependencies
bash
```
pip install -r requirements.txt
```

### Database Setup
Initialize and migrate the database:
bash
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Seed the Database (Optional)
bash
```
python seed.py
```

## Running the Application
bash
```
flask run
```
The server will start at http://127.0.0.1:5000/

## API Endpoints

### Heroes
#### Get all heroes
http
GET /heroes

*Response:*
json
[
  {
    "id": 1,
    "name": "Superman",
    "super_name": "Clark Kent"
  }
]


#### Get a hero by ID
http
GET /heroes/<id>

*Response:*
json
{
  "id": 1,
  "name": "Superman",
  "super_name": "Clark Kent"
}


### Powers
#### Get all powers
http
GET /powers

*Response:*
json
[
  {
    "id": 1,
    "name": "Flight",
    "description": "Ability to fly"
  }
]


#### Update power description
http
PATCH /powers/<id>

*Request Body:*
json
{
  "description": "Enhanced speed and strength"
}


### Hero Powers
#### Assign a power to a hero
http
POST /hero_powers

*Request Body:*
json
{
  "strength": "Strong",
  "hero_id": 1,
  "power_id": 2
}


*Response:*
json
{
  "id": 1,
  "strength": "Strong",
  "hero_id": 1,
  "power_id": 2
}


## Validations
- strength must be one of: "Strong", "Weak", "Average".
- description of power cannot be empty.

## License
This project is licensed under the MIT License.

