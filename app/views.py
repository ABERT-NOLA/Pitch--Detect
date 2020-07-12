@app.route('/')
def base():
    return render_template("base.html")

@app.route('/index')
def index():
    return render_template("index.html") 