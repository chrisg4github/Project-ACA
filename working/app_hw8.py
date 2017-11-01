import datetime as dt
from datetime import datetime, date, time
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, and_

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
weather = Base.classes.weather
station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/vi.0/yyyy-mm-dd (on a datez0<br/>"
        f"/api/vi.0/yyyy-mm-dd,yyyy-mm-dd	(between dates)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    """Join station, weather tables and return a dictionary with name, station, date, prcp values"""
    # Query all weather stations for all data available for 2017
    results = session.query(station.name, weather.station, weather.date, weather.prcp).\
                       join(weather, station.station == weather.station).filter(weather.date.between('2017-01-01','2017-12-31')).\
                      order_by(weather.date, weather.station.asc()).all()
    # Create a dictionary from the row data and append to a list of all_stations_precip
    all_stations_precip = []
    for i in results:
        station_precip_dict = {}
        station_precip_dict["name"] = i.name
        station_precip_dict["station"] = i.station
        station_precip_dict["date"] = i.date
        station_precip_dict["prcp"] = i.prcp
        all_stations_precip.append(station_precip_dict)
    return jsonify(all_stations_precip)


@app.route("/api/v1.0/stations")
def stations():
    """Return all records from station table as a dictionary"""
    # Query stations table
    results = session.query(station.name, station.station, station.latitude,\
    	                    station.longitude, station.elevation).\
                      order_by(station.station.asc()).all()
    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for i in results:
        station_dict = {}
        station_dict["name"] = i.name
        station_dict["station"] = i.station
        station_dict["latitude"] = i.latitude
        station_dict["longitude"] = i.longitude
        station_dict["elevation"] = i.elevation
        all_stations.append(station_dict)
    return jsonify(all_stations)
   

@app.route("/api/v1.0/tobs")
def temps():
    """Join station, weather tables and return a dictionary with name, station, date, tobs values"""
    # Query all weather stations for the previous year (2016)
    results = session.query(station.name, weather.station, weather.date, weather.tobs).\
                       join(weather, station.station == weather.station).filter(weather.date.between('2016-01-01','2016-12-31')).\
                      order_by(weather.date, weather.station.asc()).all()
    # Create a dictionary from the row data and append to a list of all_stations_tobs
    all_stations_tobs = []
    for i in results:
        station_tobs_dict = {}
        station_tobs_dict["name"] = i.name
        station_tobs_dict["station"] = i.station
        station_tobs_dict["date"] = i.date
        station_tobs_dict["tobs"] = i.tobs
        all_stations_tobs.append(station_tobs_dict)
    return jsonify(all_stations_tobs)


@app.route("/api/v1.0/<start_date>")
def calc_temps1(start_date):
    """return min_tobs, avg_tobs, max_tobs values for one day using all available stations"""
    tobs_mam = session.query(func.min(weather.tobs),func.avg(weather.tobs),\
                func.max(weather.tobs)).filter(weather.date == start_date).all()
    # Convert list of tuples into normal list
    all_values = list(np.ravel(tobs_mam))
    return jsonify(all_values)   


@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps2(start_date, end_date):
    """return min_tobs, avg_tobs, max_tobs values for a date range using all available stations"""
    tobs_mam = session.query(func.min(weather.tobs),func.avg(weather.tobs),\
                func.max(weather.tobs)).filter(weather.date.between(start_date, end_date)).all()
    # Convert list of tuples into normal list
    all_values = list(np.ravel(tobs_mam))
    return jsonify(all_values)


if __name__ == '__main__':
    app.run(debug=True)
