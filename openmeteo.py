"""IMPORTANT: Prefix with an underscore anything that the user shouldn"t see."""

# Import modules:
from modules import *
from datetime import date
from dateutil.relativedelta import relativedelta as rltvD
#import numpy as np
#import pandas as pd
#import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
# ... and some cool modules idk:
from streamlit_extras.stateful_button import button as stex_button # Button that saves its own state
from streamlit_extras.toggle_switch import st_toggle_switch as stex_switch # Toggle switch
from streamlit_extras.mandatory_date_range import date_range_picker as stex_dt_range # Date picker but with range selection

#-----------------------------------------------------------------------------------------------------------------------------------------------------

st.title("WEATHER")

#st.session_state[""] # The magic line of code, just need to copy paste
#timef = "&timeformat=unixtime"

param, loc = "", ""
lat, long = 0, 0

# Session state (fk this sht):
def ss_chk(param: str, var):
    for i in ss:
        key = ss[i]["key"]
        val = ss[i]["val"]
        if key not in st.session_state: st.session_state[key] = val
        elif key in st.session_state:
            if var != val and var != st.session_state[param]:
                st.session_state[param] = var
                return var
            else: pass

# Date range input:
def get_date(start, end, min, max, key):
    with st.sidebar:
        date = stex_dt_range(
            title = "Select a date range",
            default_start = start,
            default_end = end,
            min_date = min,
            max_date = max,
            key = key
        )
        return "&start_date=" + date[0].strftime("%Y-%m-%d") + "&end_date=" + date[1].strftime("%Y-%m-%d")
    
def get_unit(name, unit):
    expd = st.expander(
        label = "Unit Preferences",
        expanded = True
    )
    return expd.radio(
        label = name,
        options = dict_unit[unit],
        format_func = lambda x: dict_unit[unit][x][1],
        horizontal = True,
        key = "ss_unit",
        help = ""
    )

#-----------------------------------------------------------------------------------------------------------------------------------------------------

# Location input:
with st.sidebar:
    in_opt = st.radio(
        label = "Search type",
        options = dict_loc.keys(),
        format_func = lambda x: dict_loc.get(x),
        horizontal = True,
        label_visibility = "collapsed",
        help = ""
    )
    ss_chk("in", in_opt)

    if st.session_state["in"] == "coord": # Coordinates
        col_lat, col_long = st.columns(
            spec = 2,
            gap = "small"
        )

        with col_lat:
            lat = st.number_input(
                label = "Latitude",
                min_value = -90.0,
                max_value = 90.0,
                value = 0.0,
                step = 0.0001,
                format = "%.4f",
                key = "ss_lat",
                help = "Use negative value for South"
            )
            lat = round(lat, 4)
            ss_chk("lat", lat)

        with col_long:
            long = st.number_input(
                label = "Longitude",
                min_value = -180.0,
                max_value = 180.0,
                value = 0.0,
                step = 0.0001,
                format = "%.4f",
                key = "ss_long",
                help = "Use negative value for West"
            )
        long = round(long, 4)
        ss_chk("long", long)

    elif st.session_state["in"] == "name": # Name/Postal Code
        in_loc = st.text_input(
            label = "Location name or postal code:",
            key = "ss_name",
            help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
        )
        ss_chk("loc", in_loc)

        if st.session_state["loc"] != "":
            loc = find_name(in_loc)
            lat = loc["latitude"]
            ss_chk("lat", lat)
            long = loc["longitude"]
            ss_chk("long", long)

    elif st.session_state["in"] == "ip": # IP address
        in_loc = st.text_input(
            label = "IP address:",
            key = "ss_ip",
            help = 'If you want to get your current IP address, you can type "me" in the box.'
        )
        ss_chk("ip", in_loc)
        
        if st.session_state["ip"] != "":
            loc = find_ip(in_loc)
            lat = loc["lat"]
            ss_chk("lat", lat)
            long = loc["long"]
            ss_chk("long", long)
            st.write("The current IP address is:", loc["ip"])

coord = "latitude=" + str(st.session_state["lat"]) + "&longitude=" + str(st.session_state["long"])
param += coord

#-----------------------------------------------------------------------------------------------------------------------------------------------------

# Weather type selection:
wx_opt = st.selectbox(
    label = "Weather type",
    options = dict_wx.keys(),
    format_func = lambda x: dict_wx.get(x),
    key = "ss_wx_opt",
    help = ""
)

if any([
    wx_opt == "fcst",
    wx_opt == "ens",
    wx_opt == "hist",
    wx_opt == "clim"
]):
    param += "&timezone=auto"

if wx_opt == "fld": # WX type: Flood
    dly = "&daily="
    dly_opt = st.multiselect(
        label = "Daily Weather Variables",
        options = dict_fld.keys(),
        default = None,
        format_func = lambda x: dict_fld[x],
        key = None,
        help = "Uses GloFAS version 3 with Seamless data (which combines Forecast & Consolidated historical data). For Version 4, no data is available yet."
    )
    for opt in dly_opt: dly += opt + ","
    param += dly
            
    if stex_switch(
        label = "Enable All 50 Ensemble Members",
        default_value = False,
        label_after = True,
        inactive_color = "#fafafa",
        active_color = "#fafafa",
        track_color = "#00c0f2",
        key = "ss_fld_ens"
    ): param += "&ensemble=true"
    else: param.replace("&ensemble=true", "")

    dt = get_date(
        start = date.today(),
        end = date.today(),
        min = date(1984, 1, 1),
        max = date.today() + rltvD(months = +7),
        key = "ss_dt_fld"
    ) 
    param += dt
    st.sidebar.write("Date:", dt) # debug

    json_obj = flood(param)
    data = json_obj["daily"]
    unit = json_obj["daily_units"]
    df = {}
    fig = go.Figure()

    for v in data:
        if v == "time": df["Time (YYYY-MM-DD)"] = data[v]

        elif v in dict_fld:
            df["%s (%s)" % (dict_fld[v], unit[v])] = data[v]
            fig.add_trace(go.Scatter(
                x = data["time"],
                y = data[v],
                name = dict_fld[v],
                mode = "lines+markers"
            ))

        else:
            s = v.replace(v[-2:], "")
            s += " " + v[-2:]
            s = s.replace("_", " ")
            s = s.title()
            df["%s (%s)" % (s, unit[v])] = data[v]
            fig.add_trace(go.Scatter(
                x = data["time"],
                y = data[v],
                name = s,
                mode = "lines+markers"
            ))

    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="m³/s"
    )

    with st.expander(
        label = "Table",
        expanded = False
    ):
        st.dataframe(
            data = df,
            use_container_width = True,
            hide_index = True
        )

    with st.expander(
        label = "Chart",
        expanded = True
    ):
        st.plotly_chart(
            figure_or_data = fig,
            use_container_width = True,
            theme = "streamlit",
            sharing = "streamlit"
        )

    st.sidebar.write("Dataframe", df) # debug
    
# debug:
with st.sidebar:
    st.divider()
    st.subheader("DEBUG")
    st.write("Parameters:", param)
    st.write("Location:", loc)
    st.write("Session State:", st.session_state)
