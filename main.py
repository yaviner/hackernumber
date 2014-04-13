from flask import Flask, request, render_template, Markup, json
from sets import Set
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

def get_related_users(user):
    payload = {'type': 'all', 'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    payload2 = {'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    r = requests.get('https://api.github.com/users/' + user + '/repos', params=payload)
    user_repos_raw = r.json()
    user_repos = {}

    for repos in user_repos_raw:
        user_repos[repos['full_name']] = repos['contributors_url']

    users = Set([])

    for repos in user_repos.values(): 
        print repos
        q = requests.get(repos, params=payload2)
        try:
            users_raw = q.json()
            for person in users_raw:
                users.add(person['login'])
                # users[person['login']] = 'true' 
        except ValueError:
            print "shit.. didnt work"
            print q

    return users

# user is a string of username
# already_searched is a set containing users that have already been searched. 
# levels left is a number that starts at the max level reach
def user_bfs(user, already_searched, levels_left):
    if levels_left == 0:
        return
    elif not user in already_searched: 
        already_searched.add(user)
        related_user_set = get_related_users(user)
        print related_user_set
        for rel_user in related_user_set:
            rem_levels = levels_left - 1
            print '%s -> %s (%d)' %(user, rel_user, levels_left)
            user_bfs(rel_user, already_searched, rem_levels)
    else:
        return




@app.route('/')
def hello_world():
    end_set = []
    names = match_users('jromer94', 'sagnew', Set([]), Set([]), 1, end_set)
    print end_set
    return 'names'

@app.route('/user/<username>')
def show_user(username):
	return 'User %s' % username

@app.route('/search/<username>')
def search_user(username):
    searched_users = Set([])
    max_levels = 2
    user_bfs(username, searched_users, max_levels);
    return 'see console'

if __name__ == '__main__':
    app.run(debug="true") 
