import os
from flask import Flask,session,request
import sqlite3
import json
from pyhunter import PyHunter
app = Flask(__name__)
from views import *

with open('server_cfg.json',"r+") as conf_file:
    config = json.loads(conf_file.read())
    database = config['database']
    if os.path.isfile(database):
        conn = sqlite3.connect(database, check_same_thread=False)
        db = conn.cursor()
    else:
        conn = sqlite3.connect(database,check_same_thread=False)
        db = conn.cursor()
        db.execute("CREATE TABLE posts (thread,author_id,id,timestamp,text,image,locked)")
        db.execute("CREATE TABLE users (username,fullname,password,email,id,ip_addr,reg_date,admin,zucc)")
        db.execute("CREATE TABLE sessions (uid,sid,time,invalid)")
    user_id = config['user_id']
    exts = set(config['file_exts'])
    hash_length = int(config['hash_length'])
    session_expire = int(config['max_session_time'])
    hunter = PyHunter(config['hunter_key'])
    app.config['MAX_CONTENT_LENGTH'] = int(config['max_size'])*1024^2
    app.config['JSONIFY_MIMETYPE'] = config['json_mimetype']
    app.config['SECRET_KEY'] = config['secret_key']
    app.config['SESSION_COOKIE_NAME'] = config['session_name']


if __name__=='__main__':
    app.run(port=5000,debug=True)
