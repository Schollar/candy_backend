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
        post_json = json.dumps(post_list, default=str)
    except:
        return Response("Something went wrong getting employee from the DB!", mimetype="application/json", status=400)
    if(post_list):
        return Response(post_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting employee from the DB!", mimetype="application/json", status=400)


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
