from flask import Flask, request, render_template, Markup, json
from sets import Set
import requests
import sqlite3




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

def get_related_users(user):
    payload = {'type': 'all', 'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    payload2 = {'access_token': '7b5e948bbb33a71fa7842b970b835a6717b28050'}
    r = requests.get('https://api.github.com/users/' + user + '/repos', params=payload)
    user_repos_raw = r.json()
    user_repos = {}

    #users = Set([])
    
    users_with_repo = {}

    try:
        for repos in user_repos_raw:
            user_repos[repos['full_name']] = repos['contributors_url']
        for repos in user_repos.values(): 
            #print repos
            q = requests.get(repos, params=payload2)
            try:
                users_raw = q.json()
                for person in users_raw:
                    #users.add(person['login'])
                    users_with_repo[person['login']] = repos
                    # users[person['login']] = 'true' 
            except Exception:
                continue
    except Exception:
        return users_with_repo

    return users_with_repo

# user is a string of username
# already_searched is a set containing users that have already been searched. 
# levels left is a number that starts at the max level reach
def user_bfs(user, already_searched, current_level, max_level):
    if current_level >= max_level:
        return
    elif not user in already_searched: 
        already_searched.add(user)
        related_user_set = get_related_users(user)
        print related_user_set
        for rel_user in related_user_set:
            repo_url = related_user_set[rel_user]
            insert_conn_row(user, rel_user, repo_url, (current_level+1))
            new_level = current_level + 1
            user_bfs(rel_user, already_searched, new_level, max_level)
    else:
        return


def start_search(user, max_levels):
    searched_users = Set([])
    user_bfs(user, searched_users, 0, max_levels);

##############
#  DB stuff  #
##############
conn_table = 'github_connections'
def init_db():
    db_conn = sqlite3.connect('example.db')
    db_cursor = db_conn.cursor()
    res = db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS
            github_connections
        (
            from_user TEXT,
            to_user TEXT,
            repo_url TEXT,
            conn_distance INTEGER
        );
    ''')
    print res
    print "created db with table `github_connections`"
    db_conn.commit()
    db_conn.close()
    return

def insert_conn_row(from_user, to_user, repo_url, conn_distance):
    db_conn = sqlite3.connect('example.db')
    db_cursor = db_conn.cursor()
    db_cursor.execute('''
        INSERT INTO github_connections 
        (from_user, to_user, repo_url, conn_distance)
        VALUES ('%s', '%s', '%s', '%s');
    ''' %(from_user, to_user, repo_url, conn_distance))
    print '%s -> %s (%d) [%s]' %(from_user, to_user, (conn_distance+1), repo_url)
    db_conn.commit()
    db_conn.close()
    return 





#############
#  Routing  #
#############
@app.route('/')
def hello_world():
    names = match_users('jromer94', 'adispen')
    return 'names'

@app.route('/user/<username>')
def show_user(username):
	return 'User %s' % username

@app.route('/search/<username>')
def search_user(username):
    start_search(username, 3);
    return 'see console'

if __name__ == '__main__':
    init_db()
    app.run(debug="true") 
