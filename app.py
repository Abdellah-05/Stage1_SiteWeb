from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from validate_email import validate_email
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def hello_world():
    titre = "Acceil"
    return render_template('home.html', titre = titre)


@app.route('/about')
def aboutUs():
    id = "about-body"
    titre = "About Us"
    return render_template('about.html',  titre = titre, id = id)

if __name__ == "__main__" :
    app.run(debug=True)