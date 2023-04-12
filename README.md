
# Flask with MongoDB and Flask-RESTX using a Virtual Environment

This is a simple Flask application that uses MongoDB for data storage and Flask-RESTX for building a RESTful API. The application is built using a virtual environment and can be easily installed using pip.


## Prerequisites
Before you begin, make sure you have the following installed on your system:

- Python 3.6 or higher
- pip
- MongoDB
- Git (optional)


## Getting Started

Follow these steps to get started with the application:

1. Clone the repository (if you haven't already):

```
  git clone https://github.com/mustafainxiteout/flask-mongo.git
```

2. Create and activate a virtual environment:

```
  python3 -m venv venv
  source venv/bin/activate
```

3. Install the required packages using pip:

```
pip install -r requirements.txt
```

4. Start the Flask application:

```
flask run
```

5. Open the application in your browser at http://localhost:8000.



## Features
This application includes the following features:

- MongoDB integration for data storage
- Flask-RESTX for building a RESTful API
- CRUD operations for managing data

## File Structure
The file structure of this application is as follows:

```
├── app.py
├── config.py
├── requirements.txt
└── application
    ├── templates
    ├── __init__.py
    ├── models.py
    └── routes.py    
```

- `app.py` calls the main Flask application.
- `config.py` contains the configuration settings for the application.
- `requirements.txt` contains the required packages for the application.
- `application/__init__.py` contains the configuration for Flask.
- `application/models.py` contains the MongoDB models for the application.
- `application/routes.py` contains the Flask and RESTful API routes.
