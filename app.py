from flask import Flask, request, Response
import json
import dbhandler as dbh

import sys
app = Flask(__name__)

# Function that takes in no user input, runs the dbhandler get posts which gets all the posts from the db and returns them in the response


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

# Function that gets title and content as user input and sends it off to dbhandler add post function to add a post to the db.


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

# Function that takes in user input and sends it off to dbhandler change post to change the title and content of a post.


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

# Function that takes in a post title and sends it off to dbhandler to be deleted from the DB


@app.delete('/candy')
def delete_post():
    post_title = None
    try:
        post_title = request.json['title']
        if(dbh.delete_post(post_title)):
            return Response("You've successfully deleted a candy post!", mimetype="plain/text", status=200)
        else:
            return Response("Something went wrong deleting a candy", mimetype="plain/text", status=400)
    except:
        return Response("Something went wrong deleting a candy!", mimetype="application/json", status=400)


# Checking to see if a mode was passed to the script
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print('You must pass a mode to run this script. Either testing or production')
    exit()
# Depending on what mode is passed, we check and run the appropriate code.
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
