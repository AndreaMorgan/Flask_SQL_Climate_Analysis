import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Welcome to my climate app. <br/>All available data is between the dates of January 1, 2010, and August 23, 2017. <br/>Here are the available API Routes:<br/><br/>"
        f"Returns precipitation data:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"Returns station names:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"Returns temperature data:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Returns data after date (YYYY-MM-DD format):<br/>"
        f"/api/v1.0/<start><br/><br/>"
        "Returns data between dates (YYYY-MM-DD format):<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Convert the query results to a Dictionary using date as the key and prcp as the value"""
    """Return the JSON representation of your dictionary"""

    session = Session(engine)

    year_prior = dt.date(2017,8,23)-dt.timedelta(weeks = 52)
    query_date=str(year_prior)

    results=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > query_date).\
        order_by(Measurement.date).all()

    session.close()

    all_rainfall = []
    for date, precipitation in results:
        rainfall_dict = {}
        rainfall_dict["date"] = date
        rainfall_dict["precipitation"] = precipitation
        all_rainfall.append(rainfall_dict)
        
    return jsonify(all_rainfall)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    session = Session(engine)

    station_results = session.query(Station.id, Station.station, Station.name)

    session.close()

    all_stations = []
    for id, station, name in station_results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    year_prior = dt.date(2017,8,23)-dt.timedelta(weeks = 52)
    query_date=str(year_prior)

    results=session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > query_date).\
        order_by(Measurement.date).all()

    session.close()

    all_tobs = []
    for date, temp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = temp
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def startdate(start):
    
    session = Session(engine)

    my_trip=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()

    session.close()

    all_start = []
    for min, avg, max in my_trip:
        start_dict = {}
        start_dict["min"] = min
        start_dict["avg"] = avg
        start_dict["max"] = max
        all_start.append(start_dict)

    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")

def daterange(start, end):

    session = Session(engine)

    my_trip=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).\
        group_by(Measurement.date).all()

    session.close()

    all_startend = []
    for min, avg, max in my_trip:
        startend_dict = {}
        startend_dict["min"] = min
        startend_dict["avg"] = avg
        startend_dict["max"] = max
        all_startend.append(startend_dict)

    return jsonify(all_startend)


if __name__ == "__main__":
    app.run(debug=True)