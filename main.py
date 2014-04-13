from flask import Flask, request, render_template, Markup, json
import requests
from sets import Set

app = Flask(__name__)

def match_users(user, target, user_set, repo_set, level, degree_list):
    payload = {'type': 'all', 'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    payload2 = {'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    
    r = requests.get('https://api.github.com/users/' + user + '/repos', params=payload)
    if not r.status_code == requests.codes.ok:
        print r.status_code
        return False

    user_repos_raw = r.json()

    user_repos = {}

    for repos in user_repos_raw:
        if repos['full_name'] not in repo_set:
            user_repos[repos['full_name']] = repos['contributors_url']
            repo_set.add(repos['full_name'])


    users = Set([])

    for repos in user_repos.values(): 
        try:
            print repos
            q = requests.get(repos, params=payload2)
            users_raw = q.json()
            if not r.status_code == requests.codes.ok:
                print r.status_code
                continue
        except Exception as inst:
            continue;
        for person in users_raw:
            if person['login'] not in user_set:
                users.add(person['login']) 
                user_set.add(person['login'])
    if target in users:
        degree_list.append(target)
        return True
    for person in users:
       if  level < 3 and match_users(person, target, user_set, repo_set, level + 1, degree_list):
           degree_list.append(person)
           return True

    return False


@app.route('/')
def hello_world():
    end_set = []
    names = match_users('jromer94', 'sagnew', Set([]), Set([]), 1, end_set)
    print end_set
    return 'names'

@app.route('/user/<username>')
def show_user(username):
	return 'User %s' % username

if __name__ == '__main__':
    app.run(debug="true") 
