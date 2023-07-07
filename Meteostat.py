"""Meteostat weather data"""
# Import modules:
from meteostat import Point, Hourly, Daily, Monthly
from main import get_loc, get_date, stats, chart
from collections import Counter
from json import loads
from datetime import date, datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
from pandas import Series
from plotly.subplots import make_subplots as subplot
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
icon = Image.open("./static/icon.png")

st.set_page_config(
    page_title = "Meteostat",
    page_icon = icon,
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        "Get Help" : "https://github.com/OlaMushroom/weather-stats/wiki",
        "Report a bug" : "https://github.com/OlaMushroom/weather-stats/issues",
        "About" : "https://meteostat.net"
    }
)

wx_code = { # Weather condition codes
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

lat, long = 0, 0

with st.sidebar:
    loc = get_loc()
    if loc != None:
        lat = loc["lat"]
        long = loc["long"]

        st.write("Latitude:", lat)
        st.write("Longitude:", long)

with st.form("form"): # Create a form
    with st.sidebar:      
        data_opt = st.sidebar.radio(
            label = "Data timescale",
            options = ("hourly", "daily", "monthly"),
            format_func = lambda x: x.capitalize(),
            horizontal = True,
            key = "data_opt",
            help = ""
        )

        def get_data(): # Get data
            if data_opt == "hourly":
                dt = mtst_date(date.today())
                return Hourly(
                    loc = Point(lat, long),
                    start = dt[0],
                    end = dt[1]
                ).fetch()

            elif data_opt == "daily":
                dt = mtst_date(date.today())
                return Daily(
                    loc = Point(lat, long),
                    start = dt[0],
                    end = dt[1]
                ).fetch()

            elif data_opt == "monthly":
                dt = mtst_date(date(2023, 4, 1))
                return Monthly(
                    loc = Point(lat, long),
                    start = dt[0],
                    end = dt[1]
                ).fetch()
            
        data_raw = get_data() # Store data

        submit = st.form_submit_button("Get data!") # Create a submit button

    if submit:
        prog_bar = st.sidebar.progress(0, text = "Starting...0%")

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
        for i in data_json["index"]: timestamp.append(isoparse(i))

        for i in data_json["columns"]:
            data[i] = []
            c = data_json["columns"].index(i)
            for j in data_json["data"]:
                if i == "coco": j[c] = wx_code[str(int(j[c]))]
                data[i].append(j[c])

        prog_bar.progress(25, text = "Processing...25%")

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

        st.dataframe(data = df, use_container_width = True) # Display dataframe

        prog_bar.progress(50, text = "Updating...50%")

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
            if data_opt == "daily": y2(fig_wind, "°")
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
            
        prog_bar.progress(75, text = "Finalizing...75%")

        # Display figures:
        with tab_temp:
            chart(fig_temp)
            rank_show(list_temp)

        with tab_prcp:
            chart(fig_prcp)
            rank_show(list_prcp)

        with tab_wind:
            chart(fig_wind)
            rank_show(list_wind)

        with tab_misc:
            chart(fig_misc)
            rank_show(list_misc)

        prog_bar.progress(100, text = "Done! 100%")

# debug:
#st.write(st.session_state)
#st.write(rank)
#st.write(data)
