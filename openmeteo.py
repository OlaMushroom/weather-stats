import streamlit as st
#...and some cool modules idk:

#add blank lines (verticle spaces) to the code instead of spamming st.write():
#from streamlit_extras.add_vertical_space import add_vertical_space as stex_vert_sp

#cooler header:
#from streamlit_extras.colored_header import colored_header as stex_header

#button that saves its own state:
#from streamlit_extras.stateful_button import button as stex_button

#toggle switch:
from streamlit_toggle import st_toggle_switch as stex_switch

#date picker but with a range selection:
from streamlit_extras.mandatory_date_range import date_range_picker as stex_dt_range

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from modules import *

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
    st.title('WEATHER')
    
    '''
    stex_header(
        label = '',
        description = '',
        color_name = 'blue-green-70'
    )
    '''
    
    in_opt = st.radio(
        label = 'Search type',
        options = ('loc', 'coord'),
        format_func = lambda x: dict_loc_opt.get(x),
        horizontal = True,
        label_visibility = 'collapsed',
        key = 'ss_in',
        help = ""
    )

    if in_opt == 'loc':
        loc_opt = st.radio(
            label = 'Location type',
            options = ('name', 'ip'),
            format_func = lambda x: dict_loc_opt.get(x),
            horizontal = True,
            label_visibility = 'collapsed',
            key = 'ss_loc_opt',
            help = ""
        )

        if loc_opt == 'name':
            in_loc = st.text_input(
                label = 'Location name or postal code',
                key = 'ss_loc_name',
                help = "Only 1 character will return empty result, 2 characters will only match exact matching locations, 3 and more characters will perform fuzzy matching."
            )

            if in_loc != '':
                loc = find_name(in_loc)
                lat = loc['latitude']
                long = loc['longitude']            

        elif loc_opt == 'ip':
            col_ip_txtin, col_ip_button = st.columns(
                spec = [0.69, 0.30],
                gap = 'small'
            )

            with col_ip_txtin:
                in_loc = st.text_input(
                    label = 'IP address',
                    key = 'ss_loc_ip',
                    help = "Type location's IP address."
                )
            
            with col_ip_button:
                st.write('')
                st.write('')
                if st.button(
                    label = 'Get your IP!',
                    key = 'ss_ip_get',
                    help = "Click here to get your current device's IP address."
                ): in_loc = 'me'

            if in_loc != '':
                loc = find_ip(in_loc)
                lat = loc['lat']
                long = loc['long']
                st.write("The current IP address is:", loc['ip'])

    elif in_opt == 'coord':
        coord_opt = st.radio(
            label = 'Choose coordinates notation',
            options = ('dd', 'dms'),
            format_func = lambda x: dict_loc_opt.get(x),
            horizontal = True,
            key = 'ss_coord_opt',
            help = ""
        )

        col_lat_sign, col_long_sign = st.columns(
            spec = 2,
            gap = 'small'
        )
        
        with col_lat_sign:
            lat_sign = st.radio(
                label = 'Latitude direction',
                options = ('N', 'S'),
                format_func = lambda x: dict_loc_opt.get(x),
                horizontal = True,
                key = 'ss_lat_sign',
                help = 'Choose "South" if the latitude contains minus sign.'
            )
        
        with col_long_sign:
            long_sign = st.radio(
                label = 'Longitude direction',
                options = ('E', 'W'),
                format_func = lambda x: dict_loc_opt.get(x),
                horizontal = True,
                key = 'ss_long_sign',
                help = 'Choose "West" if the longitude contains minus sign.'
            )

        if coord_opt == 'dd':
            col_lat, col_long = st.columns(
                spec = 2,
                gap = 'small'
            )

            with col_lat:
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

            with col_long:
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
                    max_value = 89,
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
                    max_value = 179,
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

            lat = dd(lat_deg, lat_min, lat_sec)
            long = dd(long_deg, long_min, long_sec)

        if lat_sign == 'north': lat *= 1
        elif lat_sign == 'south': lat *= -1
        if long_sign == 'east': long *= 1
        elif long_sign == 'west': long *= -1

coord = 'latitude=' + str(lat) + '&longitude=' + str(long)
param += coord

wx_opt = st.selectbox(
    label = 'Weather type',
    options = (None, 'fcst', 'ens', 'hist', 'clim', 'aq', 'mar', 'fld'),
    format_func = lambda x: dict_wx.get(x),
    key = 'ss_wx_opt',
    help = ""
)

st.write("Result:", wx_opt)

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

    v4_consol = False #placeholder variable to prevent unbound because i am stupid

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
        if 'v4_consol' in mdl_opt: v4_consol = True
        for opt in mdl_opt: mdl += dict_fld[opt][0]
        param += mdl
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

    dt_max = date.today() + relativedelta(months = +7, weeks= +2)
    dt_start, dt_end = date.today(), date.today()
    if v4_consol == True:
        dt_max = date(2022, 6, 30)
        dt_start, dt_end = date(2022, 6, 30), date(2022, 6, 30)
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
st.write('Parameters:', param)
st.write(loc)
