from flask import Flask, render_template
from user import User
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile/<screen_name>")
def profile(screen_name):
    user = User(screen_name)
    profession = user.profession()
    entries = [{"left" : "profession", "right" : profession}]
    return render_template('profile.html', profession=profession, user=screen_name, entries=entries)