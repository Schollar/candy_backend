from flask import Flask, request, Response
import json
import dbhandler as dbh

import sys
app = Flask(__name__)


@app.get('/candy')
def get_posts():
    post_list = []
    posts_json = None
    try:
        post_list = dbh.get_posts()
        posts_json = json.dumps(post_list, default=str)
    except:
        return Response("Something went wrong getting the list of candy from the DB!", mimetype="application/json", status=400)
    if(post_list):
        return Response(posts_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting the list of candy from the DB!", mimetype="application/json", status=400)


@app.post('/candy')
def add_post():
    post_title = None
    post_content = None
    try:
        post_title = request.json['title']
        post_content = request.json['content']
        if(dbh.add_post(post_title, post_content)):
            return Response("You've successfully added a candy post!", mimetype="plain/text", status=200)
        else:
            return Response("Something went wrong adding a candy", mimetype="plain/text", status=400)
    except:
        return Response("Something went wrong adding a candy!", mimetype="application/json", status=400)


@app.patch('/candy')
def change_post():
    post_title = None
    post_new_title = None
    post_new_content = None
    try:
        post_title = request.json['title']
        post_new_title = request.json['new_title']
        post_new_content = request.json['content']
        if(dbh.change_post(post_title, post_new_title, post_new_content)):
            return Response("You've successfully changed a candy post!", mimetype="plain/text", status=200)
        else:
            return Response("Something went wrong editing a candy", mimetype="plain/text", status=400)
    except:
        return Response("Something went wrong editing a candy!", mimetype="application/json", status=400)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print('You must pass a mode to run this script. Either testing or production')
    exit()

if(mode == "testing"):
    print('Running in testing mode!')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode == "production"):
    print('Running in production mode')
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5005)
else:
    print('Please Run in either testing or production')
