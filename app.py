from flask import Flask, jsonify 
app = Flask(__name__)


@app.route("/")
def home():
    x=1
    return "Home Page"

@app.route("/api/v1.0/precipitation")
def home():
    x=1
    return "Home Page"

@app.route("/api/v1.0/stations")
def home():
    x=1
    return "/api/v1.0/<start>"

@app.route("/api/v1.0/<start>/<end>")
def home():
    x=1
    return "Home Page"

@app.route("/")
def home():
    x=1
    return "Home Page"

@app.route("/")
def home():
    x=1
    return "Home Page"





if __name__ == "__main__":
    app.run(debug=True)