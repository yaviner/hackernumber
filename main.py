from flask import Flask, request, render_template, Markup, json
import requests

app = Flask(__name__)

def match_users(user, target):
    payload = {'type': 'all', 'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    payload2 = {'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    r = requests.get('https://api.github.com/users/' + user + '/repos', params=payload)
    user_repos_raw = r.json()
    user_repos = {}

    for repos in user_repos_raw:
        user_repos[repos['full_name']] = repos['contributors_url']

    users = {}

    for repos in user_repos.values(): 
        print repos
        q = requests.get(repos, params=payload2)
        users_raw = q.json()
        for person in users_raw:
            users[person['login']] = 'true' 
    if users.has_key(target):
        return target 

    return 'null'


@app.route('/')
def hello_world():
    names = match_users('jromer94', 'adispen')
    return 'names'

@app.route('/user/<username>')
def show_user(username):
	return 'User %s' % username

if __name__ == '__main__':
    app.run(debug="true") 
