import streamlit as st
#...and some cool modules idk:

#button that saves its own state:
#from streamlit_extras.stateful_button import button as stex_button

#toggle switch:
from streamlit_toggle import st_toggle_switch as stex_switch

#date picker but with a range selection:
from streamlit_extras.mandatory_date_range import date_range_picker as stex_dt_range

from datetime import date
from dateutil.relativedelta import relativedelta as rltvDelta
from modules import *

st.title('WEATHER')

#default parameter:
#'&timeformat=unixtime&timezone=auto'

param, loc = '', ''
lat, long = 0, 0

def get_date(start, end, min, max, key):
    return stex_dt_range(
        title = "Select a date range",
        default_start = start,
        default_end = end,
        min_date = min,
        max_date = max,
        key = key
    )

with st.sidebar:
    in_opt = st.radio(
        label = 'Search type',
        options = ('coord', 'name', 'ip'),
        format_func = lambda x: dict_loc.get(x),
        horizontal = True,
        label_visibility = 'collapsed',
        key = 'ss_in',
        help = ""
    )

    if in_opt == 'coord':
        lat = st.number_input(
            label = 'Latitude',
            min_value = -90.0,
            max_value = 90.0,
            value = 0.0,
            step = 0.0001,
            format = '%.4f',
            key = 'ss_lat',
            help = "Use negative value for South"
        )

        long = st.number_input(
            label = 'Longitude',
            min_value = -180.0,
            max_value = 180.0,
            value = 0.0,
            step = 0.0001,
            format = '%.4f',
            key = 'ss_long',
            help = "Use negative value for West"
        )

    elif in_opt == 'name':
        in_loc = st.text_input(
            label = 'Location name or postal code:',
            key = 'ss_name',
            help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
        )

        if in_loc != '':
            loc = find_name(in_loc)
            lat = loc['latitude']
            long = loc['longitude']

    elif in_opt == 'ip':
        in_loc = st.text_input(
            label = 'IP address:',
            key = 'ss_ip',
            help = "Type location's IP address."
        )

        if st.button(
            label = 'Get your IP!',
            #key = 'ss_ip_get',
            help = "Click here to get your current device's IP address."
        ): in_loc = 'me'

        if in_loc != '':
            loc = find_ip(in_loc)
            lat = loc['lat']
            long = loc['long']
            st.write("The current IP address is:", loc['ip'])

lat = round(lat, 4)
long = round(long, 4)
#if lat == -0.0: lat = 0.0
#if long == -0.0: long = 0.0

coord = 'latitude=' + str(lat) + '&longitude=' + str(long)
param += coord

wx_opt = st.selectbox(
    label = 'Weather type',
    options = (None, 'fcst', 'ens', 'hist', 'clim', 'aq', 'mar', 'fld'),
    format_func = lambda x: dict_wx.get(x),
    key = 'ss_wx_opt',
    help = ""
)

def pref():
    with st.expander(
        label = 'Preferences',
        expanded = True
    ):
        temp_unit = st.radio(
            label = 'Temperature Unit',
            options = ('C', 'F'),
            format_func = lambda x: dict_unit.get(x),
            horizontal = True,
            key = 'ss_temp_unit',
            help = ""
        )

        prec_unit = st.radio(
            label = 'Precipitation Unit',
            options = ('mm', 'in'),
            format_func = lambda x: dict_unit.get(x),
            horizontal = True,
            key = 'ss_prec_unit',
            help = ""
        )

        ws_unit = st.radio(
            label = 'Wind Speed Unit',
            options = ('kmh', 'ms', 'mph', 'kn'),
            format_func = lambda x: dict_unit.get(x),
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
    param += '&timezone=auto'
    pref()

if wx_opt == 'mar':
    len_unit = st.radio(
        label = 'Length Unit',
        options = ('m', 'imp'),
        format_func = lambda x: dict_unit.get(x),
        horizontal = True,
        key = 'ss_len_unit',
        help = ""
    )

if wx_opt == 'fld':    
    dly = '&daily='
    dly_opt = st.multiselect(
        label = 'Daily Weather Variables',
        options = ['dc', 'mn', 'med', 'max', 'min', 'p25', 'p75'],
        default = None,
        format_func = lambda x: dict_fld[x][1],
        disabled = False,
        key = None,
        help = ""
    )
    for opt in dly_opt: dly += dict_fld[opt][0]
    param += dly
    
    mdl = '&models='
    fld_mdl = stex_switch(
        label = "Enable Flood models",
        default_value = False,
        label_after = True,
        inactive_color = "#fafafa",
        active_color = "#fafafa",
        track_color = "#00c0f2",
        key = "ss_fld_mdl"
    )

    mdl_consol = False #placeholder variable to prevent unbound because i am stupid

    if fld_mdl == True:
        mdl_opt = st.multiselect(
            label = 'Daily Weather Variables',
            options = ['v3_smls', 'v3_fcst', 'v3_consol', 'v4_consol'],
            default = None,
            format_func = lambda x: dict_fld[x][1],
            disabled = False,
            key = None,
            help = ""
        )
        for opt in mdl_opt: mdl += dict_fld[opt][0]
        param += mdl

        if all([
            not not mdl_opt, #lmao not not
            'v3_smls' not in mdl_opt,
            'v3_fcst' not in mdl_opt, 
        ]): mdl_consol = True
    elif fld_mdl == False: param.replace(mdl, '')

    ens =  stex_switch(
        label = "Enable All 50 Ensemble Members",
        default_value = False,
        label_after = True,
        inactive_color = "#fafafa",
        active_color = "#fafafa",
        track_color = "#00c0f2",
        key = "ss_fld_ens"
    )
    if ens == True: param += dict_fld['ens']
    elif ens == False: param.replace(dict_fld['ens'], '')

    dt_max = date.today() + rltvDelta(months = +7, weeks= +2)
    dt_start, dt_end = date.today(), date.today()
    if mdl_consol == True:
        dt_max = date(2022, 7, 31)
        dt_start, dt_end = date(2022, 7, 31), date(2022, 7, 31)
    dt = get_date(
        start = dt_start,
        end = dt_end,
        min = date(1984, 1, 1),
        max = dt_max,
        key = 'ss_dt_fld'
    )
    
    param += ('&start_date=' + dt[0].strftime('%Y-%m-%d') + '&end_date=' + dt[1].strftime('%Y-%m-%d'))
    st.write("Date:", dt) #debug
    
#debug:
st.sidebar.write("WX type:", wx_opt)
st.sidebar.write('Parameters:', param)
st.sidebar.write('Location:', loc)
