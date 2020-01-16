from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

#create database connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#route to call the scraped data from the database, insert it into the html, and render the webpage
@app.route("/")
def home():


    mars_dict = mongo.db.collection.find_one()


    return render_template("index.html", mars=mars_dict)


#route to scrape data, same as the juypter notebook

@app.route("/scrape")
def scrape():

#call scrape function
    mars_data = scrape_mars.scrape()

#overwrite the previous collection of data and replace it with the newest scrape
    mongo.db.collection.update({}, mars_data, upsert=True)


    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
