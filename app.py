# 1. import Flask
from flask import Flask, jsonify


import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to Weather API!<br/><br/>"
        f"Below routes are available:<br/>"
        f"""<ul>
                <li>/api/v1.0/precipitation/&lt;date&gt;</li><br/>
                <li>/api/v1.0/stations</li><br/>
                <li>/api/v1.0/tobs</li><br/>
                <li>/api/v1.0/&lt;start&gt; and /api/v1.0/&lt;end&gt;<end></li><br/>
            </ul>"""
    )

@app.route("/api/v1.0/precipitation/<date>")
def get_precipitation(date):
    #Sample execution http://127.0.0.1:5000/api/v1.0/precipitation/20170801
    try:
        engine = create_engine("sqlite:///Resources/hawaii.sqlite")
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement
        Station = Base.classes.station
        session = Session(engine)
        fmt_date = datetime.datetime(int(date[0:4]),int(date[4:6]), int(date[6:8]))
        print(fmt_date)
        end_date = fmt_date + datetime.timedelta(days=1)
        print(end_date)
        result_list=[]
        
        #for row in session.query(Measurement.station, Measurement.prcp).filter(Measurement.date == fmt_date).all():
        for row in session.query(Measurement.station, Measurement.prcp).filter(Measurement.date.between(fmt_date,end_date)).all():
            result={}
            result[row[0]] = row[1]
            result_list.append(result)
        session.close_all()
        return(jsonify(result_list))
    except Exception:
        return ("", 404)

@app.route("/api/v1.0/stations")
def get_station_list():
    #Sample execution http://127.0.0.1:5000/api/v1.0/stations
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)

    result_list=[]
    for row in session.query(Station.station, Station.name).all():
        result=[row[0], row[1]]
        result_list.append(result)
    session.close_all()
    return(jsonify(result_list))


@app.route("/api/v1.0/tobs/<date>")
def get_last_year_prcp(date):
    #Sample execution http://127.0.0.1:5000/api/v1.0/tobs/20160101
    try:
        engine = create_engine("sqlite:///Resources/hawaii.sqlite")
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement
        Station = Base.classes.station
        session = Session(engine)

        fmt_date = datetime.datetime(int(date[0:4]),int(date[4:6]), int(date[6:8]))
        print(fmt_date)
        end_date = fmt_date - datetime.timedelta(days=365)
        print(end_date)
        result_list=[]

        for row in session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date.between(end_date,fmt_date)).all():
            result={}
            result[row[0]] = {"Station":row[1], "TOBS":row[2]}
            result_list.append(result)
        session.close_all()
        return(jsonify(result_list), 200)
    except Exception:
        return ("" , 404)

@app.route("/api/v1.0/<start>")
def get_temp_status(start):
    #Sample execution http://127.0.0.1:5000/api/v1.0/20160101
    try:
        engine = create_engine("sqlite:///Resources/hawaii.sqlite")
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement
        Station = Base.classes.station
        session = Session(engine)

        start_date = datetime.datetime(int(start[0:4]),int(start[4:6]), int(start[6:8]))
        print(start_date)
        
        result={}
        for row in session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all():
            print(row[0], row[1], row[2])
            result={
                "Duration Begin Date":start_date,
                "TimeFrame Minimum Temperature":row[0],
                "TimeFrame Average Temperature":row[1],
                "TimeFrame Maximum Temperature":row[2]
            }

            session.close_all()
        return(jsonify(result), 200)
    except Exception as e:
        print(type(e).__name__)
        return ("" , 404)

@app.route("/api/v1.0/<start>/<end>")
def get_temp_status2(start, end):
    #Sample execution http://127.0.0.1:5000/api/v1.0/20160101/20170101
    try:
        engine = create_engine("sqlite:///Resources/hawaii.sqlite")
        Base = automap_base()
        Base.prepare(engine, reflect=True)
        Measurement = Base.classes.measurement
        Station = Base.classes.station
        session = Session(engine)

        start_date = datetime.datetime(int(start[0:4]),int(start[4:6]), int(start[6:8]))
        end_date = datetime.datetime(int(end[0:4]),int(end[4:6]), int(end[6:8]))
        #print(fmt_date)
        
        result={}
        for row in session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all():
            print(row[0], row[1], row[2])
            result={
                "Duration Begin Date":start_date,
                "Duration End Date":end_date,
                "TimeFrame Minimum Temperature":row[0],
                "TimeFrame Average Temperature":row[1],
                "TimeFrame Maximum Temperature":row[2]
            }

            session.close_all()
        return(jsonify(result), 200)
    except Exception as e:
        print(type(e).__name__)
        return ("" , 404)

if __name__ == "__main__":
    app.run(debug=True)