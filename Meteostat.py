
from geolocation_req import *
from datetime import datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
import json
#from pandas import DataFrame
import streamlit as st
from meteostat import Point, Hourly, Daily

dict_columns = {
    "station" : "Station",
    "time" : "Time",
    "month" : "Month",
    "start" : "First year (YYYY) of the reference period",
    "end" : "End year (YYYY) of the reference period",
    "temp" : "Temperature (°C)",
    "tavg" : "Average temperature (°C)",
    "tmin" : "Minimum Temperature (°C)",
    "tmax" : "Maximum Temperature (°C)",
    "dwpt" : "Dew point (°C)",
    "rhum" : "Relative humidity (%)",
    "prcp" : "Precipitation (mm)",
    "snow" : "Snow depth (mm)",
    "wdir" : "Wind direction (°)",
    "wspd" : "Wind speed (km/h)",
    "wpgt" : "Peak wind gust (km/h)",
    "pres" : "Average sea-level air pressure (hPa)",
    "tsun" : "Sunshine total (minutes)",

}

get_loc()

# Get daily data:
data = Daily(
    loc = Point(49.2497, -123.1193, 70), # Create Point for Vancouver, BC
    start = datetime(2018, 1, 1),
    end = datetime(2018, 1, 2)
).fetch()

data_json = data.to_json(
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)
data_json = json.loads(data_json)

for i in data_json["index"]:
    st.write(isoparse(i))

# debug:
st.write(data)
st.write(data_json)
