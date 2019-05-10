from flask import Flask, render_template, redirect
from flask_pymongo import pymongo
import scrape_mars
 
# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Set route
@app.route('/')
def home():
    # Store the entire team collection in a list
    mars_db = client.db.mars.find_one()
    #return render_template('index.html')
    #print(mars)

    # Return the template with the teams list passed in
    return render_template('index.html', mars=mars_db)

# Set route
@app.route('/scrape')
def scrape():
    mars_db = client.db.mars
    mars_data = scrape_mars.scrape_info()
    mars_db.update({},mars_data, upsert = True)

    return redirect('/', code = 302)

if __name__ == "__main__":
    app.run(debug=True)
