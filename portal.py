from ast import parse
from distutils.log import debug
from flask import Flask, jsonify, redirect, request, render_template, url_for
from parse import PathParser
from store import DatabaseHandler
from urllib.parse import urlencode

app = Flask(__name__)
dbHandler = DatabaseHandler("db.dat")
parser = PathParser()

@app.route("/", methods=['GET'])
def home():
    referrer = request.args.get("referrer")
    if referrer:
        return render_template("index.html", has_referrer=True, referrer=referrer)
    return render_template("index.html", has_referrer=False)

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    # invalid search keyword
    if not parser.is_valid(query):
        return jsonify(
            {
                "status" : "INVALID",
                "data" : []
            }
        )
    matches = dbHandler.match(query.lower().strip())
    return jsonify(
        {
            "status" : "FOUND" if matches else "NOT FOUND",
            "data" : matches
        }
    )

@app.route("/check", methods=['GET'])
def check():
    key = request.args.get('key')
    return jsonify(
        {
            "isKey" : parser.is_valid(key) and dbHandler.has_key(key)
        }
    )
    
@app.route("/save", methods=['POST'])
def save():
    key = request.form.get("key")
    link = request.form.get("link")
    has_query = request.form.get("has_query")
    print(key, link, has_query)
    if not parser.is_valid(key):
        return "INVALID KEY", 400
    dbHandler.set(key, link, has_query)
    return "OK", 200
    
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form.get("key")
    if parser.is_valid(key) and dbHandler.has_key(key):
        dbHandler.pop(key)
        return "OK", 200
    return "Bad Request", 400
    
if __name__ == '__main__':
    app.run(port=5001, debug=True)
