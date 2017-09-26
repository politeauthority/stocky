import os

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
    os.environ.get('STOCKY_MYSQL_USER'),
    os.environ.get('STOCKY_MYSQL_PASS'),
    os.environ.get('STOCKY_MYSQL_HOST'),
    os.environ.get('STOCKY_MYSQL_PORT', 3306),
    os.environ.get('STOCKY_MYSQL_NAME'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
TESTING = False
THREADS_PER_PAGE = 2
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "0296686426"

# Secret key for signing cookies
SECRET_KEY = "3963963928"
APP_DATA_PATH = '/data/'
