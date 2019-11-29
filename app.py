### IMPORTS
# Python import
import datetime as dt
import numpy as numpy
import pandas as import pd

# SQLite 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask (website)
from flask import Flask, jsonify

#set up database
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect DB into class
Base = automatp_base()

#Reflect DB into Tables 
Base.prepare(engine, reflect=True)

#save references
measurement = Base.classes.measurement
station = Base.classes.station

#Python session link
session = Session(engine)

#Flask setup - application called 'app' --> needs to be at top of work
app = Flask(__name__) # run locally --> variable will be __main__

################################ import into example.py
#import app
#print("example __name__ = %s", __name__)
#if __name__ == "__main__":
#print("example is being run directly.")
#else:
#print("example is being imported")
################################ 

#welcome route
@app.route("/")

def welcome():
    return(
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
	)