from flask import Flask, render_template, request
from user import User
import twitter
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile")
def profile():
    screen_name = request.args.get('UserName', '')
    user = User(screen_name=screen_name)
    try:
        profession = user.profession()
        interests = user.interests()
        location = user.location()

        if len(location) > 0:
            entries.append(entry("Location", location))
        if len(interests) > 0:
            entries.append(entry("Interests", interests))

        return render_template('profile.html', user=screen_name, entries=entries)
    except twitter.TwitterError:
        return render_template('profile.html', notfound=True)

    

def entry(title, content):
    return {"left" : title, "right": content}