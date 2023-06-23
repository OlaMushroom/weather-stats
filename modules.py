"""SPLITTED CHUNK OF CODE (That is not using Streamlit)"""

# Import modules:
from requests import get
from geocoder import ip

# IMPORTANT (and i hate this):
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------

# Location input types:
dict_loc = {
    None : "---",
    "coord" : "Coordinates",
    "name" : "Name/Postal code",
    "ip" : "IP address",
}

# Unit types:
dict_unit = {
    "temp" : {
        "C" : ["celcius", "Celsius (°C)"],
        "F" : ["fahrenheit", "Fahrenheit (°F)"],
    },

    "prec" : {
        "mm" : ["millimeter", "Millimeter"],
        "in" : ["inch", "Inch"],
    },

    "ws" : {
        "kmh" : ["kmh", "Km/h"],
        "ms" : ["ms", "m/s"],
        "mph" : ["mph", "mi/h (Mph)"],
        "kn" : ["kn", "Knots"],
    },

    "mar" : {
        "m" : ["metric", "Metric"],
        "imp" : ["imperial", "Imperial"],
    },
}

# Weather (WX) types:
dict_wx = {
    None : "---",
    "fcst" : "Forecast",
    "ens" : "Ensemble",
    "hist" : "Historical",
    "clim" : "Climate",
    "aq" : "Air Quality",
    "mar" : "Marine",
    "fld" : "Flood",
}

# WX type: Forecast:
dict_fcst = {
    
}

# WX type: Ensemble:
dict_ens = {

}

# WX type: Historical:
dict_hist = {

}

# WX type: Climate:
dict_clim = {
    "temp_mn" : "temperature_2m_mean",
    "temp_max" : "temperature_2m_max",
    "temp_min" : "temperature_2m_min",

    "ws_mn" : "windspeed_10m_mean",
    "ws_max" : "windspeed_10m_max",

    "hmd_mn" : "relative_humidity_2m_mean",
    "hmd_max" : "relative_humidity_2m_max",
    "hmd_min" : "relative_humidity_2m_min",

    "dp_mn" : "dewpoint_2m_mean",
    "dp_max" : "dewpoint_2m_max",
    "dp_min" : "dewpoint_2m_min",

    "swr" : "shortwave_radiation_sum",
    "prec" : "precipitation_sum",
    "ra" : "rain_sum",
    "snwfl" : "snowfall_sum",
    "cc" : "cloudcover_mean",
    "sm" : "soil_moisture_0_to_10cm_mean",
    "slp" : "pressure_msl_mean",
    "vpd" : "vapor_pressure_deficit_mean",
    "et0" : "et0_fao_evapotranspiration_sum",

    # Models:
    "EC" : "EC_Earth3P_HR",
    "MRI" : "MRI_AGCM3_2_S",
    "MIROC" : "NICAM16_8S",
    "CMCC" : "CMCC_CM2_VHR4",
    "MPI" : "MPI_ESM1_2_XR",
    "AS-RCEC" : "HiRAM_SIT_HR",
    "CAS" : "FGOALS_f3_H",
}

# WX type: Air Quality:
dict_aq = {
    "uv" : "uv_index",
    "uv_cs" : "uv_index_clear_sky",
    "du" : "dust",
    "aod" : "aerosol_optical_depth",
    "pm10" : "pm10",
    "pm2.5" : "pm2_5",
    "co" : "carbon_monoxide",
    "no2" : "nitrogen_dioxide",
    "so2" : "sulphur_dioxide",
    "o3" : "ozone",
    
    # Europe:
    "nh3" : "ammonia",
    "aldr" : "alder_pollen",
    "bp" : "birch_pollen",
    "gp" : "grass_pollen",
    "mp" : "mugwort_pollen",
    "ol" : "olive_pollen",
    "rw" : "ragweed_pollen",

    # European AQI:
    "eu" : "european_aqi",
    "eu_pm10" : "european_aqi_pm10",
    "eu_pm2.5" : "european_aqi_pm2_5",
    "eu_no2" : "european_aqi_no2",
    "eu_so2" : "european_aqi_so2",
    "eu_o3" : "european_aqi_o3",

    # US AQI:
    "us" : "us_aqi",
    "us_pm10" : "us_aqi_pm10",
    "us_pm2.5" : "us_aqi_pm2_5",
    "us_co" : "us_aqi_co",
    "us_no2" : "us_aqi_no2",
    "us_so2" : "us_aqi_so2",
    "us_o3" : "us_aqi_o3",
}

# WX type: Marine:
dict_mar = {
    # Hourly variables:
    "hrly" : {
        "mn_ht" : "wave_height",
        "mn_dir" : "wave_direction",
        "mn_prd" : "wave_period",

        "wnd_ht" : "wind_wave_height",
        "wnd_dir" : "wind_wave_direction",
        "wnd_prd" : "wind_wave_period",
        "wnd_prd_pk" : "wind_wave_peak_period",

        "swll_ht" : "swell_wave_height",
        "swll_dir" : "swell_wave_direction",
        "swll_prd" : "swell_wave_period",
        "swll_prd_pk" : "swell_wave_peak_period",
    },

    # Daily variables:
    "dly" : {
        "mn_ht" : "wave_height_max",
        "mn_dir" : "wave_direction_dominant",
        "mn_prd" : "wave_period_max",

        "wnd_ht" : "wind_wave_height_max",
        "wnd_dir" : "wind_wave_direction_dominant",
        "wnd_prd" : "wind_wave_period_max",
        "wnd_prd_pk" : "wind_wave_peak_period_max",

        "swll_ht" : "swell_wave_height_max",
        "swll_dir" : "swell_wave_direction_dominant",
        "swll_prd" : "swell_wave_period_max",
        "swll_prd_pk" : "swell_wave_peak_period_max",
    },
}

# WX type: Flood:
dict_fld = {
    "river_discharge" : "River Discharge",
    "river_discharge_mean" : "River Discharge Mean",
    "river_discharge_median" : "River Discharge Median",
    "river_discharge_max" : "River Discharge Max",
    "river_discharge_min" : "River Discharge Min",
    "river_discharge_p25" : "River Discharge 25ᵗʰ Percentile",
    "river_discharge_p75" : "River Discharge 75ᵗʰ Percentile",
}

#-----------------------------------------------------------------------------------------------------------------------------------------------------

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

def find_name(loc): return get("https://geocoding-api.open-meteo.com/v1/search?name=" + loc + "&count=1&language=en&format=json").json()["results"][0] # Location search based on Name/Postal Code

#def forecast(param, model): return get("https://api.open-meteo.com/v1/" + model + param).json()

#def ensemble(param): return get("https://ensemble-api.open-meteo.com/v1/ensemble" + param).json()

#def historical(param): return get("https://archive-api.open-meteo.com/v1/archive" + param).json()

#def climate(param): return get("https://climate-api.open-meteo.com/v1/climate" + param).json()

#def aq(param): return get("https://air-quality-api.open-meteo.com/v1/air-quality?" + param).json()

def marine(param): return get("https://marine-api.open-meteo.com/v1/marine?" + param).json() # Return "WX type: Marine" data

def flood(param): return get("https://flood-api.open-meteo.com/v1/flood?" + param).json() # Return "WX type: Flood" data

#-----------------TEMP CHUNK OF CODE-----------------:
'''

def pref():
    with st.expander(
        label = "Preferences",
        expanded = True
    ):
        temp_unit = st.radio(
            label = "Temperature Unit",
            options = ("C", "F"),
            format_func = lambda x: dict_unit.get(x),
            horizontal = True,
            key = "ss_temp_unit",
            help = ""
        )

        prec_unit = st.radio(
            label = "Precipitation Unit",
            options = ("mm", "in"),
            format_func = lambda x: dict_unit.get(x),
            horizontal = True,
            key = "ss_prec_unit",
            help = ""
        )

        ws_unit = st.radio(
            label = "Wind Speed Unit",
            options = ("kmh", "ms", "mph", "kn"),
            format_func = lambda x: dict_unit.get(x),
            horizontal = True,
            key = "ss_ws_unit",
            help = ""
        )

'''
