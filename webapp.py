from flask import Flask, jsonify, redirect, request, render_template
from parse import PathParser
from store import DatabaseHandler
from urllib.parse import urlencode

app = Flask(__name__)

parser = PathParser()
dbHandler = DatabaseHandler("db.dat")

"""
me/ is proxied to /redirect/
me.links/static/ is proxied to /static/
me.links/ is proxied to /portal/
"""

@app.route("/redirect/<path:arg>")
def me(arg):
    key, query = parser.parse(arg.strip())
    # lookup DB
    link, has_query = dbHandler.get(key)
    
    # key not found
    if link is None:
        redirect_base_url = "http://me.links"
        params = {
            "referrer" : key
        }
        redirect_url = redirect_base_url + "?" + urlencode(params)
        
        return redirect(redirect_url)
    
    # pass query if querying is allowed
    if has_query and query:
        link += query
    
    return redirect(link)

@app.route("/portal/", methods=['GET'])
def home():
    referrer = request.args.get("referrer")
    if referrer:
        return render_template("index.html", has_referrer=True, referrer=referrer)
    return render_template("index.html", has_referrer=False)

@app.route("/portal/search", methods=['GET'])
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

@app.route("/portal/check", methods=['GET'])
def check():
    key = request.args.get('key')
    return jsonify(
        {
            "isKey" : parser.is_valid(key) and dbHandler.has_key(key)
        }
    )
    
@app.route("/portal/save", methods=['POST'])
def save():
    key = request.form.get("key")
    link = request.form.get("link")
    has_query = request.form.get("has_query")
    if not parser.is_valid(key):
        return "INVALID KEY", 400
    dbHandler.set(key, link, has_query)
    return "OK", 200
    
@app.route('/portal/delete', methods=['POST'])
def delete():
    key = request.form.get("key")
    if parser.is_valid(key) and dbHandler.has_key(key):
        dbHandler.pop(key)
        return "OK", 200
    return "Bad Request", 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
