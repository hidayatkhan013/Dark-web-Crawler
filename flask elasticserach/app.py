from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from elasticsearch import Elasticsearch,helpers
import bcrypt
import datetime
import requests
import json
import time

def connect():
    connection = MongoClient('localhost', 27017)
    handle = connection["darkweb"]
    return handle

app = Flask(__name__)
app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200/'
es =  Elasticsearch([app.config['ELASTICSEARCH_URL']])
handle = connect()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = handle.usersessions
    login_user = "users.find_one({'name': request.form['username']})"

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return render_template('redirect.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = handle.usersessions
        existing_user = users.find_one({'name': request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'Username Already Exists'

    return render_template('register.html')

@app.route('/list')
def get():
    # if 'username' in session:
    cdata = handle.DW_data_onion_only.find()
    count = handle.DW_data_onion_only.find().count()
    return render_template('home.html', mydata=cdata,number=count)
    # return render_template('login.html')

@app.route('/search')
def lookup():
    # if 'username' in session:
    return render_template('search.html')
    # return render_template('login.html')

@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    # if 'username' in session:
    search_term = request.form["input"]
    
    res = es.search(index="darkwebdata", size=10000, body={"query": {"multi_match" : { "query": search_term, "fields": ["Name","PageText"] }}})
    print("-------------------------------" ,len(res['hits']['hits']))
    return render_template('results.html', res=res ,query=search_term )
    # return render_template('login.html')

@app.route('/add')
def registration():
    # if 'username' in session:
    return render_template('add.html', pagetitle='Add Item')
    # return render_template('login.html')

@app.route("/post", methods=['GET', 'POST'])
def write():
    cdata = connect().DW_data_onion_only.find()
    k=0
    for i in cdata:
        
        print(f"[+] {k}  pushing ---",i["Name"])
        k+=1
        esdata = json.dumps({
            "Name": i['Name'],
            "PageText": i['Page Text']
            })
        es.index(index="darkwebdata", doc_type="Data", body=esdata)
    # # docs={}
    
    #     docs[u["Name"]]=u["Page Text"]
    # # print(docs.keys())
    # # print(docs.values())
    # es.index(index="darkweb", doc_type="ESDW", body=docs)
    # helpers.bulk(es, docs, index='darkweb', doc_type='ESDW')
    return redirect ("/list")

    # return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
