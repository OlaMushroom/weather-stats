
from geolocation_req import *
from datetime import datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
import json
import pandas as pd
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
    j = data_json["index"].index(i)
    data_json["index"][j] = isoparse(i)

d = {}
df = {}

for i in data_json["columns"]:
    d[dict_columns[i]] = []
    c = data_json["columns"].index(i)

    for j in data_json["data"]:
        data_list = j
        d[dict_columns[i]].append(data_list[c])

df[dict_columns["time"]] = pd.Series(data_json["index"])
for i in d: df[i] = pd.Series(d[i])

st.dataframe(
    data = df,
    use_container_width = True,
)

# debug:
st.write(data_json)
