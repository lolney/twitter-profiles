import StringIO
import csv
from twitter import TwitterError
from flask import Flask, render_template, request, jsonify, make_response
from user import User

class Users:

    def __init__(self):
        self.users = {}

    def get_user(self, screen_name):
        key = screen_name.lower()
        try:
            res = self.users[key]
            return res
        except:
            user = User(screen_name=screen_name)
            self.users[key] = user
            return user

app = Flask(__name__)
users = Users()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile/<username>")
def profile(username):
    try:
        user = users.get_user(username)
    except TwitterError as e:
        return e[0][0]['message'], 400

    try:
        profession = user.profession()
        interests = user.interests()
        location = user.location()

        entries = [entry("Profession", profession)]

        if len(location) > 0:
            entries.append(entry("Location", location))
        if len(interests) > 0:
            entries.append(entry("Interests", interests))

        return render_template('profile.html', user=username, entries=entries)
    except TwitterError:
        return render_template('profile.html', notfound=True)

@app.route('/username/<username>', methods=['PUT'])
def username(username):
    try:
        user = users.get_user(username)
        return "", 200
    except TwitterError as e:
        return str(e), 400

@app.route("/profile/<username>/frequencies", methods=['GET'])
def frequencies(username):
    return jsonify([["interest1",50],["interest2",50]])

@app.route("/profile/<username>/categories", methods=['GET'])
def categories(username):
    return jsonify(get_categories(username))

@app.route("/profile/<username>/categories/csv", methods=['GET'])
def categories_csv(username):
    cats = get_categories(username)
    csvList = formatcats("", cats)

    si = StringIO.StringIO()
    cw = csv.DictWriter(si, fieldnames=['id','value'])
    cw.writeheader()
    cw.writerows(csvList)
    output = make_response(si.getvalue())
    output.headers["Content-type"] = "text/csv"
    return output

def get_categories(username):
    return users.get_user(username).categories()

def formatcats(super, cats):
    ret = []
    for cat, subcats in cats.iteritems():
        if type(subcats) is list:
            if len(subcats) == 0:
                ret = ret + [{'id':super + cat, 'value':0}]
            else:
                ret = ret + [{'id':super + cat, 'value':0}]+ [{'id':super + cat + "." + subcat, 'value':0} for subcat in subcats]
        else:
            ret = ret + [{'id':super + cat, 'value':None}]
            ret = ret + formatcats(super + cat + ".", subcats)
    return ret

def entry(title, content):
    return {"left" : title, "right": content}