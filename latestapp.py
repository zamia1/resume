

#import json
 
#import pprint
#from json2html import *
from pymongo import MongoClient

from flask import jsonify, render_template, request, url_for
#, send_file
from flask import Flask, flash, redirect
import pdb
#import ast
import os

import gridfs


app = Flask(__name__)

# Configure a secret key for Flask-Login
app.secret_key =os.urandom(50)
#url= "http://python-web-test-softpost-newh.azurewebsites.net/"
url="http://127.0.0.1:5000/"
FILE_SYSTEM_ROOT =os.getcwd()


client = MongoClient("mongodb+srv://mongodb:mongodb@cluster0.ps5mh8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Get and Post Route
bflag=True
db = client.dataghotkali
#allghotkali = db.dataghotkalicol
ghotkali_collection = db['ghotali']
users_collection = db['users']


def connectToDb(namesp):
    fs = gridfs.GridFS(db,namesp)
    return db, ghotkali_collection, fs

@app.route('/register', methods=['GET', 'POST'])
def register():
   # pdb.set_trace()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
           # return redirect(url+'/login')


    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
@app.route('/',methods=['GET', 'POST'])
def login():
    #pdb.set_trace()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            #flash('Login successful.', 'success')
            return render_template('home.html',url=url)
            # Add any additional logic, such as session management
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')
@app.route('/get_file/<name>/<gender>')
@app.route('/get_file', methods=['GET','POST'])
def get_file(name=None,gender=None):
    pdb.set_trace()
    
    if request.method=="POST":
        
    #fs = gridfs.GridFS(MongoClient().CINEfs_example)

        if name is not None:
            f = fs.get_last_version(name)
            r = app.response_class(f, direct_passthrough=True, mimetype='application/octet-stream')
            r.headers.set('Content-Disposition', 'attachment', filename=name)
            return r
        else:
            gender=request.form['gender']
            age=request.form['age']
            db, collectn, fs = connectToDb(gender+age)
            # db, collectn, fsimage = connectToDb(gender+age+"image")
            # if fsimage:
            #     return render_template('get_file.html', names=fs.list(), images=fsimage.list())
            # else:
            if fs:
                return render_template('get_file.html', names=fs.list())
    return render_template('filter.html')




@app.route('/upload', methods=['GET','POST'])
def upload():
    pdb.set_trace()
    if request.method == "POST":
        names=request.form['names']
        age=request.form['age']
        filenamea=""
        files = request.files.getlist("file[]")
        for file in files: 
            if file.filename.endswith('.pdf'):
                filenamea=file.filename.replace(".pdf","")
        for file in files:
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if file and file.filename.endswith('.pdf'):
                file_id = fs.put(file, filename=file.filename)
                db, collectn, fs = connectToDb(names+age)
                file_id = fs.put(file, filename=file.filename)
            #if image:
            elif file and file.filename.endswith('.jpeg'):
                db, collectn, fs = connectToDb(names+age)
                file_id = fs.put(file, filename=filenamea+"image")
           # return jsonify({'file_id': str(file_id)}), 201
            else:
                return jsonify({'error': 'Only PDF files are allowed'}), 400

        return jsonify({'output':'file is uploaded'}), 201
    else:
        return render_template('index.html')


