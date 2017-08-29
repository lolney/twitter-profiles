import StringIO
import csv
from flask import Flask, render_template, request, jsonify, make_response
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

@app.route('/username/<username>', methods=['PUT'])
def username(username):
    try:
        user = User(screen_name=username, create=True)
        return "", 200
    except TwitterError:
        return "Twitter username does not exist", 400

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
    return {"interests":
        {"Sports":
            {
                "Baseball" : [],
                "Track and Field" : ["800m"]
            },
        "Creative":
            {
                "Writing" : {"Fiction" : ["Poetry", "Short stories"]}
            },
        "Formal studies": ["Mathematics"]
        }
    }

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