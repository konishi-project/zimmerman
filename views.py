import flask
import time
from app import app,session,request,conn,db
from konishi_utils import *

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/pictures/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/')
def home():
    return 'Hello Konishi and >P!'

@app.route('/register',methods=['POST'])
def register():
    #Checks if user is already logged in
    if  'konishi_session' in session:
        return flask.make_response('<h1>409 Conflict</h1><br>You are already logged in',409)
    #Checks if username is already taken
    username = request.form['username']
    db.execute("SELECT id FROM users WHERE username=?",(username,))
    if db.fetchone():
        return flask.make_response('That username is already taken',400)
    fullname = request.form['fullname'][:20] #Typically a fullname won't be longer than 20 characters
    #Check db_utils for more info on email checking
    email = request.form['email']
    db.execute("SELECT id FROM users WHERE email=?",(email,))
    if not valid_email(email) or db.fetchone():
        return flask.make_response('That email is invalid or taken',400)
    ip_addr = request.remote_addr #Gets the IP Address of the user
    user_id = make_hash(ip_addr,get_time(),username) #Makes the user ID by hashing the username, IP Address and timestamp
    password = request.form['password']
    if len(password)<8: #Password should be longer than 8 characters
        return flask.make_response('Password needs to be at least 8 characters long',400)
    else:
        password = make_hash(password) #Hashes the password
    if db.execute("INSERT INTO users(username,fullname,email,password,id,ip_addr,reg_date,admin,zucc) values(?,?,?,?,?,?,?,0,1)",(username,fullname,email,password,user_id,ip_addr,get_time())):
        #Sets the zucc parameter to 1 aka banned on new members until they answer the admin questions. Typically this should be a trivial task handled by the frontend so i don't include any references to that here
        conn.commit()
        resp = flask.make_response(flask.jsonify({'status':'success','konishi_id':user_id,'ip_addr':ip_addr,'username':username,'fullname':fullname,'registration_date':time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))}),201)
    else:
        #Returns a server error code if submiting to the database fails for some reason
        resp = flask.make_response('<h1>500 Internal Server Error</h1><br>An error occured. Please try again later',500)
    return resp


@app.route('/login',methods=['GET','POST'])
def login():
    #Checks if user is already logged in
    if  'konishi_session' in session:
        print('logged in')
        return flask.make_response('<h1>409 Conflict</h1><br>You are already logged in',409)
    #POST Request parameters
    if 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        passwrd = request.form['password']
    else:
        return flask.make_response('<h1>400 Bad Request</h1><br>No parameters provided',400)
    #Selects the hashed password,ban status and user ID from the database where either the username or email is the given login parameter
    db.execute("SELECT password,zucc,id FROM users WHERE username=? OR email=?",(login,login,))
    res = db.fetchone()
    if res: #Checks if the database fetch was successfull
        password = res[0]
        if password == make_hash(passwrd): #Checks the fetched password against a hashed version of the user provided password
            if int(res[1]) == 0: #Checks if the user is banned or not
                session_id = make_hash(get_time(),res[2]) #Makes a session id by hashing the timestamp and the user ID
                if db.execute("INSERT INTO sessions(sid,uid,time,invalid) values(?,?,?,0)",(session_id,res[2],get_time(),)):
                    conn.commit()
                    session['konishi_session'] = session_id #Makes a flask session
                    return flask.make_response(flask.jsonify({'status':'success','session_id':session_id}),200)
                else:
                    resp = flask.make_response('<h1>500 Internal Server Error</h1><br>An error occured. Please try again later',500)
            else:
                resp = flask.make_response('<h1>403 Forbidden</h1><br>Your account is suspended',403)
        else:
            resp = flask.make_response('<h1>403 Forbidden</h1><br>Wrong password',403)
    else:
        resp = flask.make_response('<h1>404 Not Found</h1><br>Could not find user',404)
    return resp


@app.route('/upload_image',methods=['GET','POST'])
def upload_image():
    if not valid_session(): #Checks if the session is valid
        return flask.make_response('<h1>401 Unauthorized</h1><br>You are not logged in',401)
    if request.method == 'POST' and 'image' not in request.files or request.files['image'].filename == '': #Checks if the image was submitted and does not have an empty name
        return flask.make_response('<h1>400 Bad Request</h1><br>No image uploaded',400)
    image = request.files['image']
    #Checks the nsfw status provided by the user. It can only be 0 or 1
    if request.form['nsfw']=='0':
        nsfw = 0
    elif request.form['nsfw']=='1':
        nsfw = 1
    else:
        return flask.make_response('<h1>400 Bad Request</h1><br>Invalid nsfw argument',400)
    #Last check if image was submitted and is allowed (aka is an image)
    if image and allowed_file(image.filename):
        #Gets the session ID and uses that to safely fetch the user_id
        uid = valid_session()['user'].id
        pic_id = make_hash(get_time(),uid,image.filename) #Makes the picture ID by hashing the timestamp, user ID and original filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], pic_id+'.'+allowed_file(image.filename))
        image.save(path)
        if db.execute("INSERT INTO pictures(id,path,uid,time,og_name,nsfw) values(?,?,?,?,?,?)",(pic_id,path,uid,get_time(),image.filename,nsfw,)):
            conn.commit()
            resp = flask.make_response(flask.jsonify({'status':'success','user_id':uid,'picture_id':pic_id}),201)
        else:
            resp = flask.make_response('<h1>500 Internal Server Error</h1><br>An error occured. Please try again later',500)
    else:
        resp = flask.make_response('<h1>400 Bad Request</h1><br>The file provided is not a valid image',400)
    return resp


@app.route('/getmypics',methods=['GET'])
def getmypics():
    if not valid_session(): #Checks if the session is valid
        return flask.make_response('<h1>401 Unauthorized</h1><br>You are not logged in',401)
    pics = get_all_pictures(valid_session()['user'])
    pic_list = {
        'status':'success',
        'uid':valid_session()['user'].id,
        'pictures':[]
    }
    for pic in pics:
        pic.path = flask.url_for('uploaded_file',filename=pic.id+pic.ext)
        pic = pic.pack_dict()
        pic.pop('uid',None)
        pic_list['pictures'].append(pic)
    return flask.make_response(flask.jsonify(pic_list),200)


@app.route('/change_pfp',methods=['GET','POST'])
def change_pfp():
    if not valid_session(): #Checks if the session is valid
        return flask.make_response('<h1>401 Unauthorized</h1><br>You are not logged in',401)
    img_id = request.args['img_id']
    user = valid_session()['user']
    img = get_picture(img_id)
    if img.uid == user.id:
        user.profile_pic = img.id
        if user.update():
            resp = flask.make_response(flask.jsonify({'status':'success','user_id':user.id,'picture_id':img.id}),200)
        else:
            resp = flask.make_response('<h1>500 Internal Server Error</h1><br>An error occured. Please try again later',500)
    else:
        resp = flask.make_response('<h1>403 Forbidden</h1><br>This picture does not belong to you',403)
    return resp
