import streamlit as st
#...and some cool modules idk:

#add blank lines (verticle spaces) to the code instead of spamming st.write() (uhh idk):
#from streamlit_extras.add_vertical_space import add_vertical_space as stex_vert_sp

#cooler header:
#from streamlit_extras.colored_header import colored_header as stex_header

#button that saves its own state:
#from streamlit_extras.stateful_button import button as stex_button

#toggle switch
from streamlit_toggle import st_toggle_switch as stex_switch

#st.selectbox() but with "None" as default selection:
#from streamlit_extras.no_default_selectbox import selectbox as stex_selbx

#date picker but with a range selection:
from streamlit_extras.mandatory_date_range import date_range_picker as stex_dt_range

from datetime import date, datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
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
                format_func = lambda x: dict_cd_dir.get(x),
                horizontal = True,
                key = 'ss_lat_sign',
                help = 'Choose "South" if the latitude contains minus sign.'
            )
        
        with col_long_sign:
            long_sign = st.radio(
                label = 'Longitude direction',
                options = ('E', 'W'),
                format_func = lambda x: dict_cd_dir.get(x),
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

    dc =  st.checkbox(
        label = 'River Discharge',
        value = False,
        disabled = False,
        key = 'ss_fld_dc',
        help = ""
    )
    if dc == True: dly += dict_fld['dc']
    elif dc == False: dly.replace(dict_fld['dc'], '')

    dc_mn = st.checkbox(
        label = 'River Discharge Mean',
        value = False,
        disabled = False,
        key = 'ss_fld_dc_mn',
        help = ""
    )
    if dc_mn == True: dly += dict_fld['mn']
    elif dc_mn == False: dly.replace(dict_fld['mn'], '')

    dc_med = st.checkbox(
        label = 'River Discharge Median',
        value = False,
        disabled = False,
        key = 'ss_fld_dc_med',
        help = ""
    )
    if dc_med == True: dly += dict_fld['med']
    elif dc_med == False: dly.replace(dict_fld['med'], '')

    dc_max = st.checkbox(
        label = 'River Discharge Max',
        value = False,
        disabled = False,
        key = 'ss_fld_dc_max',
        help = ""
    )
    if dc_max == True: dly += dict_fld['max']
    elif dc_max == False: dly.replace(dict_fld['max'], '')

    dc_min = st.checkbox(
        label = 'River Discharge Min',
        value = False,
        disabled = False,
        key = 'ss_fld_dc_min',
        help = ""
    )
    if dc_min == True: dly += dict_fld['min']
    elif dc_min == False: dly.replace(dict_fld['min'], '')

    dc_p25 = st.checkbox(
        label = 'River Discharge 25ᵗʰ Percentile',
        value = False,
        disabled = False,
        key = 'ss_fld_dc_p25',
        help = ""
    )
    if dc_p25 == True: dly += dict_fld['p25']
    elif dc_p25 == False: dly.replace(dict_fld['p25'], '')

    dc_p75 = st.checkbox(
        label = 'River Discharge 75ᵗʰ Percentile',
        value = False,
        disabled = False,
        key = 'ss_fld_dc_p75',
        help = ""
    )
    if dc_p75 == True: dly += dict_fld['p75']
    elif dc_p75 == False: dly.replace(dict_fld['p75'], '')

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

    v4_consol = False #placeholder variable because i'm stupid

    if fld_mdl == True:
        with st.expander(
            label = "Flood models",
            expanded = False
        ):
            v3_smls = st.checkbox(
            label = 'GloFAS v3 Seamless',
            value = False,
            disabled = False,
            key = 'ss_v3_smls',
            help = "Combines both Forecast and Consolidated historical data."
            )
            if v3_smls == True: mdl += dict_fld['v3_smls']
            elif v3_smls == False: mdl.replace(dict_fld['v3_smls'], '')

            v3_fcst = st.checkbox(
            label = 'GloFAS v3 Forecast',
            value = False,
            disabled = False,
            key = 'ss_v3_fcst',
            help = ""
            )
            if v3_fcst == True: mdl += dict_fld['v3_fcst']
            elif v3_fcst == False: mdl.replace(dict_fld['v3_fcst'], '')

            v3_consol = st.checkbox(
            label = 'GloFAS v3 Consolidated',
            value = False,
            disabled = False,
            key = 'ss_v3_consol',
            help = ""
            )
            if v3_consol == True: mdl += dict_fld['v3_consol']
            elif v3_consol == False: mdl.replace(dict_fld['v3_consol'], '')

            v4_smls = st.checkbox(
            label = 'GloFAS v4 Seamless',
            value = False,
            disabled = True,
            key = 'ss_v4_smls',
            help = "Combines both Forecast and Consolidated historical data. Due to the unavailability of v4 Forecast, this is not available yet."
            )
            if v4_smls == True: mdl += dict_fld['v4_smls']
            elif v4_smls == False: mdl.replace(dict_fld['v4_smls'], '')

            v4_fcst = st.checkbox(
            label = 'GloFAS v4 Forecast',
            value = False,
            disabled = True,
            key = 'ss_v4_fcst',
            help = "Version 4 Forecast is not available yet."
            )
            if v4_fcst == True: mdl += dict_fld['v4_fcst']
            elif v4_fcst == False: mdl.replace(dict_fld['v4_fcst'], '')

            v4_consol = st.checkbox(
            label = 'GloFAS v4 Consolidated',
            value = False,
            disabled = False,
            key = 'ss_v4_consol',
            help = "Available only as historical reanalysis data (1984 - 2022)."
            )
            if v4_consol == True: mdl += dict_fld['v4_consol']
            elif v4_consol == False: mdl.replace(dict_fld['v4_consol'], '')

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
        dt_start, dt_end = date(2022, 6, 30), date(2022, 6, 30)
        dt_max = date(2022, 6, 30)

    dt = get_date(
        start = dt_start,
        end = dt_end,
        min = date(1984, 1, 1),
        max = dt_max,
        key = 'ss_dt_fld'
    )
    
    st.write("Date:", dt) #debug

    param += ('&start_date=' + dt[0].strftime('%Y-%m-%d') + '&end_date=' + dt[1].strftime('%Y-%m-%d'))
    
#debug:
st.write('Parameters:', param)
st.write(loc)
