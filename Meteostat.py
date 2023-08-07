"""Meteostat weather data"""
# Import modules:
from meteostat import Point, Hourly, Daily, Monthly#, units
from main import get_loc, get_date, stats, chart, geomap

from time import perf_counter
from collections import Counter
from json import loads

from datetime import date, datetime
#from dateutil.relativedelta import relativedelta
from dateutil.parser import isoparse

from pandas import DataFrame, Series

import plotly.graph_objects as go
from plotly.subplots import make_subplots as subplot

import streamlit as st
from streamlit_extras.buy_me_a_coffee import button as buymeacoffee

st.set_page_config( # Page configuration
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
    "3" : ["Cloudy", ""],
    "4" : ["Overcast", "app/static/overcast.png"],
    "5" : ["Fog", "app/static/fog.png"],
    "6" : ["Freezing Fog", "app/static/freezing_fog.png"],
    "7" : ["Light Rain", "app/static/rain.png"],
    "8" : ["Rain", "app/static/rain.png"],
    "9" : ["Heavy Rain", "app/static/heavy_rain.png"],
    "10" : ["Freezing Rain", "app/static/freezing_rain.png"],
    "11" : ["Heavy Freezing Rain", "app/static/freezing_rain.png"],
    "12" : ["Sleet", "app/static/sleet.png"],
    "13" : ["Heavy Sleet", "app/static/sleet.png"],
    "14" : ["Light Snowfall", "app/static/snowfall.png"],
    "15" : ["Snowfall", "app/static/snowfall.png"],
    "16" : ["Heavy Snowfall", "app/static/heavy_snowfall.png"],
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
    "temp" : "Temperature",
    "tavg" : "Average temperature",
    "tmin" : "Minimum temperature",
    "tmax" : "Maximum temperature",
    "dwpt" : "Dew point",
    "rhum" : "Relative humidity",
    "prcp" : "Precipitation",
    "snow" : "Snow depth",
    "wdir" : "Wind direction",
    "wspd" : "Wind speed",
    "wpgt" : "Peak wind gust",
    "pres" : "Average sea-level air pressure",
    "tsun" : "Sunshine total",
    "coco" : "Weather condition",
}

exec_start = perf_counter()

def mtst_date( # Get date
    min: date = date(1973, 1, 1),
    max: date = date.today(),
):
    with st.sidebar: dt = get_date(
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

col_info, col_map = st.columns(2)

with col_info: loc = get_loc()

if loc is not None:
    lat = loc["lat"]
    long = loc["long"]

    with col_info:
        st.write("Latitude:", lat)
        st.write("Longitude:", long)

    with col_map: geomap(lat, long)

st.sidebar.divider()
    
dict_data_opt = {
    "hourly" : "Hourly",
    "daily" : "Daily",
    "monthly" : "Monthly",
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
        dt = mtst_date()

        param = {
            "loc" : Point(lat, long),
            "start" : dt[0],
            "end" : dt[1]
        }

        if data_opt == "hourly": return Hourly(**param)
        elif data_opt == "daily": return Daily(**param)
        elif data_opt == "monthly": return Monthly(**param)
        elif data_opt == "normals": pass

mtst_data = get_data().fetch()

data_json = mtst_data.to_json(
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)

data_pydict = loads(data_json)

# Reorganize data:
data = {}
timestamp = []
wx_img = []

for i in data_pydict["index"]: timestamp.append(isoparse(i))

for i in data_pydict["columns"]:
    data[i] = []
    col = data_pydict["columns"].index(i)

    for j in data_pydict["data"]:
        if i == "coco" and j[col] is not None:
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

list_temp = ["temp", "tavg", "tmin", "tmax", "dwpt"]

rank = {}

def ranking(i):
    for n in data[i]:
        if n is None: return True

# Process data to dataframe and figures:
df = {}

df["Time"] = Series(timestamp)

for i in data:
    if i not in ["time", "coco"] and data[i]:
        if ranking(i) != True:
            rank[i] = stats(data[i])
            data[i].append(sum(data[i]))

        df[dict_abbr[i]] = Series(data[i])

    elif i == "coco":
        df["Weather condition"] = Series(data["coco"])
        df["IMG"] = Series(wx_img)

    param = go.Scatter(
        name = dict_abbr[i],
        x = timestamp,
        y = data[i],
        mode = "lines+markers+text"
    )

    if i in list_temp: fig_temp.add_trace(param)

    elif i in ["prcp", "snow"]: fig_prcp.add_trace(param)
    elif i == "rhum": fig_prcp.add_trace(param, secondary_y = True)

    elif i in ["wspd", "wpgt"]: fig_wind.add_trace(param)
    elif i == "wdir": fig_wind.add_trace(param, secondary_y = True)

    elif i == "pres": fig_misc.add_trace(param)
    elif i == "tsun": fig_misc.add_trace(param, secondary_y = True)

    elif i == "coco": fig_wxco.add_trace(param)

st.dataframe(
    data = df,
    use_container_width = True,
    column_config = {
        "Time" : st.column_config.DatetimeColumn("Time"),
        "IMG" : st.column_config.ImageColumn("Image")
    }
)

def fig_update(fig, y1: str): # Update figure
    fig.update_layout(
        title = "Chart",
        xaxis_title = "🕰️ Time",
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

            col_medl, col_medh = st.columns(2)

            # Display metrics of statistics:
            col_medl.metric(
                label = "Low median",
                value = rank[data]["medl"]
            )

            col_medh.metric(
                label = "High median",
                value = rank[data]["medh"]
            )

            with st.expander("Frequency"):
                st.caption("Value count: " + str(len(rank[data]["freq"])))

                st.dataframe(
                    data = rank[data]["freq"],
                    use_container_width = True,
                    hide_index = False,
                    column_config = {
                        "_index" : st.column_config.Column(label = "Value"),
                        "value" : st.column_config.Column(label = "Frequency"),
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
                chart(fig_freq)

# Update figures:
fig_update(fig_temp, "°C")

fig_update(fig_prcp, "mm")

fig_update(fig_wind, "km/h")

fig_update(fig_misc, "hPa")
y2(fig_misc, "minutes")

tab_temp, tab_prcp, tab_wind, tab_misc, tab_wxco = st.tabs([
    "🌡️ Temperature",
    "💧 Precipitation",
    "💨 Wind data",
    "☀️ Miscellaneous",
    "⛅ Weather conditions"
])

isWDIR = data_opt == "hourly" or data_opt == "daily"

if data_opt == "hourly": # More updates to figures when current data timescale is hourly
    y2(fig_prcp, "%")
    if isWDIR: y2(fig_wind, "°")

    fig_update(fig_wxco, "Conditions")

    wxco_freq = Counter(data["coco"])

    # Create frequency figure for weather conditions:

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

        with st.expander("Frequency"):
            st.caption("Value count: " + str(len(wxco_freq)))

            st.dataframe(
                data = wxco_freq,
                use_container_width = True,
                hide_index = False,
                column_config = {
                    "_index" : st.column_config.Column(label = "Value"),
                    "value" : st.column_config.Column(label = "Frequency"),
                }
            )

            chart(fig_wxco_freq)

# Display figures:
with tab_temp:
    chart(fig_temp)
    rank_show(list_temp)

with tab_prcp:
    chart(fig_prcp)
    rank_show(["rhum", "prcp", "snow"])

with tab_wind:
    chart(fig_wind)

    if isWDIR and "wdir" in rank:
        l = rank["wdir"]["freq"]
        v = list(l.values())

        fig_wdir = go.Figure(data = go.Barpolar(
            r = v,
            theta = list(l.keys()),
            width = v,
            marker_line_color = "white",
            marker_line_width = 1,
            opacity = 0.5
        ))

        fig_wdir.update_layout(
            title = "Polar chart for wind direction",
            template = "plotly_dark",
            polar = {
                "angularaxis" : {
                    "tickfont_size" : 15,
                    "rotation" : 90,
                    "direction" : "clockwise"
                }
            }
        )

        chart(fig_wdir)

    rank_show(["wdir", "wspd", "wpgt"])

with tab_misc:
    chart(fig_misc)
    rank_show(["pres", "tsun"])

@st.cache_data
def df_dl(df, frmt: str):
    if frmt == "csv": return df.to_csv()
    if frmt == "html": return df.to_html()
    if frmt == "txt": return df.to_string()

with st.sidebar:
    st.divider()
    st.subheader("Download data")

    if st.checkbox(
        label = "Use original data",
        value = True,
        help = 'Use the orginal fetched dataframe instead of the "touched-up" dataframe.'
    ): dl_df = mtst_data
    else: dl_df = DataFrame.from_dict(df)

    dl_frmt = st.selectbox(
        label = "File format",
        options = ["csv", "html", "txt"],
        format_func = lambda x: {
            "csv" : "Comma-separated values",
            #"xlsx" : "Microsoft Excel spreadsheet",
            #"hdf" : "Hierarchical Data Format",
            "html" : "HyperText Markup Language",
            #"json" : "JavaScript Object Notation",
            #"tex" : "LaTeX document",
            #"sql" : "Structured Query Language",
            #"dta" : "Stata datasets",
            "txt" : "Text document",
        }.get(x)
    )

    dl_data = df_dl(dl_df, dl_frmt)

    param = {
        "label" : f"Download .{dl_frmt}",
        "help" : "Click to download file.",
        "data" : dl_data,
        "file_name" : f"wx_data.{dl_frmt}",
    }

    if dl_frmt == "csv": st.download_button(**param, mime = "text/csv")
    elif dl_frmt == "html": st.download_button(**param, mime = "text/html")
    elif dl_frmt == "txt": st.download_button(**param)

buymeacoffee( # A Buymeacoffee button :)
    username = "olamushroom",
    text = "Coffee, please?",
    emoji = "☕",
    font = "Poppins",
    width = 300,
    floating = True
)

st.sidebar.info(body = f"Running time: {round(perf_counter() - exec_start, 10)}s", icon = "⏲️")

# debug:
