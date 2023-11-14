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
    if request.method != "POST":
        return
    operation = str(request.json["Operation"])
    if operation == 'Create Collection':
        db1 = dbconn[request.json['Choose Database']]
        collection_name = request.json['Collection']
        try:
            db1.create_collection(collection_name)
            return jsonify("collection created successfully")
        except Exception as f:
            return jsonify(f)

    elif operation == 'Delete Data':
        choose_db_todel = dbconn[request.json['Choose_Database']]
        choose_collection_todel = choose_db_todel[request.json['choose_collection']]
        dataset_todel = request.json['dataset']
        try:
            choose_collection_todel.delete_one(dataset_todel)
            return jsonify(f'{str(dataset_todel)}Has been Deleted')
        finally:
            return jsonify("dataset DNE")

    elif operation == "Add Data":
        choose_db = dbconn[request.json['Choose_Database']]
        choose_collection = choose_db[request.json['choose_collection']]
        dataset = request.json['dataset']
        choose_collection.insert_one(dataset)
        return jsonify(f'{str(dataset)}Has been Inserted')

    elif operation == "Create Database":
        dbname = str(request.json["dbname"])
        try:
            db = dbconn[dbname]
            db.create_collection(f"{dbname}_Collection")
            return jsonify(f"{dbname}Database & {dbname} Collection Created")
        except Exception as e:
            return jsonify(e)

    elif operation == "Drop Database":
        dbtoremove = dbconn[request.json['Choose_Database']]
        dbconn.drop_database(dbtoremove)
        return jsonify('Database Has been Dropped')
    elif operation == "Show Available Databases":
        dbnames = dbconn.list_database_names()
        return jsonify(dbnames)


if __name__ == "__main__":
    app.run(debug=True)
