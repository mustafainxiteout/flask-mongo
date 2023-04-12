import os

class Config(object):
    # A secret key is used to keep the client-side sessions secure. Here, the key is taken from an environment variable
    # named 'SECRET_KEY'. If it doesn't exist, a default string 'secret_string' is used as the secret key.
    SECRET_KEY=os.environ.get('SECRET_KEY') or "secret_string"

    # MongoDB settings are defined as a list of dictionaries, with each dictionary representing a MongoDB instance.
    # Here, a single MongoDB instance is defined with a database name 'UTA_Enrollment', host address '127.0.0.1',
    # port number '27017', and an alias 'default'.
    MONGODB_SETTINGS=[ {"db": "UTA_Enrollment","host": "127.0.0.1","port": 27017,"alias": "default"}]