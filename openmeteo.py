from datetime import datetime, timedelta
import streamlit as st
from streamlit_extras.mandatory_date_range import date_range_picker
from modules import *

st.sidebar.title('WEATHER')

loc = ''

in_opt = st.sidebar.radio(
    label = 'Search type',
    options = ('opt_loc', 'opt_coord'),
    format_func = lambda x: dict_in_opt.get(x),
    horizontal = True,
    key = 'ss_in',
    help = "Choose."
)

if in_opt == 'opt_loc':
    loc_opt = st.sidebar.radio(
        label = 'a',
        options = ('loc_name', 'loc_ip'),
        format_func = lambda x: dict_loc_opt.get(x),
        horizontal = True,
        key = 'ss_loc_opt',
        help = "Choose."
    )

    if loc_opt == 'loc_name':
        in_loc = st.text_input(
            label = 'Location name or postal code',
            key = 'ss_loc_name',
            help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
        )
        if in_loc != '': loc = find_name(in_loc)

    elif loc_opt == 'loc_ip':
        in_loc = st.text_input(
            label = 'IP address',
            key = 'ss_loc_ip',
            help = "Type location's IP address."
        )

        if st.button(
            label = 'Get your IP!',
            help = "Click here to get your current device's IP address."
        ): in_loc = 'me'

        if in_loc != '':
            loc = find_ip(in_loc)
            st.write("The current IP address is:", loc['ip'])

elif in_opt == 'opt_coord':
    lat = 0
    long = 0

    coord_opt = st.sidebar.radio(
        label = 'Choose coordinates notation',
        options = ('dec_deg', 'dms'),
        format_func = lambda x: dict_coord_opt.get(x),
        horizontal = True,
        key = 'ss_coord_opt',
        help = "Choose."
    )

    lat_sign = st.radio(
        label = 'Latitude direction',
        options = ('north', 'south'),
        format_func = lambda x: dict_cardinal_dir.get(x),
        horizontal = True,
        key = 'ss_lat_sign',
        help = 'Choose "South" if the latitude contains minus sign.'
    )

    long_sign = st.radio(
        label = 'Longitude direction',
        options = ('east', 'west'),
        format_func = lambda x: dict_cardinal_dir.get(x),
        horizontal = True,
        key = 'ss_long_sign',
        help = 'Choose "West" if the longitude contains minus sign.'
    )

    if coord_opt == 'dec_deg':
        lat = st.number_input(
            label = 'Latitude',
            min_value = 0.0,
            max_value = 90.0,
            value = 0.0,
            step = 0.0001,
            format = '%.4f',
            key = 'ss_lat',
            help = ""
        )
        long = st.number_input(
            label = 'Longitude',
            min_value = 0.0,
            max_value = 180.0,
            value = 0.0,
            step = 0.0001,
            format = '%.4f',
            key = 'ss_long',
            help = ""
        )

        lat = round(lat, 4)
        long = round(long, 4)

    elif coord_opt == 'dms':
        with st.expander(
            label = "Latitude",
            expanded = True
        ):
            lat_deg = st.slider(
                label = 'Degrees',
                min_value = 0,
                max_value = 90,
                value = 0,
                step = 1,
                format = '%s°',
                key = 'ss_lat_deg',
                help = ""
            )
            lat_min = st.slider(
                label = 'Minutes',
                min_value = 0,
                max_value = 59,
                value = 0,
                step = 1,
                format = "%s'",
                key = 'ss_lat_min',
                help = ""
            )
            lat_sec = st.slider(
                label = 'Seconds',
                min_value = 0,
                max_value = 59,
                value = 0,
                step = 1,
                format = '%s"',
                key = 'ss_lat_sec',
                help = ""
            )

        with st.expander(
            label = "Longitude",
            expanded = True
        ):
            long_deg = st.slider(
                label = 'Degrees',
                min_value = 0,
                max_value = 180,
                value = 0,
                step = 1,
                format = '%s°',
                key = 'ss_long_deg',
                help = ""
            )
            long_min = st.slider(
                label = 'Minutes',
                min_value = 0,
                max_value = 59,
                value = 0,
                step = 1,
                format = "%s'",
                key = 'ss_long_min',
                help = ""
            )
            long_sec = st.slider(
                label = 'Seconds',
                min_value = 0,
                max_value = 59,
                value = 0,
                step = 1,
                format = '%s"',
                key = 'ss_long_sec',
                help = ""
            )

        lat = dec_deg(lat_deg, lat_min, lat_sec)
        long = dec_deg(long_deg, long_min, long_sec)

    if lat_sign == 'north': lat *= 1
    elif lat_sign == 'south': lat *= -1
    if long_sign == 'east': long *= 1
    elif long_sign == 'west': long *= -1

    st.write('Latitude:', lat)
    st.write('Longitude:', long)

st.divider()

with st.sidebar:
    result = date_range_picker(
        title = "Select a date range",
        default_start = datetime.now(),
        default_end = datetime.now(),
        min_date = datetime.now(),
        max_date = datetime.now() + timedelta(days = 16),
        key = "ss_date")

st.write("Result:", result)

wx_opt = st.sidebar.selectbox(
    label = 'Weather type',
    options = ('fcst', 'ens', 'hist', 'clim', 'mar', 'fld', 'aq'),
    format_func = lambda x: dict_wx_opt.get(x),
    key = 'ss_wx_opt',
    help = ""
)

def perf():
    temp_unit = st.sidebar.radio(
        label = 'Temperature Unit',
        options = ('C', 'F'),
        format_func = lambda x: dict_temp_unit.get(x),
        horizontal = True,
        key = 'ss_temp_unit',
        help = ""
    )

    prec_unit = st.sidebar.radio(
        label = 'Precipitation Unit',
        options = ('mm', 'in'),
        format_func = lambda x: dict_prec_unit.get(x),
        horizontal = True,
        key = 'ss_prec_unit',
        help = ""
    )

    ws_unit = st.sidebar.radio(
        label = 'Wind Speed Unit',
        options = ('kmh', 'ms', 'mph', 'kn'),
        format_func = lambda x: dict_ws_unit.get(x),
        horizontal = True,
        key = 'ss_ws_unit',
        help = ""
    )

if any([
    wx_opt == 'fcst',
    wx_opt == 'ens',
    wx_opt == 'hist',
    wx_opt == 'clim'
    ]):
    perf()

st.write(loc) #debug