
# Import modules:
from meteostat import Point, Hourly, Daily, Monthly
from modules.main import get_loc, get_date, stats, chart
from datetime import date, datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
from json import loads
from pandas import Series
from plotly.subplots import make_subplots as subplot
import plotly.graph_objects as go
import streamlit as st

# Weather data codes:
dict_col = {
    #"station" : "Station",
    "temp" : "Temperature (°C)",
    "tavg" : "Average temperature (°C)",
    "tmin" : "Minimum temperature (°C)",
    "tmax" : "Maximum temperature (°C)",
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

# Weather condition codes:
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

today = date.today()
def mtst_date(current): # Get date
    with st.sidebar:
        dt = get_date(
            start = current,
            end = current,
            min = datetime(2000, 1, 1),
            max = current,
            key = "date",
        )

    return {
        0 : datetime.combine(dt["start_date"], datetime.min.time()),
        1 : datetime.combine(dt["end_date"], datetime.max.time())
    }

if "lat" not in st.session_state: st.session_state["lat"] = 0
if "long" not in st.session_state: st.session_state["long"] = 0
get_loc() # Get location

# Get data timescale:
st.sidebar.radio(
    label = "Data timescale",
    options = ("hourly", "daily", "monthly"),
    format_func = lambda x: x.capitalize(),
    horizontal = True,
    key = "data_opt",
    help = ""
)

lat = st.session_state["lat"]
long = st.session_state["long"]

# Get data:
if st.session_state["data_opt"] == "hourly":
    dt = mtst_date(today)

    mtst_data = Hourly(
        loc = Point(lat, long),
        start = dt[0],
        end = dt[1]
    ).fetch()

elif st.session_state["data_opt"] == "daily":
    dt = mtst_date(today)

    mtst_data = Daily(
        loc = Point(lat, long),
        start = dt[0],
        end = dt[1]
    ).fetch()

elif st.session_state["data_opt"] == "monthly":
    today = date(2023, 4, 1)
    dt = mtst_date(today)

    mtst_data = Monthly(
        loc = Point(lat, long),
        start = dt[0],
        end = dt[1]
    ).fetch()

# Format data:
data_json = mtst_data.to_json( # type:ignore
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)
data_json = loads(data_json)

# Store different data types:
data = {}
df = {}
rank = {}

fig_temp = go.Figure()
fig_prcp = subplot(specs = [[{"secondary_y": True}]])
fig_wnd = subplot(specs = [[{"secondary_y": True}]])
fig_misc = subplot(specs = [[{"secondary_y": True}]])
fig_coco = go.Figure()

# Add data:
timestamp = []
for i in data_json["index"]: timestamp.append(isoparse(i))

for i in data_json["columns"]:
    data[i] = []
    c = data_json["columns"].index(i)
    for j in data_json["data"]:
        if i == "coco": j[c] = wx_code[str(int(j[c]))]
        data[i].append(j[c])

df["Time"] = Series(timestamp)
for i in data:
    if i != "Time":
        df[dict_col[i]] = Series(data[i])

        if i != "coco":
            isNone = False
            for n in data[i]:
                if n == None:
                    isNone = True
                    break
            if isNone == False: rank[i] = stats(data[i])
            else: pass

    param = go.Scatter(
        name = dict_col[i],
        x = timestamp,
        y = data[i],
        mode = "lines+markers+text"
    )

    if any([
        i == "temp",
        i == "tavg",
        i == "tmax",
        i == "tmin",
        i == "dwpt"
    ]): fig_temp.add_trace(param)

    elif any([
        i == "prcp",
        i == "snow"
    ]): fig_prcp.add_trace(param)
    elif i == "rhum": fig_prcp.add_trace(param, secondary_y = True)

    elif any([
        i == "wspd",
        i == "wpgt",
    ]): fig_wnd.add_trace(param)
    elif i == "wdir": fig_wnd.add_trace(param, secondary_y = True)

    elif i == "pres": fig_misc.add_trace(param)
    elif i == "tsun": fig_misc.add_trace(param, secondary_y = True)

    elif i == "coco": fig_coco.add_trace(param)

st.dataframe(data = df, use_container_width = True)

isHourly = st.session_state["data_opt"] == "hourly"

# Temperature:
expd_temp = st.expander(label = "Temperature")
fig_temp.update_layout(
    title = "Chart",
    xaxis_title="Time",
    yaxis_title="°C",
)
with expd_temp: chart(fig_temp)

# Precipitation & relative humidity:
expd_prcp = st.expander(label = "Precipitation")
fig_prcp.update_layout(title = "Chart", xaxis_title="Time", showlegend = True)
fig_prcp.update_yaxes(title_text="mm", secondary_y=False)
if isHourly: fig_prcp.update_yaxes(title_text="%", secondary_y=True)
with expd_prcp: chart(fig_prcp)

# Wind data:
expd_wnd = st.expander(label = "Wind data")
fig_wnd.update_layout(title = "Chart", xaxis_title="Time", showlegend = True)
fig_wnd.update_yaxes(title_text="km/h", secondary_y=False)
if isHourly or st.session_state["data_opt"] == "daily": fig_wnd.update_yaxes(title_text="°", secondary_y=True)
with expd_wnd: chart(fig_wnd)

# Miscellaneous:
expd_misc = st.expander(label = "Miscellaneous")
fig_misc.update_layout(title = "Chart", xaxis_title="Time", showlegend = True)
fig_misc.update_yaxes(title_text="hPa", secondary_y=False)
fig_misc.update_yaxes(title_text="minutes", secondary_y=True)
with expd_misc: chart(fig_misc)

if isHourly:
    expd_coco = st.expander(label = "Weather condition")
    fig_coco.update_layout(
        title = "Chart",
        xaxis_title="Time",
        yaxis_title="Conditions",
    )
    with expd_coco: chart(fig_coco)

for i in rank:
    st.divider()
    st.subheader(dict_col[i])
    for j in rank[i]: st.write(j, rank[i][j])

# debug:
#st.write(st.session_state)
st.write(rank)
st.write(data)
