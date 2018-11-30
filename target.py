import logging
from flask import request, Blueprint, Response
import os, json
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()
from google.appengine.api import urlfetch
from pymongo import MongoClient
import base64

client = MongoClient("mongodb://127.0.0.1:27017")

db = client.app

targetdb = db.target

target = Blueprint('target', __name__)



@target.route('/authentication', methods=['POST'], strict_slashes=False)
def authentication(request=request):
    """
            Authentication System
            ---
            tags:
              - System - Authentication System
            parameters:
              - in: body
                name: data
                description: authentication
                default: '{"userName": "Pooja", "password": "xyz"}'


            responses:
              200:
                description: Hello

           """

    request = request.json
    userName = request.get("userName")
    password = request.get("password")

    print(password.encode('ascii', 'ignore'), "passworddddd")

    cursor = targetdb.userdb.find({'userName': userName})

    try:
        record = cursor.next()
        print(record, "recorddd")
        savedPassword = record.get("password")
        decodePassword = savedPassword.decode('base64')

        print(decodePassword, password, "decoodeeeeeeee")

        if password != decodePassword:
            return Response("incorrect password", mimetype='text/plain', status=401)

        else:
            return Response("Authentication Successfull", mimetype='text/plain', status=200)


    except StopIteration:

        return Response("not found", mimetype='text/plain', status=404)






@target.route('/register', methods=['POST'], strict_slashes=False)
def register(request=request):
    """
            register user
            ---
            tags:
              - System - register user
            parameters:
              - in: body
                name: data
                description: authentication
                default: '{"userName": "Pooja", "Password": "abcd"}'


            responses:
              200:
                description: Hello

           """

    request = request.json
    userName = request.get("userName")
    password = request.get("Password")

    encodedpassword= base64.b64encode(password)

    res = targetdb.userdb.insert({'userName': userName, 'password':encodedpassword})
    print res

    return Response("user name and password has been saved", mimetype='text/plain', status=200)



@target.route('/insert', methods=['POST'], strict_slashes=False)
def insert(request=request):
    """
            insert details
            ---
            tags:
              - System - insert the data
            parameters:
              - in: body
                name: data
                description: authentication
                default: '{"userName": "Pooja", "city": "Bangalore", "movie": "DDLG"}'


            responses:
              200:
                description: Hello

           """

    request = request.json
    userName = request.get("userName")
    city = request.get("city")
    movie = request.get("movie")

    details= base64.b64encode({'userName': userName, 'city':city, 'movie': movie})

    res = targetdb.userdb.insert(details)
    print res

    return Response("user name and password has been saved", mimetype='text/plain', status=200)