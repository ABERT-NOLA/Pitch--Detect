from flask import Flask
from flask import render_template
from app import app
@app.route('/')
def base():
    return render_template("base.html")

@app.route('/index')
def index():
    return render_template("index.html")    
if __name__ == '__main__':
    app.run(debug = True)