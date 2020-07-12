from flask import render_template
from app import app
@app.route('/')
def base():
    return render_template("base.html")

@app.route('/index')
def index():
    return render_template("index.html") 

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    error = None 
    return render_template('login.html', error=error) 