### IMPORTS
# Python import
import datetime as dt
import numpy as np
import pandas as pd

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
Base = automap_base()

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

#[recip route]
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)


#Get stations
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(station.station).all() #get all stations
    stations = list(np.ravel(results)) #results into a list
    return jsonify(stations)

#get monthly temp
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prev_year).all()
    temps = list(np.ravel(results)) #unravel into a list
    return(jsonify(temps))

#Statistic Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(measurement.tobs),\
        func.avg(measurement.tobs), func.max(measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)