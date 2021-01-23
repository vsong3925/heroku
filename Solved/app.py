# import necessary libraries
import os
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True

import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from sqlalchemy import func, create_engine

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



app = Flask(__name__)

engine = create_engine('sqlite:///db/pets.sqlite')

# create route that renders index.html template
@app.route("/")
def home():    
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    conn = engine.connect()

    if request.method == "POST":
        name = request.form["petName"]
        pet_type = request.form["petType"]
        age = request.form["petAge"]

        pets_df = pd.DataFrame({
            'name': [name],
            'type': [pet_type],
            'age': [age]
        })

        pets_df.to_sql('pets', con=conn, if_exists='append', index=False)

        return redirect("/", code=302)

    conn.close()

    return render_template("form.html")

@app.route("/api/pals-summary")
def pals_summary():
    conn = engine.connect()
    
    query = '''
        SELECT 
            type,
            COUNT(type) as count
        FROM
            pets
        GROUP BY
            type
    ''' 

    pets_df = pd.read_sql(query, con=conn)

    pets_json = pets_df.to_json(orient='records')

    conn.close()

    return pets_json

@app.route("/api/pals")
def pals():
    conn = engine.connect()
    
    query = '''
        SELECT 
            *
        FROM
            pets
    ''' 

    pets_df = pd.read_sql(query, con=conn)

    pets_json = pets_df.to_json(orient='records')

    conn.close()

    return pets_json

if __name__ == "__main__":
    app.run(debug=True)