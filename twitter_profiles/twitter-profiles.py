from flask import Flask, render_template, request, jsonify
from user import User
from twitter import TwitterError
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile/<username>")
def profile(username):
    user = User(screen_name=username)
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

@app.route("/profile/<username>/frequencies", methods=['GET'])
def frequencies(username):
    return jsonify([["interest1",50],["interest2",50]])

def entry(title, content):
    return {"left" : title, "right": content}