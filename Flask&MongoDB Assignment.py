# The Objective of this assignment is to make an url page which can
# 1. create a dataset inside mongodb
# 2. update into the dataset
# 3. insertion of data into the dataset
# 4. delete from table
# 5. download data from database

import pymongo
from flask import Flask, request, jsonify

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
            dataset = request.json['dataset']
            choose_db = dbconn[request.json['Choose_Database']]
            choose_collection = choose_db[request.json['choose_collection']]
            choose_collection.insert_one(dataset)
            return jsonify(str(dataset) + 'Has been Inserted')

        if operation == 'Delete Data':
            dataset_todel = request.json['dataset']
            choose_db_todel = dbconn[request.json['Choose_Database']]
            choose_collection_todel = choose_db_todel[request.json['choose_collection']]
            try:
                choose_collection_todel.delete_one(dataset_todel)
                return jsonify(str(dataset_todel) + 'Has been Deleted')
            finally:
                return jsonify("dataset DNE")

        if operation == "Drop Database":
            dbtoremove = dbconn[request.json['Choose_Database']]
            dbconn.drop_database(dbtoremove)
            return jsonify('Database Has been Dropped')


if __name__ == "__main__":
    app.run(debug=True)
