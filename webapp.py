from flask import Flask, redirect, request
from parse import PathParser
from store import DatabaseHandler
from urllib.parse import urlencode

app = Flask(__name__)

parser = PathParser()
dbHandler = DatabaseHandler("db.dat")

@app.route("/<path:arg>")
def go(arg):
    key, query = parser.parse(arg.strip())
    # lookup DB
    link, has_query = dbHandler.get(key)
    
    # key not found
    if link is None:
        redirect_base_url = "http://go.links"
        params = {
            "referrer" : key
        }
        redirect_url = redirect_base_url + "?" + urlencode(params)
        
        return redirect(redirect_url)
    
    # pass query if querying is allowed
    if has_query and query:
        link += query
    
    return redirect(link)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
