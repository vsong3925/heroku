import os

# Heroku check
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True

# Flask
from flask import Flask, request, render_template, jsonify

# SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine

# PyMySQL
import pymysql

# Pandas
import pandas as pd

# JSON
import json

# Import your config file(s) and variable(s)
if is_heroku == True:
    # if IS_HEROKU is found in the environment variables, then use the rest
    # NOTE: you still need to set up the IS_HEROKU environment variable on Heroku (it is not there by default)
    remote_db_endpoint = os.environ.get('remote_db_endpoint')
    remote_db_port = os.environ.get('remote_db_port')
    remote_db_name = os.environ.get('remote_db_name')
    remote_db_user = os.environ.get('remote_db_user')
    remote_db_pwd = os.environ.get('remote_db_pwd')
else:
    # use the config.py file if IS_HEROKU is not detected
    from config import remote_db_endpoint, remote_db_port, remote_db_name, remote_db_user, remote_db_pwd

# Configure MySQL connection and connect 
pymysql.install_as_MySQLdb()
engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

# Initialize Flask application
app = Flask(__name__)

# Set up your default route
@app.route('/')
def home():
    return render_template('index.html')

# set up the data route
@app.route('/api/data/students')
def get_students():

    # Establish DB connection
    conn = engine.connect()
    
    query = '''
        SELECT
            StudentID
            ,LastName
            ,FirstName
            ,MiddleName
        FROM
            student
        ORDER BY
            LastName
            ,FirstName
            ,MiddleName
        '''
    
    student_data = pd.read_sql(query, con=conn)
    student_json = student_data.to_json(orient='records')

    conn.close()
    return student_json

if __name__ == "__main__":
    app.run(debug=True)