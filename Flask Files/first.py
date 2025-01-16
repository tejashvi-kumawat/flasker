from flask import Flask, render_template, request
import json

#Flask Instance
app = Flask(__name__)

#Create a route decorator
#safe: If HTML tags paresd than it will run those HTML Tags
#capitalize
#lower
#upper
#title
#trim
#striptags : it can strip tags so that when we create commenting at that time hackers can't make changes in the website, it will strip all html tags from that

@app.route('/index/<name>')
def index(name):
    with open('data/sample.json', 'r') as file:
        data = json.load(file)
    ls = [[users['ID'], users['username']] for users in data['users']]
    return render_template("dashboard.html", name = ls[0][1])

@app.route('/submit', methods=['POST'])
def submit():
    # Get the text entered by the user in the input field
    user_input = request.form.get('user_input')
    
    # Return the input text to be displayed on the same page
    return user_input

@app.route('/user/<name>')

def about(name):
    return "<h1>Hello {}</h1>".format(name)



if __name__ == "__main__":
    app.run(debug=True)