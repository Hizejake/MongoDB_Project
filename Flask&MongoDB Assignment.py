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
                return jsonify(dbname + "Database & " + dbname + " Collection Created")
            except Exception as e:
                return jsonify(e)

        if operation == "Show Available Databases":
            dbnames = dbconn.list_database_names()
            return jsonify(dbnames)

        if operation == 'Create Collection':
            collection_name = request.json['Collection']
            connected_db = request.json['Choose Database']
            db1 = dbconn[connected_db]
            try:
                db1.create_collection(collection_name)
                return jsonify("collection created successfully")
            except Exception as f:
                return jsonify(f)

        if operation == "Add Data":
            data_to_add = dict(request.json["dataset"])
            collection = str(request.json["choose_collection"])
            collection.insert_many(data_to_add)
            return jsonify(data_to_add + "Has Been Inserted")

        if operation == 'Delete Data':

            return

        if operation == "Drop Database":
            dbtoremove = dbconn[request.json['Choose_Database']]
            dbconn.drop_database(dbtoremove)
            return jsonify('Database Has been Dropped')



if __name__ == "__main__":
    app.run()
