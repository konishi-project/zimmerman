import json
import konishi_utils
from app import conn,db

class Post():
    id = ""
    author_id = ""
    timestamp = ""
    text = ""
    image = ""
    thread = ""
    locked = 0

    def update(self):
	    db.execute("UPDATE posts SET author_id=?,text=?,image=?,locked=? WHERE id=?",(self.author_id,self.text,self.image,self.locked,self.id,))
	    conn.commit()
	    return 1


    def save_post(self):
	    id = self.id
	    author_id = self.author_id
	    text = self.text
	    image = self.image
	    timestamp = self.timestamp
	    thread = self.thread
	    if db.execute("INSERT INTO posts (thread,id,author_id,timestamp,text,image) VALUES(?,?,?,?,?,?)",(thread,id,author_id,timestamp,text,image)):
	        conn.commit()
	        return 1
	    else:
	        return 0

    def add_comment(self,comm):
	    author_id = comm.author_id
	    timestamp = comm.timestamp
	    subject = comm.subject
	    image = comm.image
	    comment = comm.comment
	    post_id = self.id
	    id = make_hash(timestamp,post_id)
	    if db.execute("INSERT INTO posts(thread,author_id,id,timestamp,text,image) values(?,?,?,?,?,?)",(post_id,author_id,id,timestamp,text,image)):
	        conn.commit()
	        return 1
	    else:
	        return 0

    def get_comment_count(self):
	    db.execute("SELECT count(*) FROM posts WHERE thread=?",(self.id,))
	    return db.fetchone()[0]

    def get_comments(self):
	    post = {
	    'post_id':self.id,
	    'comments':[]
	    }
	    db.execute("SELECT id FROM posts WHERE thread=?",(self.id,))
	    for res in db.fetchall():
	        comment = {
	        'id':res,
	        'replies':[]
	        }
	        db.execute("SELECT id FROM posts WHERE thread=?",(res,))
	        for res2 in db.fetchall():
		        res['replies'].append(res2)
		        post['comments'].append(res)
	    return comments

    def delete(self):
	    db.execute("DELETE FROM posts WHERE id=?",(self.id,))
	    conn.commit()

    def pack_dict(self):
	    post = {
	    "author_id": self.author_id,
	    "post_id" : self.id,
	    "timestamp" : self.timestamp,
	    "text" : self.comment,
	    "image" : self.image,
	    "thread": self.thread
	    }
	    return post


class User():
    id = ""
    username = ""
    fullname = ""
    profile_pic = ""
    password = ""
    reg_datetime = ""
    admin = 0
    zucc = 0

    def update(self):
	    if db.execute("UPDATE users SET username=?,fullname=?,password=?,admin=?,zucc=?,profile_pic=? WHERE id=?",(self.username,self.fullname,self.password,self.admin,self.zucc,self.profile_pic,self.id,)):
                conn.commit()
                return 1

    def make_post(text,image=0,post_id=0,thread=0):
	    timestamp = get_time()
	    author_id = user_id
	    if post_id == 0:
	        post_id = make_hash(timestamp,author_id)
	    post = Post()
	    post.id = post_id
	    post.author_id = self.id
	    post.timestamp = timestamp
	    post.text = text
	    post.image = image
	    post.thread = thread
	    return post

    def pack_dict(self):
        user = {
            'id':self.id,
            'username':self.username,
            'fullname':self.fullname,
            'profile_pic':self.profile_pic,
            'password':self.password,
            'reg_time':self.reg_datetime,
            'admin':self.admin,
            'zucc':self.zucc
        }
        return user

    def ban(self,user):
	    if self.admin>=2:
	        user = get_user(user)
	        user.zucc = 1
	        user.update()

    def postblock(self,user,duration):
	    if self.admin>=1:
	        user = get_user(user)
	        user.zucc = duration
	        user.update()

    def lock_post(self,post):
	    if self.admin>=1:
		    get_post(post).locked = 1


class Picture():
    id = ""
    uid = ""
    path = ""
    og_name = ""
    nsfw = 0

    def pack_dict(self):
        pic = {
            'id':self.id,
            'uid':self.uid,
            'path':self.path,
            'og_name':self.og_name,
            'nsfw':self.nsfw
        }
        return pic
