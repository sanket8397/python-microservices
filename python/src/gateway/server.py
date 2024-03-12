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