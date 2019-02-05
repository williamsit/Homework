#################################################
# Dependencies
#################################################

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> (Input date after /v1.0/ in YYYY-MM-DD format) e.g. /api/v1.0/2010-01-04 <br/>"
        f"/api/v1.0/<start>/<end> (Input range of dates after /v1.0/ in YYYY-MM-DD format) e.g. /api/v1.0/2010-01-04/2010-01-14"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    one_year_from_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=366)
    
    date_precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_from_date).group_by(Measurement.date).all()
    
    date_precip_dict = dict(date_precip_scores)
    return jsonify (date_precip_dict)

@app.route("/api/v1.0/stations")
def stations(): 
    print("Server received request for 'Stations' page...")

    available_stations =  session.query(Measurement.station).group_by(Measurement.station).all()
    stations_list = list(np.ravel(available_stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    print("Server received request for 'tobs' page...")
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    
    one_year_from_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=366)

    stations_query = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    most_tobs_station= stations_query[0]
    
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_from_date).filter(Measurement.station == most_tobs_station).all()
    
    tobs_list = list(tobs_data)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start=None):
    start_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    start_list=list(start_query)
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    between_date_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    
    between_date_list=list(between_date_query)
    return jsonify(between_date_list)

if __name__ == "__main__":
    app.run(debug=True)












