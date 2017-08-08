from flask import Flask, render_template, request
from user import User
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile")
def profile():
    screen_name = request.args.get('UserName', '')
    user = User(screen_name)
    profession = user.profession()
    entries = [{"left" : "profession", "right" : profession}]
    return render_template('profile.html', profession=profession, user=screen_name, entries=entries)