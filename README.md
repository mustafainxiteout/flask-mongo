
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
  venv\Scripts\activate
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
- User Authentication and Hashing Password through Restful API

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

```
└── mongodb_files
     ├── courses.json
     └── users.json
```

- `courses.json` contains courses data to import in mongodb
- `users.json` contains users data to import in mongodb and password of it is hashed and stored in it. For the attached one, The password is `12345678`.

## Sending Verification and Reset Password Mails via Mailtrap.io

Mailtrap.io is a cloud-based fake SMTP server that allows software developers and testers to test and preview their email notifications without sending them to real users. It intercepts emails sent from development and staging environments and stores them in a test inbox for review. This allows developers to test the functionality of their email notifications in a safe environment, without risking the delivery of test emails to real users or spamming their inboxes. Mailtrap.io supports a variety of programming languages, frameworks, and tools, including Flask-Mail.

### Getting Started with Mailtrap.io

To get started with Mailtrap.io, you need to create an account on their website, and then create an inbox. You will then be given an SMTP username and password for your inbox, which you will use to send emails to your Mailtrap.io inbox.

### Flask-Mail

Flask-Mail is an extension that provides email sending capabilities for Flask applications. To use Mailtrap.io with Flask-Mail, you need to install Flask-Mail:

```
pip install Flask-Mail
```

After installing Flask-Mail, you need to configure it in your Flask application:

```
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_DEFAULT_SENDER'] = 'from@example.com'

mail = Mail(app)
```
In the above code, replace your_username and your_password with the SMTP username and password provided by Mailtrap.io.

### Sending Emails

To send an email with Flask-Mail, you need to create a message object:

```
from flask_mail import Message

html_body = render_template('verify_email.html', verify_url=verification_url)
msg = Message('Subject', sender='sender@example.com', recipients=['recipient@example.com'])
msg.html = html_body
```
In the above code, replace sender@example.com and recipient@example.com with the appropriate email addresses.

After creating the message object, you can send the email using the send method of the Mail object:
```
mail.send(msg)
```
The email will then be sent to your Mailtrap.io inbox, where you can view and test it.
