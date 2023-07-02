"""IMPORTANT: Prefix with an underscore anything that the user shouldn"t see."""

# Import modules:
from modules.openmeteo import *
from modules.main import get_loc, get_date
from datetime import date
from dateutil.relativedelta import relativedelta as rltvD

import plotly.graph_objects as go
import streamlit as st
# ... and some cool modules idk:
from streamlit_extras.stateful_button import button as stex_button # Button that saves its own state
from streamlit_extras.toggle_switch import st_toggle_switch as stex_switch # Toggle switch


#-----------------------------------------------------------------------------------------------------------------------------------------------------

st.title("WEATHER")

#timef = "&timeformat=unixtime"

param = ""

def date_frmt(date): return "&start_date=" + date[0].strftime("%Y-%m-%d") + "&end_date=" + date[1].strftime("%Y-%m-%d") # Format datetime object into date parameter string
    
def get_unit(name: str, unit: str, key, help: str):
    expd = st.expander(
        label = "Unit Preferences",
        expanded = True
    )
    return expd.radio(
        label = name,
        options = dict_unit[unit],
        format_func = lambda x: dict_unit[unit][x],
        horizontal = True,
        key = key,
        help = help
    )

get_loc() # Get location

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

if wx_opt == "mar" : # WX type: Marine
    get_unit(
        name = "Length Unit",
        unit = "len",
        key = "ss_unit_len",
        help = ""
    )

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

    with st.sidebar:
        dt = get_date(
            start = date.today(),
            end = date.today(),
            min = date(1984, 1, 1),
            max = date.today() + rltvD(months = +7),
            key = "ss_dt_fld"
        )
    dt = date_frmt(dt)
    param += dt

    json_obj = flood(param)

    st.write("Latitude:", json_obj["latitude"], "°")
    st.write("Longitude:", json_obj["longitude"], "°")
    st.write("Generation time:", json_obj["generationtime_ms"], "ms")

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

    st.sidebar.write("Dataframe:", df) # debug

# debug:
with st.sidebar:
    st.divider()
    st.subheader("DEBUG")
    st.write("Parameters:", param)
    st.write("Session State:", st.session_state)
