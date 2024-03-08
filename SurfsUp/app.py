# Import the dependencies.
import datetime as dt
from datetime import datetime, timedelta
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request  # Added 'request' module

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
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
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"- List of prior (or 1) year rain totals from all stations<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"- List of prior (or 1) year temperatures from Station USC00519281<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/start'>/api/v1.0/start</a><br/>"
        f"- When given the start date (YYYY-MM-DD), calculates AVG/MAX/MIN temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/start/end'>/api/v1.0/start/end</a><br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculates AVG/MAX/MIN temperature for dates between the start and end date inclusive<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d').date()
    prev_year = last_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    precipitation_data = [{"Date": date, "PRCP": prcp} for date, prcp in results]

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station, Station.name).all()
    stations_list = [{"Station": station_id, "Name": name} for station_id, name in results]
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the previous year."""
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count().desc()).first()

    last_date = session.query(func.max(Measurement.date)).\
                filter(Measurement.station == most_active_station[0]).scalar()
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    twelve_months_ago = last_date - timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.station == most_active_station[0]).\
              filter(Measurement.date >= twelve_months_ago).all()

    tobs_data = [{"Date": date, "TOBS": tobs} for date, tobs in results]

    return jsonify(tobs_data)




@app.route("/api/v1.0/start")
def start():
    start_date = dt.date(2016, 8, 23)

    # Query the minimum, average, and maximum temperatures
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start_date).all()

    # Convert the results to a JSON format
    temp_data = {
        "Stats from start date": start_date.strftime('%Y-%m-%d'),
        "Temperature Min": results[0][0],
        "Temperature Average": results[0][1],
        "Temperature Max": results[0][2]
    }

    return jsonify(temp_data)


@app.route("/api/v1.0/start/end")
def start_end():
    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2016, 10, 23)

    # Calculate the temperature statistics between start and end dates
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Convert the results to a JSON format
    temp_json = {
        "Stats": f"from {start_date} to {end_date}",
        "Temperature Minimum": temp_data[0][0],
        "Temperature Average": temp_data[0][1],
        "Temperature Maximum": temp_data[0][2]
    }

    return jsonify(temp_json)



if __name__ == "__main__":
    app.run(debug=True)

