"""IMPORTANT: Prefix with an underscore anything that the user shouldn't see."""

# Import modules:
from modules import *
from datetime import date
from dateutil.relativedelta import relativedelta as rltvDelta
import pandas as pd
import streamlit as st
# ... and some cool modules idk:
from streamlit_extras.stateful_button import button as stex_button # Button that saves its own state
from streamlit_extras.toggle_switch import st_toggle_switch as stex_switch # Toggle switch
from streamlit_extras.mandatory_date_range import date_range_picker as stex_dt_range # Date picker but with range selection

st.title('WEATHER')

#st.session_state[''] # The magic line of code, just need to copy paste
#'&timeformat=unixtime&timezone=auto' # Temp default parameter

param, loc = '', ''
lat, long = 0, 0

# Session state (fk this sht):
def ss_chk(param: str, var):
    for i in ss:
        key = ss[i]['key']
        val = ss[i]['val']
        if key not in st.session_state: st.session_state[key] = val
        elif key in st.session_state:
            if var != val and var != st.session_state[param]:
                st.session_state[param] = var
                return var
            else: pass

def lat_chk(lat):
    lat = round(lat, 4)
    ss_chk('lat', lat)
def long_chk(long):
    long = round(long, 4)
    ss_chk('long', long)

# Date range input:
def get_date(start, end, min, max, key):
    return stex_dt_range(
        title = "Select a date range",
        default_start = start,
        default_end = end,
        min_date = min,
        max_date = max,
        key = key
    )

# Location input:
#with st.sidebar:
in_opt = st.radio(
    label = 'Search type',
    options = ('coord', 'name', 'ip'),
    format_func = lambda x: dict_loc.get(x),
    horizontal = True,
    label_visibility = 'collapsed',
    help = ""
)
ss_chk('in', in_opt)

if st.session_state['in'] == 'coord': # Coordinates
    lat = st.number_input(
        label = 'Latitude',
        min_value = -90.0,
        max_value = 90.0,
        value = 0.0,
        step = 0.0001,
        format = '%.4f',
        help = "Use negative value for South"
    )
    lat_chk(lat)

    long = st.number_input(
        label = 'Longitude',
        min_value = -180.0,
        max_value = 180.0,
        value = 0.0,
        step = 0.0001,
        format = '%.4f',
        help = "Use negative value for West"
    )
    long_chk(long)

elif st.session_state['in'] == 'name': # Name/Postal Code
    in_loc = st.text_input(
        label = 'Location name or postal code:',
        help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
    )
    ss_chk('loc', in_loc)

    if st.session_state['loc'] != '':
        loc = find_name(in_loc)
        lat = loc['latitude']
        lat_chk(lat)
        long = loc['longitude']
        long_chk(long)

elif st.session_state['in'] == 'ip': # IP address
    in_loc = st.text_input(
        label = 'IP address:',
        help = 'If you want to get your current IP address, you can type "me" in the box.'
    )
    ss_chk('ip', in_loc)
    
    if st.session_state['ip'] != '':
        loc = find_ip(in_loc)
        lat = loc['lat']
        lat_chk(lat)
        long = loc['long']
        long_chk(long)
        st.write("The current IP address is:", loc['ip'])

coord = 'latitude=' + str(st.session_state['lat']) + '&longitude=' + str(st.session_state['long'])
param += coord

# Weather type selection:
wx_opt = st.selectbox(
    label = 'Weather type',
    options = (None, 'fcst', 'ens', 'hist', 'clim', 'aq', 'mar', 'fld'),
    format_func = lambda x: dict_wx.get(x),
    key = 'ss_wx_opt',
    help = ""
)

if wx_opt == 'mar': # WX type: Marine
    len_unit = st.radio(
        label = 'Length Unit',
        options = ('m', 'imp'),
        format_func = lambda x: dict_unit.get(x),
        horizontal = True,
        key = 'ss_len_unit',
        help = ""
    )

if wx_opt == 'fld': # WX type: Flood
    index, list = [], []
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
    for opt in dly_opt:
        index.append(dict_fld[opt][1])
        list.append(dict_fld[opt][0])
        dly += dict_fld[opt][0] + ','
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

    mdl_consol = False # placeholder variable to prevent unbound because i am stupid

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
        param += mdl + ','

        if all([
            not not mdl_opt, # lmao not not
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
    st.write("Date:", dt) # debug

    if st.button(
        label = 'Get weather data',
        key = 'ss_fld_data',
        help = ""
    ):
        data = flood(param)['daily']
        frame = []
        for i in data['time']: frame = pd.DataFrame({'Time': data['time']})
        for opt in dly_opt: frame[dict_fld[opt][1]] = pd.Series(data[dict_fld[opt][0]])
        st.write(frame)
        st.sidebar.write(data)
    
# debug:
st.sidebar.write('Parameters:', param)
st.sidebar.write('Location:', loc)
st.sidebar.write(st.session_state)

#-----------------TEMP CHUNK OF CODE-----------------:
'''

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

'''
