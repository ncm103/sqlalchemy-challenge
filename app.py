#Flask 
#Imports
from matplotlib import style
import matplotlib.pyplot as plt


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into the model
Base = automap_base()
# reflect tables
Base.prepare(engine, reflect=True)

# saving table references
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)


#Sort date description and grab the first result

#Get start date by subtracting 1 from year

#Get most active station

#create a flask name
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#Display the last 12 months of precipitation
    last_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    prec_scores = session.query(measurement.date, measurement.prcp).filter(measurement.date>last_year).all()

    precipitation = {date:pcrp for date,pcrp in prec_scores}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = session.query(station.station).all()
    stations = list(np.ravel(stations))
    return jsonify(stations)


#@app.route("/api/v1.0/tobs")
#def tobs():
#    session = Session(engine)
#
 #   tobs_info = 
  #  tobs_info = list(np.ravel(tobs)
   # return jsonify(tobs)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")   
def trip_dates(start=None, end=None):
    session = Session(engine)

    dates = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    dates = list(np.ravel(dates))
    return jsonify(dates)





if __name__ == '__main__':
    app.run(debug=True)