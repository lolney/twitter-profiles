from flask import Flask, render_template
import user
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/profile")
def profile():
    return render_template('profile.html', profession=user.profession(), user="test_user")