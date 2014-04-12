from flask import Flask, request, render_template, Markup, json
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Great Big World!'

@app.route('/user/<username>')
def show_user(username):
	return 'User %s' % username

if __name__ == '__main__':
    app.run(debug="true") 