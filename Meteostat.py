
from input_req import get_loc, get_date
from datetime import date, datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
from json import loads
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from meteostat import Point, Hourly, Daily, Monthly

dict_col = {
    "station" : "Station",
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

st.sidebar.radio(
    label = "Data timescale",
    options = ("hourly", "daily", "monthly"),
    format_func = lambda x: x.capitalize(),
    horizontal = True,
    key = "data_opt",
    help = ""
)

dt = get_date(
    start = date.today(),
    end = date.today(),
    min = datetime(2000, 1, 1),
    max = date.today(),
    key = "date",
)

start_date = datetime.combine(dt["start_date"], datetime.min.time())
end_date = datetime.combine(dt["end_date"], datetime.max.time())

if st.session_state["data_opt"] == "hourly":
    mtst_data = Hourly(
        loc = Point(st.session_state["lat"], st.session_state["long"]),
        start = start_date,
        end = end_date
    ).fetch()

if st.session_state["data_opt"] == "daily":
    mtst_data = Daily(
        loc = Point(st.session_state["lat"], st.session_state["long"]),
        start = start_date,
        end = end_date
    ).fetch()

if st.session_state["data_opt"] == "monthly":
    mtst_data = Monthly(
        loc = Point(st.session_state["lat"], st.session_state["long"]),
        start = start_date,
        end = end_date
    ).fetch()    

data_json = mtst_data.to_json( # type:ignore
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)
data_json = loads(data_json)

data = {}
df = {}

fig_temp = go.Figure()
fig_rhum = go.Figure()
fig_prcp = go.Figure()
fig_dir = go.Figure()
fig_spd = go.Figure()
fig_pres = go.Figure()
fig_coco = go.Figure()

data["Time"] = []
for i in data_json["index"]: data["Time"].append(isoparse(i))

for i in data_json["columns"]:
    data[i] = []
    c = data_json["columns"].index(i)
    for j in data_json["data"]:
        if i == "coco": j[c] = wx_code[str(int(j[c]))]
        data[i].append(j[c])

df["Time"] = pd.Series(data["Time"])
for i in data:
    if i != "Time": df[dict_col[i]] = pd.Series(data[i])

    if any([
        i == "temp",
        i == "tavg",
        i == "tmax",
        i == "tmin",
        i == "dwpt"
    ]):
        fig_temp.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

    if i == "rhum":
        fig_rhum.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

    if any([
        i == "prcp",
        i == "snow",
    ]):
        fig_prcp.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

    if i == "wdir":
        fig_dir.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

    if any([
        i == "wspd",
        i == "wpgt",
    ]):
        fig_spd.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

    if i == "pres":
        fig_pres.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

    if i == "coco":
        fig_coco.add_trace(go.Scatter(
            x = data["Time"],
            y = data[i],
            name = dict_col[i],
            mode = "lines+markers"
        ))

st.dataframe(
    data = df,
    use_container_width = True,
)

fig_temp.update_layout(
    title = st.session_state["data_opt"].capitalize() + " temperature",
    xaxis_title="Time",
    yaxis_title="°C",
)

st.plotly_chart(
    figure_or_data = fig_temp,
    use_container_width = True,
    theme = "streamlit"
)

if st.session_state["data_opt"] == "hourly":
    fig_rhum.update_layout(
        title = st.session_state["data_opt"].capitalize() + " relative humidity",
        xaxis_title="Time",
        yaxis_title="%",
    )

    st.plotly_chart(
    figure_or_data = fig_rhum,
    use_container_width = True,
    theme = "streamlit"
    )

fig_prcp.update_layout(
    title = st.session_state["data_opt"].capitalize() + " precipitation",
    xaxis_title="Time",
    yaxis_title="mm",
)

st.plotly_chart(
    figure_or_data = fig_prcp,
    use_container_width = True,
    theme = "streamlit"
)

if st.session_state["data_opt"] == "hourly" or st.session_state["data_opt"] == "daily":
    fig_dir.update_layout(
        title = st.session_state["data_opt"].capitalize() + " wind direction",
        xaxis_title="Time",
        yaxis_title="°",
    )

    st.plotly_chart(
    figure_or_data = fig_dir,
    use_container_width = True,
    theme = "streamlit"
    )

fig_spd.update_layout(
    title = st.session_state["data_opt"].capitalize() + " wind speed",
    xaxis_title="Time",
    yaxis_title="km/h",
)

st.plotly_chart(
    figure_or_data = fig_spd,
    use_container_width = True,
    theme = "streamlit"
)

fig_pres.update_layout(
    title = st.session_state["data_opt"].capitalize() + " average sea-level air pressure",
    xaxis_title="Time",
    yaxis_title="hPa",
)

st.plotly_chart(
    figure_or_data = fig_pres,
    use_container_width = True,
    theme = "streamlit"
)

if st.session_state["data_opt"] == "hourly":
    fig_coco.update_layout(
        title = st.session_state["data_opt"].capitalize() + " weather condition",
        xaxis_title="Time",
        yaxis_title="",
    )

    st.plotly_chart(
    figure_or_data = fig_coco,
    use_container_width = True,
    theme = "streamlit"
    )

# debug:
#st.write(data)
#st.write(st.session_state)
