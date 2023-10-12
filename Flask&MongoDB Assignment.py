# The Objective of this assignment is to make an url page which can
# 1. create a dataset inside mongodb
# 2. update into the dataset
# 3. insertion of data into the dataset
# 4. delete from table
# 5. download data from database

import random
import math
import string
from flask import Flask, request, jsonify, render_template
import pymongo

app = Flask("__name__")
dbconn = pymongo.MongoClient("mongodb://localhost:27017/")


@app.route("/db", methods=["POST"])
def dbdoing():
    if request.method != "POST":
        return
    operation = str(request.json["Operation"])
    if operation == 'Create Collection':
        collection_name = request.json['Collection']
        db1 = dbconn[request.json['Choose Database']]
        try:
            db1.create_collection(collection_name)
            return jsonify("collection created successfully")
        except Exception as f:
            return jsonify(f)

    elif operation == "Add Data":
        data = dict(request.json["dataset"])
        collection = str(request.json["choose_collection"])
        collection.insert_many(data)
        return jsonify(f"{data}Has Been Inserted")
    elif operation == "Create Database":
        dbname = str(request.json["dbname"])
        try:
            db = dbconn[dbname]
            db.create_collection(f"{dbname}_Collection")
            return jsonify(f"{dbname}Database & {dbname} Collection Created")
        except Exception as e:
            return jsonify(e)

    elif operation == "Show Available Databases":
        dbnames = dbconn.list_database_names()
        return jsonify(dbnames)


if __name__ == "__main__":
    app.run()
