from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars
import collections  # From Python standard library.
import bson
from bson.codec_options import CodecOptions
 
# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/mars'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Set route
@app.route('/')
def home():
    # Store the entire team collection in a list
    mars = client.db.mars.find_one()
    #return render_template('index.html')
    #print(mars)

    # Return the template with the teams list passed in
    return render_template('index.html', mars=mars)

# Set route
@app.route('/scrape')
def scrape():
    mars = client.db.mars
#    print(mars)
    mars_data = scrape_mars.scrape_info()
    mars.update_one({},mars_data, upsert = True)

    return redirect('/', code = 302)

if __name__ == "__main__":
    app.run(debug=True)
