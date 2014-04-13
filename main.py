from flask import Flask, request, render_template, Markup, json
from sets import Set
import requests
import sqlite3
from sets import Set


app = Flask(__name__)

def match_users(user, user_dict, repo_set, level):
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
            if not user_dict.has_key(person['login']):
                users.add(person['login']) 
                user_dict[person['login']] = level
    for person in users:
       if level < 2:
           match_users(person, user_dict, repo_set, level + 1)
    return

access_token = '7b5e948bbb33a71fa7842b970b835a6717b28050'
_global = {}
_global["access_token"] = '7b5e948bbb33a71fa7842b970b835a6717b28050'

def get_related_users(user):
    payload = {'type': 'all', 'access_token': _global["access_token"]}
    payload2 = {'access_token': _global["access_token"]}
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
        new_access_token = raw_input("*** Please enter new access_token ***");
        _global["access_token"] = new_access_token
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
        # print related_user_set
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
from_user_index = 0
to_user_index = 1
repo_url_index = 2
conn_distance_index = 3

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
    print '%s -> %s (%d) [%s]' %(from_user, to_user, conn_distance, repo_url)
    db_conn.commit()
    db_conn.close()
    return 

def is_user_in_db(search_user):
    db_conn = sqlite3.connect('example.db')
    db_cursor = db_conn.cursor()
    
    db_cursor.execute('''
        SELECT * FROM github_connections WHERE to_user = '%s';
    ''' %(search_user))
    row = db_cursor.fetchone()
    result = False
    if (row):
        result = True
    
    db_conn.commit()
    db_conn.close()
    return result

def get_user_chain(search_user):
    db_conn = sqlite3.connect('example.db')
    db_cursor = db_conn.cursor()
    
    user_chain = []

    curr_user = search_user
    while (curr_user != 'theycallmeswift'):
        db_cursor.execute('''
            SELECT * FROM github_connections WHERE to_user = '%s';
        ''' %(curr_user))
        row = db_cursor.fetchone()
        next_user = row[from_user_index]
        connecting_repo = row[repo_url_index]

        data = {}
        data["user"] = next_user
        data["repo"] = connecting_repo
        user_chain.append(data)

        print next_user, connecting_repo
        curr_user = next_user


    db_conn.commit()
    db_conn.close()
    return user_chain




#############
#  Routing  #
#############
@app.route('/')
def hello_world():
    end_set = {}
    names = match_users('jromer94', end_set, Set([]), 1)
    print end_set
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
    # if (is_user_in_db("samuelreh")):
    #     print get_user_chain("samuelreh");
    # else:
    #     print "not found"
    app.run(debug="true") 
