from flask import Flask, render_template
import user
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile")
def profile():
    profession = user.profession()
    entries = [{"left" : "profession", "right" : profession}]
    return render_template('profile.html', profession=profession, user="test_user", entries=entries)