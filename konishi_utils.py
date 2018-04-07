import time
import hashlib
import base64
import models
import json
from app import db,conn,hunter,session_expire
hash_length = 32

#Self explanatory
def get_time():
    return int(time.time())

#Concatenates all the parameters except length into a string and hashes it with sha256
def make_hash(*args,length=hash_length):
    tobehashed = ''
    for arg in args:
        tobehashed = tobehashed+str(arg)
    tobehashed = tobehashed.encode("utf-8")
    hash_object = hashlib.sha256(tobehashed)
    return hash_object.hexdigest()[:length]

#Checks if email address is valid. Checking is provided by hunter.io. Needs an API key to work.
def valid_email(email):
    res = hunter.email_verifier(email)
    if res['gibberish']==False and res['disposable']==False and res['regexp']==True and res['score']>=50:
        return 1
    else:
        return 0

#Valid session check. Typically included at the top of every view with a direct return to an error if 0
def valid_session():
    if 'konishi_session' in session:
        id = session['konishi_session']
    else:
        return 0
    db.execute("SELECT time,invalid FROM sessions WHERE sid=?",(id,))
    result = db.fetchone()
    if result and get_time() - int(result[0]) < session_expire and not result[1]:
        return 1
    else:
        return 0

#Gets a user object by ID from the database
def get_user(id):
    db.execute("SELECT id,username,fullname,password,reg_datetime,zucc,admin FROM users WHERE id=?",(id,))
    res = db.fetchone()
    user = models.User()
    user.id = res[0]
    user.username = res[1]
    user.fullname = res[2]
    user.password = res[3]
    user.reg_datetime = res[4]
    user.zucc = res[5]
    user.admin = res[6]
    return user

#Gets a post object by ID from the database
def get_post(id):
    db.execute("SELECT id,thread,author_id,timestamp,text,image FROM posts WHERE id=?",(id,))
    res = db.fetchone()
    post = models.Post()
    post.id = res[0]
    post.thread = res[1]
    post.author_id = res[2]
    post.timestamp = res[3]
    post.text = res[4]
    post.image = res[5]
    return post

#Checks if a post exists
def post_exists(id):
    db.execute("SELECT id FROM posts WHERE id=?",(id,))
    if db.fetchone():
        return 1
    else:
         return 0
