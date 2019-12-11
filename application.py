# Basic mod_WSGI file for AWS which REQUIRES the term "application" for the flask app
from my_app import application

if __name__ == '__main__':
    application.run()
