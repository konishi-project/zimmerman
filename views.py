import flask
import time
from app import app,session,request,conn,db
from konishi_utils import *


@app.route('/')
def home():
    return 'Hello Konishi and >P!'

@app.route('/register',methods=['POST'])
def register():
    #Checks if user is already logged in
    if  'konishi_session' in session:
        return flask.make_response('<h1>Error 403</h1><br>You are already logged in',403)
    #Checks if username is already taken
    username = request.form['username']
    db.execute("SELECT id FROM users WHERE username=?",(username,))
    if db.fetchone():
        return flask.make_response('That username is already taken',403)
    fullname = request.form['fullname'][:20] #Typically a fullname won't be longer than 20 characters
    #Check db_utils for more info on email checking
    email = request.form['email']
    db.execute("SELECT id FROM users WHERE email=?",(email,))
    if not valid_email(email) or db.fetchone():
        return flask.make_response('That email is invalid or taken',403)
    ip_addr = request.remote_addr #Gets the IP Address of the user
    user_id = make_hash(ip_addr,get_time(),username) #Makes the user ID by hashing the username, IP Address and timestamp
    password = request.form['password']
    if len(password)<8: #Password should be longer than 8 characters
        return flask.make_response('Password needs to be at least 8 characters long',403)
    else:
        password = make_hash(password) #Hashes the password
    if db.execute("INSERT INTO users(username,fullname,email,password,id,ip_addr,reg_date,admin,zucc) values(?,?,?,?,?,?,?,0,1)",(username,fullname,email,password,user_id,ip_addr,get_time())):
        #Sets the zucc parameter to 1 aka banned on new members until they answer the admin questions. Typically this should be a trivial task handled by the frontend so i don't include any references to that here
        conn.commit()
        resp = flask.make_response(flask.jsonify({'status':'success','konishi_id':user_id,'ip_addr':ip_addr,'username':username,'fullname':fullname,'registration_date':time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))}),201)
    else:
        #Returns a server error code if submiting to the database fails for some reason
        resp = flask.make_response('<h1>Error 500</h1><br>An error occured. Please try again later',500)
    return resp


@app.route('/login',methods=['POST'])
def login():
    #Checks if user is already logged in
    if  'konishi_session' in session:
        return flask.make_response('<h1>Error 403</h1><br>You are already logged in',403)
    login = request.form['login']
    passwrd = request.form['password']
    db.execute("SELECT password,zucc,id FROM users WHERE username=? OR email=?",(login,login,))
    res = db.fetchone()
    if res:
        password = res[0]
        if password == make_hash(passwrd):
            if int(res[1]) == 0:
                session_id = make_hash(get_time(),res[2])
                db.execute("INSERT INTO sessions(sid,uid,time,invalid) values(?,?,?,?)",(session_id,res[2],get_time(),0,))
                session['konishi_session'] = session_id
                resp = flask.make_response(flask.jsonify({'status':'success','session_id':session_id}),200)
            else:
                resp = flask.make_response('<h1>Error 403</h1><br>Your account is suspended',403)
        else:
            resp = flask.make_response('<h1>Error 403</h1><br>Wrong password',403)
    else:
        resp = flask.make_response('<h1>Error 404</h1><br>Could not find user',404)
    return resp
