from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

# Use flask_pymongo to set up mongo connection
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# route
@app.route("/")
def index():
    mars = mongo.db.mars_data.find_one()
    # print(mars) 
    #return "Hello World! add '/scrape' at the end of the url!" 
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    
    mars = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)