"""Main module"""
from collections import Counter
from statistics import fmean, median_low, median_high
from requests import get
from geocoder import ip # Module for searching location with IP address
from streamlit import write, subheader, text_input, number_input, radio, plotly_chart, sidebar, columns, session_state
from streamlit_extras.mandatory_date_range import date_range_picker as date_range # Date picker but with range selection

ss = {
    "input" : {
        "key": "in",
        "val": "",
    },

    "latitude" : {
        "key" : "lat",
        "val" : None,
    },

    "longitude" : {
        "key" : "long",
        "val" : None,
    },

    "location" : {
        "key" : "loc",
        "val" : "",
    },

    "IP" : {
        "key" : "ip",
        "val" : "",
    },
}

# Session state:
def ss_chk(param: str, var):
    for i in ss:
        key = ss[i]["key"]
        val = ss[i]["val"]
        if key not in session_state: session_state[key] = val
        elif key in session_state:
            if var != val and var != session_state[param]:
                session_state[param] = var
                return var
            else: pass

def find_name(loc): return get("https://geocoding-api.open-meteo.com/v1/search?name=" + loc + "&count=1&language=en&format=json").json()["results"][0] # Location search based on Name/Postal Code

# IP-based location search using Geocoder:
def find_ip(loc):
    g = ip(loc)
    return {
        "ip": g.ip,
        "lat": g.latlng[0],
        "long": g.latlng[1],
        "city": g.city,
        "state": g.state,
        "country": g.country,
    }

# Location input types:
dict_loc = {
    None : "None",
    "coord" : "Coordinates",
    "name" : "Name/Postal code",
    "ip" : "IP address",
}

# Get location:
def get_loc():
    loc = ""
    lat, long = 0, 0

    with sidebar:
        in_opt = radio(
            label = "Search type",
            options = dict_loc.keys(),
            format_func = lambda x: dict_loc.get(x),
            horizontal = True,
            label_visibility = "collapsed",
            help = ""
        )
        ss_chk("in", in_opt)

        if session_state["in"] == "coord": # Coordinates
            col_lat, col_long = columns(
                spec = 2,
                gap = "small"
            )

            with col_lat:
                lat = number_input(
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
                long = number_input(
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

        elif session_state["in"] == "name": # Name/Postal Code
            in_loc = text_input(
                label = "Location name or postal code:",
                key = "ss_name",
                help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
            )
            ss_chk("loc", in_loc)

            if session_state["loc"] != "":
                loc = find_name(in_loc)
                subheader(loc["name"] + ", " + loc["admin1"] + ", " + loc["country"])

                lat = loc["latitude"]
                ss_chk("lat", lat)

                long = loc["longitude"]
                ss_chk("long", long)
                

        elif session_state["in"] == "ip": # IP address
            in_loc = text_input(
                label = "IP address:",
                key = "ss_ip",
                help = 'If you want to get your current IP address, you can type "me" in the box.'
            )
            ss_chk("ip", in_loc)
            
            if session_state["ip"] != "":
                loc = find_ip(in_loc)
                subheader(loc["city"] + ", " + loc["state"] + ", " + loc["country"])

                lat = loc["lat"]
                ss_chk("lat", lat)

                long = loc["long"]
                ss_chk("long", long)
                
        write("Latitude:", lat, ",", "Longitude:", long)
        #write("Location:", loc) # debug

    return {
        0 : session_state["lat"],
        1 : session_state["long"],
    }

# Get date:
def get_date(start, end, min, max, key: str):
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

# Return statistics:
def stats(data):
    return {
        "mean" : fmean(data),
        "med_l" : median_low(data),
        "med_h" : median_high(data),
        "freq" : Counter(data)
    }

# Display plotly chart:
def chart(fig):
    return plotly_chart(
        figure_or_data = fig,
        use_container_width = True,
        sharing = 'streamlit',
        theme = 'streamlit'
    )
