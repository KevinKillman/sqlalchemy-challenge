from flask import Flask, jsonify 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import datetime
import numpy as np
import string

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
inspector = inspect(engine)

session = Session(engine)

for c in session.query(Measurement.date).order_by(Measurement.date.desc()).first():
    first_date = c
date = [int(x) for x in first_date.split("-")]

first_date = (datetime.date(date[0],date[1],date[2]) - dt.timedelta(days=365))
station_counts=[]
for c in session.query(Station.station,(func.count(Station.station))).filter(Station.station==Measurement.station).group_by(Station.station).order_by(func.count(Station.station).desc()):
    station_counts.append(c)
highest_id=station_counts[0][0]


app = Flask(__name__)


@app.route("/")
def home():
    x=1
    return "Valid Routes\n/api/v1.0/precipitation \n "

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    first_date = datetime.date(date[0],date[1],date[2])

    last_12_month_query = session.query(Measurement.date, Measurement.prcp).\
        filter((Measurement.date)>(datetime.date(date[0],date[1],date[2]) - dt.timedelta(days=365))).order_by(Measurement.date.desc())
    prec_return = {}
    for result in last_12_month_query:
        prec_return.update({result.date:result.prcp})

    return jsonify(prec_return)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = []
    for result in session.query(Station.station):
        stations.append(result)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_return = []
    for result in session.query(Measurement.date, Measurement.tobs).filter((Measurement.date)>(first_date)).order_by(Measurement.date.desc()):
        tobs_return.append(result.tobs)
        
    
    return jsonify(tobs_return)

@app.route("/api/v1.0/<start>")
def startOnly(start):
    session = Session(engine)
    if len(start) !=8 or start.isdigit() == False:
        return "Please Enter Date as YYYYMMDD, no other characters"
    else:
        start_date = dt.datetime.strptime(start, '%Y%m%d')
        results = {}
        for result in session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>start_date):
            results.update({'Minimum':result[0],
                           'Maximum':result[1],
                           'Average':result[2]})
        return jsonify(results)

@app.route('/api/v1.0/<start>/<end>')
def startEnd(start, end):
    session = Session(engine)
    if len(start) !=8 or start.isdigit() == False or len(end) != 8 or end.isdigit() == False:
        return "Please Enter Date as YYYYMMDD, no other characters"
    else:
        start_date = dt.datetime.strptime(start, '%Y%m%d')
        end_date = dt.datetime.strptime(end, '%Y%m%d')
        results = {}
        for result in session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date>start_date).filter(Measurement.date<end_date):
            results.update({'Minimum':result[0],
                           'Maximum':result[1],
                           'Average':result[2]})
        return jsonify(results)







if __name__ == "__main__":
    app.run(debug=True)