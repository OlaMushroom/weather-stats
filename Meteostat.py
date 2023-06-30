
from input_req import get_loc, get_date
from datetime import date, datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
import json
import pandas as pd
import streamlit as st
from meteostat import Point, Hourly, Daily

dict_col = {
    "station" : "Station",
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
    "coco" : "Weather condition"
}

wx_code = {
    "1" : "Clear",
    "2" : "Fair",
    "3" : "Cloudy",
    "4" : "Overcast",
    "5" : "Fog",
    "6" : "Freezing Fog",
    "7" : "Light Rain",
    "8" : "Rain",
    "9" : "Heavy Rain",
    "10" : "Freezing Rain",
    "11" : "Heavy Freezing Rain",
    "12" : "Sleet",
    "13" : "Heavy Sleet",
    "14" : "Light Snowfall",
    "15" : "Snowfall",
    "16" : "Heavy Snowfall",
    "17" : "Rain Shower",
    "18" : "Heavy Rain Shower",
    "19" : "Sleet Shower",
    "20" : "Heavy Sleet Shower",
    "21" : "Snow Shower",
    "22" : "Heavy Snow Shower",
    "23" : "Lightning",
    "24" : "Hail",
    "25" : "Thunderstorm",
    "26" : "Heavy Thunderstorm",
    "27" : "Storm",
}

get_loc()

dt = get_date(
    start = date.today(),
    end = date.today(),
    min = datetime(2000, 1, 1),
    max = date.today(),
    key = "date",
)

start_date = datetime.combine(dt["start_date"], datetime.min.time())
end_date = datetime.combine(dt["end_date"], datetime.max.time())

# Get daily data:
mtst_data_df = Hourly(
    loc = Point(49.2497, -123.1193, 70), # Create Point for Vancouver, BC
    start = start_date,
    end = end_date
).fetch()

data_json = mtst_data_df.to_json(
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)
data_json = json.loads(data_json)

data = {}
data["Time"] = []
for i in data_json["index"]: data["Time"].append(isoparse(i))

for i in data_json["columns"]:
    data[dict_col[i]] = []
    c = data_json["columns"].index(i)
    for j in data_json["data"]: data[dict_col[i]].append(j[c])

for i in data[dict_col["coco"]]:
    j = data[dict_col["coco"]].index(i)
    data[dict_col["coco"]][j] = wx_code[str(int(i))]

df = {}
df["Time"] = pd.Series(data_json["index"])
for i in data: df[i] = pd.Series(data[i])

st.dataframe(
    data = df,
    use_container_width = True,
)

# debug:
st.write(data)
