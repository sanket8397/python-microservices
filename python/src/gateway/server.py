import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo

from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

# Manage mongo db connection for flask server
mongo = PyMongo(server)

# Mongo DB is used to store video files. BSON (binary JSON) max size is 16 MB. To handle big files use GridFS by sharding file
fs = gridfs.GridFS(mongo.db)

# connection with rabbitmq
# rabbitmq host is deployed in kubernetes to access use "rabbitmq"
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400

        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)

            if err:
                return err
        
        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)