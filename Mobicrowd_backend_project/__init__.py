# Import future features for compatibility
from __future__ import absolute_import, unicode_literals

# Ensure that pymysql is used in place of MySQLdb
import pymysql

try:
    pymysql.install_as_MySQLdb()
except Exception as e:
    # Log the exception or handle it as appropriate
    print(f"Error installing pymysql as MySQLdb: {e}")

# Import the Celery app to ensure it is always imported when Django starts
from .celery import app as celery_app

# Define the public interface of the module
__all__ = ('celery_app',)
