import flask
import sqlite3

######## HELPERS ############
def hash_id(id): # Creates 8 digit hashcode (int)
    return abs(hash(id)) % (10 ** 8)
#############################

app = flask.Flask(__name__)

@app.route("/register", methods=['GET','POST'])
def register():
    return flask.render_template("register.html")

@app.route("/createUser", methods=['POST'])
def submit_form():
    conn = sqlite3.connect('data/reddit.db')
    c = conn.cursor()
    first_name = flask.request.form['fname']
    last_name = flask.request.form['lname']
    userID = flask.request.form['userID']
    hashcode = hash_id(userID)
    print('Hashcode: ' + str(hashcode))
    user = (first_name, last_name, userID, hashcode)
    c.execute('INSERT INTO users VALUES(?, ?, ?, ?)', user)
    conn.commit()
    return "User has been created." # TODO: this should link to Feed page


if __name__ == '__main__':
    # Start the server
    app.run(port=8001, host='127.0.0.1', debug=True, use_evalex=False)
