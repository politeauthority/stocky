import os

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
    os.environ.get('STOCKY_MYSQL_HOST'),
    os.environ.get('STOCKY_MYSQL_USER'),
    os.environ.get('STOCKY_MYSQL_PASS'),
    os.environ.get('STOCKY_MYSQL_PORT'),
    os.environ.get('STOCKY_MYSQL_NAME'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
TESTING = True
THREADS_PER_PAGE = 2

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

APP_DATA_PATH = os.environ.get('PA_APP_DATA_PATH', '/home/alix/pas_data/')
