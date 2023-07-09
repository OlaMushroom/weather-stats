"""Meteostat weather data"""
# Import modules:
from meteostat import Point, Hourly, Daily, Monthly, Normals, units
from main import get_loc, get_date, stats, chart, geomap

from collections import Counter
from json import loads
from datetime import date, datetime
#from dateutil.relativedelta import relativedelta
from dateutil.parser import isoparse

from pandas import Series
from plotly.subplots import make_subplots as subplot
import plotly.graph_objects as go
#from PIL import Image

import streamlit as st
from streamlit_extras.buy_me_a_coffee import button as buymeacoffee

st.set_page_config(
    page_title = "Meteostat",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        "Get Help" : "https://github.com/OlaMushroom/weather-stats/wiki",
        "Report a bug" : "https://github.com/OlaMushroom/weather-stats/issues",
        "About" : "Data provider: [Meteostat](https://meteostat.net) — Map library: [Folium](https://python-visualization.github.io/folium)"
    }
)

wx_code = { # Weather condition codes
    "1" : ["Clear", ""],
    "2" : ["Fair", ""],
    "3" : ["Cloudy ☁️", ""],
    "4" : ["Overcast", "./static/overcast.png"],
    "5" : ["Fog", "./static/fog.png"],
    "6" : ["Freezing Fog", "./static/freezing_fog.png"],
    "7" : ["Light Rain", "./static/rain.png"],
    "8" : ["Rain", "./static/rain.png"],
    "9" : ["Heavy Rain", "./static/heavy_rain.png"],
    "10" : ["Freezing Rain", "./static/freezing_rain.png"],
    "11" : ["Heavy Freezing Rain", "./static/freezing_rain.png"],
    "12" : ["Sleet", "./static/sleet.png"],
    "13" : ["Heavy Sleet", "./static/sleet.png"],
    "14" : ["Light Snowfall", ""],
    "15" : ["Snowfall", ""],
    "16" : ["Heavy Snowfall", ""],
    "17" : ["Rain Shower", ""],
    "18" : ["Heavy Rain Shower", ""],
    "19" : ["Sleet Shower", ""],
    "20" : ["Heavy Sleet Shower", ""],
    "21" : ["Snow Shower", ""],
    "22" : ["Heavy Snow Shower", ""],
    "23" : ["Lightning", ""],
    "24" : ["Hail", ""],
    "25" : ["Thunderstorm", ""],
    "26" : ["Heavy Thunderstorm", ""],
    "27" : ["Storm", ""],
}

dict_abbr = { # Abbreviations
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
    "coco" : "Weather condition",
    "mean" : "Mean",
    "med_l" : "Low median",
    "med_h" : "High median",
    "mode" : "Mode",
    "freq" : "Frequency",
}

list_temp = ["temp", "tavg", "tmin", "tmax", "dwpt"]
list_prcp = [ "rhum", "prcp", "snow"]
list_wind = ["wdir", "wspd", "wpgt"]
list_misc = ["pres", "tsun"]

def mtst_date( # Get date
        min: date = date(1973, 1, 1),
        max: date = date.today(),
):
    with st.sidebar:
        dt = get_date(
            start = max,
            end = max,
            min = min,
            max = max
        )

    return {
        0 : datetime.combine(dt["start_date"], datetime.min.time()),
        1 : datetime.combine(dt["end_date"], datetime.max.time())
    }

lat, long = 0, 0

loc = get_loc()
if loc != None:
    lat = loc["lat"]
    long = loc["long"]

    st.write("Latitude:", lat, "—", "Longitude:", long)
    geomap(lat, long)
    
dict_data_opt = {
    "hourly" : "Hourly",
    "daily" : "Daily",
    "monthly" : "Monthly (from August 1981)",
    #"normals" : "Climate Normals"
}

data_opt = st.sidebar.radio(
    label = "Timescale",
    options = dict_data_opt.keys(),
    format_func = lambda x: dict_data_opt.get(x),
    horizontal = True,
    key = "data_opt",
    help = ""
)

def get_data(): # Get data
    with st.sidebar:
        if data_opt == "hourly":
            dt = mtst_date()
            return Hourly(
                loc = Point(lat, long),
                start = dt[0],
                end = dt[1]
            ).fetch()

        elif data_opt == "daily":
            dt = mtst_date()
            return Daily(
                loc = Point(lat, long),
                start = dt[0],
                end = dt[1]
            ).fetch()

        elif data_opt == "monthly":
            dt = mtst_date(min = date(1981, 8, 1))

            return Monthly(
                loc = Point(lat, long),
                start = dt[0],
                end = dt[1]
            ).fetch()

data_raw = get_data() # Store data

data_json = data_raw.to_json( # type:ignore
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)
data_json = loads(data_json)

# Reorganize data:
data = {}
timestamp = []
wx_img = []

for i in data_json["index"]: timestamp.append(isoparse(i))

for i in data_json["columns"]:
    data[i] = []
    col = data_json["columns"].index(i)
    for j in data_json["data"]:
        if i == "coco" and j[col] != None:
            k = str(int(j[col]))
            j[col] = wx_code[k][0]
            wx_img.append(wx_code[k][1])
        data[i].append(j[col])

# Create plotly figures:
fig_temp = go.Figure()
fig_prcp = subplot(specs = [[{"secondary_y": True}]])
fig_wind = subplot(specs = [[{"secondary_y": True}]])
fig_misc = subplot(specs = [[{"secondary_y": True}]])
fig_wxco = go.Figure()

rank = {}
def ranking(): # Create statistics ranking
    for n in data[i]:
        if n == None: return True
    rank[i] = stats(data[i])

# Process data to dataframe and figures:
df = {}
df["Time"] = Series(timestamp)
for i in data:
    if i != "Time": df[dict_abbr[i]] = Series(data[i])
    if i != "coco" and len(data[i]) != 0: ranking()
    elif i == "coco": df["IMG"] = Series(wx_img)

    param = go.Scatter(
        name = dict_abbr[i],
        x = timestamp,
        y = data[i],
        mode = "lines+markers+text"
    )

    if i in list_temp: fig_temp.add_trace(param)

    elif any([
        i == "prcp",
        i == "snow"
    ]): fig_prcp.add_trace(param)
    elif i == "rhum": fig_prcp.add_trace(param, secondary_y = True)

    elif any([
        i == "wspd",
        i == "wpgt",
    ]): fig_wind.add_trace(param)
    elif i == "wdir": fig_wind.add_trace(param, secondary_y = True)

    elif i == "pres": fig_misc.add_trace(param)
    elif i == "tsun": fig_misc.add_trace(param, secondary_y = True)

    elif i == "coco": fig_wxco.add_trace(param)

st.dataframe( # Display dataframe
    data = df,
    use_container_width = True,
    column_config = {"IMG" : st.column_config.ImageColumn("Image")}
)

def fig_update(fig, y1: str): # Update figure
    fig.update_layout(
        title = "Chart",
        xaxis_title = "Time",
        yaxis_title = y1,
        showlegend = True
    )
    fig.update_xaxes(rangeslider_visible = True) # Update figure with x-axis range slider

def y2(fig, text): fig.update_yaxes(title_text = text, secondary_y = True) # Update figure with two y-axes

def rank_show(set): # Display statistics
    for data in rank:
        if data in set:
            st.divider()
            st.subheader(dict_abbr[data])
            for stat in rank[data]:
                if isinstance(rank[data][stat], (int, float, str)): st.metric(dict_abbr[stat], rank[data][stat]) # Display metrics of statistics

            with st.expander("Frequency"):
                # Display frequency dataframe:
                st.dataframe(
                    data = rank[data]["freq"],
                    use_container_width = True,
                    column_config = {
                        "_index" : st.column_config.Column(
                            label = "Value",
                            help = "",
                        ),

                        "value" : st.column_config.Column(
                            label = "Frequency",
                            help = "",
                        )
                    }
                )
                
                # Create frequency figure:
                fig_freq = go.Figure(data = [go.Bar(
                        x = list(rank[data]["freq"].keys()),
                        y = list(rank[data]["freq"].values()),
                        textposition = "auto",
                    )])

                fig_freq.update_layout(
                    title = "Chart",
                    xaxis_title = "Value",
                    yaxis_title = "Frequency"
                )
                fig_freq.update_xaxes(rangeslider_visible = True)
                chart(fig_freq) # Display frequency figure

# Update figures:
fig_update(fig_temp, "°C")

fig_update(fig_prcp, "mm")

fig_update(fig_wind, "km/h")

fig_update(fig_misc, "hPa")
y2(fig_misc, "minutes")

tab_temp, tab_prcp, tab_wind, tab_misc, tab_wxco = st.tabs([ # Create tabs to organize & display data
    "Temperature",
    "Precipitation",
    "Wind data",
    "Miscellaneous",
    "Weather conditions"
])

if data_opt == "hourly": # More updates to figures when current data timescale is hourly
    y2(fig_prcp, "%")
    fig_update(fig_wxco, "Conditions")
    
    # Create frequency figure for weather conditions:
    wxco_freq = Counter(data["coco"])
    fig_wxco_freq = go.Figure(data = [go.Bar(
            x = list(wxco_freq.keys()),
            y = list(wxco_freq.values()),
            textposition = "auto",
    )])

    fig_wxco_freq.update_layout(
        title = "Frequency",
        xaxis_title = "Value",
        yaxis_title = "Frequency"
    )
    fig_wxco_freq.update_xaxes(rangeslider_visible = True)

    # Display figures for weather conditions:
    with tab_wxco:
        chart(fig_wxco)
        chart(fig_wxco_freq)    

isWDIR = data_opt == "hourly" or data_opt == "daily"

if isWDIR:
    y2(fig_wind, "°")

#    fig_wdir = go.Figure(data = go.Scatterpolar(
#        r = list(rank["wdir"]["freq"].values()),
#        theta = list(rank["wdir"]["freq"].keys()),
#        mode = "markers",
#    ))
#    fig_wdir.update_layout(showlegend = True)

# Display figures:
with tab_temp:
    chart(fig_temp)
    rank_show(list_temp)

with tab_prcp:
    chart(fig_prcp)
    rank_show(list_prcp)

with tab_wind:
    chart(fig_wind)
    #if isWDIR: chart(fig_wdir)
    rank_show(list_wind)

with tab_misc:
    chart(fig_misc)
    rank_show(list_misc)

buymeacoffee(
    username = "olamushroom",
    text = "Coffee, please!",
    emoji = "☕",
    font = "Poppins",
    width = 300,
    floating = True
)

# debug:
#st.write(st.session_state)
#st.write(rank)
st.write(data)
