from flask import Flask, render_template, request
from user import User
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile")
def profile():
    screen_name = request.args.get('UserName', '')
    user = User(screen_name=screen_name)
    profession = user.profession()
    interests = user.interests()
    location = user.location()

    entries = [entry("Profession", profession)]

    if len(location) > 0:
        entries.append(entry("Location", location))
    if len(interests) > 0:
        entries.append(entry("Interests", interests))

    return render_template('profile.html', profession=profession, user=screen_name, entries=entries)

def entry(title, content):
    return {"left" : title, "right": content}