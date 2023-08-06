"""Main module"""
from random import seed, uniform
from collections import Counter
from statistics import median_low, median_high

from requests import get
from geocoder import ip # Module for searching location with IP address

import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker as date_range # Date picker but with range selection

import folium
from streamlit_folium import st_folium

'''def ss_chk(param: str, var):
    for i in dict_ss:
        key = dict_ss[i]["key"]
        val = dict_ss[i]["val"]
        if key not in st.session_state: st.session_state[key] = val
        elif key in st.session_state:
            if var != val and var != st.session_state[param]:
                st.session_state[param] = var
                return var
            else: pass'''

def find_coord(): # Get coordinates
    lat = st.sidebar.number_input(
        label = "Latitude",
        min_value = -90.0,
        max_value = 90.0,
        value = 0.0,
        step = 0.001,
        format = "%.3f",
        key = "lat",
        help = "Use negative value for South"
    )
    lat = round(lat, 3)

    long = st.sidebar.number_input(
        label = "Longitude",
        min_value = -180.0,
        max_value = 180.0,
        value = 0.0,
        step = 0.001,
        format = "%.3f",
        key = "long",
        help = "Use negative value for West"
    )
    long = round(long, 3)

    st.sidebar.subheader("RNG")

    if st.sidebar.checkbox(label = "Enable seed"):
        seed(st.sidebar.number_input(
            label = "Seed",
            value = 0,
            help = "Please remember or note down the seed(s) for later use if you want."
        ))

    if st.sidebar.button(
        label = "I'm Feeling Lucky!",
        help = "Get random coordinates."
    ):
        lat = round(uniform(-90, 90), 5)
        long = round(uniform(-180, 180), 5)

        st.toast("Lucky enough yet?", icon = "🎲")

    return {
        "lat" : lat,
        "long" : long
    }

def find_name(): # Location search based on Name/Postal Code using Open-Meteo Geocoding API
    input = st.sidebar.text_input(
        label = "Location name or postal code",
        key = "name",
        help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
    )

    if input != None and input != "":
        loc = get(f"http://geocoding-api.open-meteo.com/v1/search?name={input}&count=1&language=en&format=json").json()["results"][0]

        st.subheader(f'{loc["name"]}, {loc["admin1"]}, {loc["country"]}')

        return {
            "lat" : loc["latitude"],
            "long" : loc["longitude"]
        }

def find_ip(): # IP-based location search using Geocoder
    input = st.sidebar.text_input(
        label = "IP address",
        key = "ip",
        help = ""
    )
            
    if input != None and input != "":
        g = ip(input)

        st.subheader(g.city + ", " + g.state + ", " + g.country)

        return {
            "lat" : g.latlng[0],
            "long" : g.latlng[1]
        }
    
def find_map():
    m = folium.Map(
        location = [0, 0],
        zoom_start = 1
    )
    m.add_child(folium.LatLngPopup())

    with st.sidebar:
        st_data = st_folium(
            fig = m,
            height = 512,
            width = 512
        )

    if st_data["last_clicked"] != None:
        return {
            "lat" : st_data["last_clicked"]["lat"],
            "long" : st_data["last_clicked"]["lng"]
        }

def get_loc(): # Get location-search type
    dict_loc = {
        "coord" : "Coordinates",
        "name" : "Name/Postal code",
        #"ip" : "IP address",
        "map" : "Map",
    }

    in_opt = st.sidebar.radio(
        label = "Location search",
        options = dict_loc.keys(),
        format_func = lambda x: dict_loc.get(x),
        horizontal = True,
        label_visibility = "collapsed",
        key = "in_opt",
        help = ""
    )
    
    if in_opt == "coord": return find_coord()
    elif in_opt == "name": return find_name()
    elif in_opt == "ip": return find_ip()
    elif in_opt == "map": return find_map()

def get_date(start, end, min, max, key: str | None = None): # Get a range of date
    date = date_range(
        title = "Select a range of date",
        default_start = start,
        default_end = end,
        min_date = min,
        max_date = max,
        key = key
    )

    return {
        "start_date" : date[0],
        "end_date" : date[1]
    }

def stats(data): # Return statistics
    return {
        "medl" : round(median_low(data), 10),
        "medh" : round(median_high(data), 10),
        "freq" : Counter(data)
    }

def chart(fig): # Display plotly chart
    return st.plotly_chart(
        figure_or_data = fig,
        use_container_width = True,
        sharing = 'streamlit',
        theme = 'streamlit'
    )

def geomap(lat, long):
    m = folium.Map(
        location = [lat, long],
        zoom_start = 10
    )
    
    fg = folium.FeatureGroup(name = "Markers")
    #for marker in st.session_state["markers"]: fg.add_child(marker)

    return st_folium(
        fig = m,
        height = 342,
        width = 608,
        feature_group_to_add = fg,
        key = "new",
        returned_objects = []
    )
