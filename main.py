"""Main module"""
from collections import Counter
from statistics import fmean, median_low, median_high
from requests import get
from geocoder import ip # Module for searching location with IP address
import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker as date_range # Date picker but with range selection

'''def ss_chk(param: str, var):
    for i in ss:
        key = ss[i]["key"]
        val = ss[i]["val"]
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
        step = 0.0001,
        format = "%.4f",
        key = "lat",
        help = "Use negative value for South"
    )
    lat = round(lat, 4)

    long = st.sidebar.number_input(
        label = "Longitude",
        min_value = -180.0,
        max_value = 180.0,
        value = 0.0,
        step = 0.0001,
        format = "%.4f",
        key = "long",
        help = "Use negative value for West"
    )
    long = round(long, 4)

    return {
        "lat": lat,
        "long": long,
    }

def find_name(): # Location search based on Name/Postal Code using Open-Meteo Geocoding API
    input = st.sidebar.text_input(
        label = "Location name or postal code",
        key = "name",
        help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
    )

    if input != None and input != "":
        loc = get("http://geocoding-api.open-meteo.com/v1/search?name=" + input + "&count=1&language=en&format=json").json()["results"][0] 
        st.subheader(loc["name"] + ", " + loc["admin1"] + ", " + loc["country"])
        return {
            "lat" : loc["latitude"],
            "long" : loc["longitude"]
        }

def find_ip(): # IP-based location search using Geocoder
    input = st.sidebar.text_input(
        label = "IP address",
        key = "ip",
        help = 'If you want to get your current IP address, you can type "me" in the box.'
    )
            
    if input != None and input != "":
        g = ip(input)
        #g.ip
        st.subheader(g.city + ", " + g.state + ", " + g.country)
        return {
            "lat" : g.latlng[0],
            "long" : g.latlng[1]
        }

def get_loc(): # Get location-search type
    dict_loc = {
        "coord" : "Coordinates",
        "name" : "Name/Postal code",
        "ip" : "IP address",
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

def get_date(start, end, min, max, key: str): # Get a range of date
    date = date_range(
        title = "Select a date range",
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
        "mean" : fmean(data),
        "med_l" : median_low(data),
        "med_h" : median_high(data),
        "freq" : Counter(data)
    }

def chart(fig): # Display plotly chart
    return st.plotly_chart(
        figure_or_data = fig,
        use_container_width = True,
        sharing = 'streamlit',
        theme = 'streamlit'
    )
