import time
import hashlib
import base64
import models
import json
from inspect import isclass
from app import *
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
    db.execute("SELECT time,invalid,uid FROM sessions WHERE sid=?",(id,))
    result = db.fetchone()
    if result and get_time() - int(result[0]) < session_expire and not result[1]:
        return {'user':get_user(result[2]),'time_remaining':get_time()-int(result[0])}

#Checks if a file is allowed. I pulled this from the flask documentation
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in exts:
        return filename.rsplit('.', 1)[1].lower()

#Gets a user object by ID from the database
def get_user(id):
    db.execute("SELECT id,username,fullname,password,reg_date,zucc,admin,profile_pic FROM users WHERE id=?",(id,))
    res = db.fetchone()
    user = models.User()
    user.id = res[0]
    user.username = res[1]
    user.fullname = res[2]
    user.password = res[3]
    user.reg_time = res[4]
    user.zucc = res[5]
    user.admin = res[6]
    user.profile_pic = res[7]
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

#Gets a picture by ID from the database
def get_picture(id):
    db.execute("SELECT id,path,uid,time,og_name,nsfw FROM pictures WHERE id=?",(id,))
    res = db.fetchone()
    pic = models.Picture()
    pic.id = res[0]
    pic.path = res[1]
    pic.uid = res[2]
    pic.time = res[3]
    pic.og_name = res[4]
    pic.nsfw = int(res[5])
    pic.ext = os.path.splitext(res[4])[1]
    return pic

#Checks if a post exists
def post_exists(id):
    db.execute("SELECT id FROM posts WHERE id=?",(id,))
    if db.fetchone():
        return 1
    else:
         return 0

#Gets all pictures of the provided user
def get_all_pictures(user):
    if not isclass(user):
        uid = user.id
    else:
        uid = user
    db.execute("SELECT id,path,time,og_name,nsfw FROM pictures WHERE uid=?",(uid,))
    result = db.fetchall()
    pictures = []
    for res in result:
        pic = models.Picture()
        pic.id = res[0]
        pic.uid = uid
        pic.path = res[1]
        pic.time = res[2]
        pic.og_name = res[3]
        pic.nsfw = int(res[4])
        pic.ext = os.path.splitext(res[3])[1]
        pictures.append(pic)
    return pictures
