from flask import Flask, render_template, request
import json
app = Flask(__name__)
# Invalid URL

@app.route('/index/<name>')
def index(name):
    with open('data/sample.json', 'r') as file:
        data = json.load(file)
    ls = [[users['ID'], users['username']] for users in data['users']]
    return render_template("dashboard.html", name = ls[0][1])

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html"), 404


#Internal server error

@app.errorhandler(500)
def serverError(e):
    return render_template("500.html"), 500