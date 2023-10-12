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
    if request.method == "POST":
        operation = str(request.json["Operation"])
        if operation == "Create Database":
            dbname = str(request.json["dbname"])
            try:
                db = dbconn[dbname]
                db.create_collection(dbname + "_Collection")
                return jsonify(dbname + "Database &" + dbname + " Collection Created")
            except Exception as e:
                return jsonify(e)

            if operation == 'Create Collection':
                collection_name = str(request.json['Collection'])
                db.create_collection(collection_name)
                return jsonify(collection_name+' Collection Created Successfully')

        if operation == 'Show Available Databases':
            dir = dbconn.list_database_names()
            return jsonify(dir)

        if operation == 'Add Data':
            return



if __name__ == "__main__":
    app.run()
