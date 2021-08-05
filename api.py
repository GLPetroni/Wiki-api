import wiki_scraper
import json
from flask import request
from flask import Flask

app = Flask(__name__)

#@app.route("/")
@app.route("/", methods=['GET'])

###################################
# Call to wiki_scraper.py main function
# ToDo: 1. figure out acceptance of arguments
#       2. deploy
####################################
def scrape():
   tmp = request.args
   value = tmp["u"]
   return wiki_scraper.main(value)
   #return wiki_scraper.main(request.args["u"])
