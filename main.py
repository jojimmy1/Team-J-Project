import flask
import sqlite3
import datetime
from flask import abort, redirect, url_for

######## HELPERS ############
def hash_id(id): # Creates 8 digit hashcode (int)
    return abs(hash(id)) % (10 ** 8)
#############################

# app = flask.Flask(__name__)
app = flask.Flask(__name__, static_folder='styles/')

@app.route("/register", methods=['GET','POST'])
def register():
    return flask.render_template("register.html")

@app.route("/createUser", methods=['POST'])
def submit_form():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    first_name = flask.request.form['fname']
    last_name = flask.request.form['lname']
    userID = flask.request.form['userID']
    hashcode = hash_id(userID)
    
    #if same id, link to already exist
    check1 = (c.execute("SELECT hashcode from users where userID = ?", (userID,)).fetchall())
    if (check1 != []):
        hashcode = check1[0][0]
        url1 = f"/{hashcode}/profile"
        return redirect(url1)
    
    print('Hashcode: ' + str(hashcode))
    user = (first_name, last_name, userID, hashcode)
    c.execute('INSERT INTO users VALUES(?, ?, ?, ?)', user)
    conn.commit()
    # return "User has been created." # TODO: this should link to Feed page
    url1 = f"/{hashcode}/profile"
    return redirect(url1)

@app.route("/<hashedcode>/create", methods=['GET', 'POST'])
def create_post(hashedcode):
    return flask.render_template("create_post.html",hashedcode = hashedcode)

@app.route("/create_done", methods=['POST'])
def create_post_done():
    conn = sqlite3.connect('./data/database.db')
    c = conn.cursor()
    
    #get user id
    hashedcode = flask.request.form['id2']
    id = (c.execute("SELECT * from users where hashcode = ?", (hashedcode,)).fetchall())
    id = id[0][2]
    print(id)
    
    #capture info
    title1 = flask.request.form['title1']
    content1 = flask.request.form['content1']
    time1 = datetime.datetime.now()
    time1 = str(time1)
    vote_count = 0
    
    # generate id, make sure unique
    post_id = hash_id(time1)
    post_str = str(post_id)
    check1 = (c.execute("SELECT * from posts where post_id = ?", (post_str,)).fetchall())
    while (check1 != []):
        post_id = post_id + 1
        post_str = str(post_id)
        check1 = (c.execute("SELECT * from posts where post_id = ?", (post_str,)).fetchall())
    
    #insert
    tobeInserted = (post_str,title1,content1,time1,vote_count,"",id)
    c.execute('INSERT INTO posts VALUES(?, ?, ?, ?, ?, ?, ?)', tobeInserted)
    
    conn.commit()
    conn.close()
    # return "Post created" # TODO: Should redirect to profile
    url1 = f"/{hashedcode}/profile"
    return redirect(url1)

# read post
@app.route("/posts/<postid>", methods=['GET', 'POST'])
def display2(postid):
    postid = str(postid)
    conn = sqlite3.connect('./data/database.db')
    c = conn.cursor()
    post9 = (c.execute("SELECT userID,title,content from posts where post_id = ?", (postid,)).fetchall())
    message = f"The user is {post9[0][0]}. Title is {post9[0][1]}. Content is {post9[0][2]}. "
    return message # TODO: Read Post frontend
    # conn.commit()
    # conn.close()
    # return flask.render_template('view1.html', message = message, id1 = id)

# profile page
@app.route("/<hashedcode>/profile", methods=['GET', 'POST'])
def seeall(hashedcode): 
    db_dict = {}
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    
    #get id
    id = (c.execute("SELECT * from users where hashcode = ?", (hashedcode,)).fetchall())
    id = id[0][2]
    
    fetchall = (c.execute("SELECT title,content,post_id from posts WHERE userID = ? ORDER BY create_time DESC", (id,)).fetchall())
    for element in (fetchall):
        db_dict.update({(element[0],element[2]): element[1]})
    print(db_dict)
    return flask.render_template('view2.html', data = db_dict, hashedcode = hashedcode)

if __name__ == '__main__':
    # Start the server
    app.run(port=8002, host='127.0.0.1', debug=True, use_evalex=False)
