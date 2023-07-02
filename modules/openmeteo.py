"""SPLITTED CHUNK OF CODE (That is not using Streamlit)"""

# Import modules:
from requests import get

# Unit types:
dict_unit = {
    "temp" : {
        "celcius" : "Celsius (°C)",
        "fahrenheit" : "Fahrenheit (°F)",
    },

    "prec" : {
        "millimeter" : "Millimeter",
        "inch" : "Inch",
    },

    "ws" : {
        "kmh" : "Km/h",
        "ms" : "m/s",
        "mph" : "mi/h (Mph)",
        "kn" : "Knots",
    },

    "len" : {
        "metric" : "Metric",
        "imperial" : "Imperial",
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
        "wave_height" : "Wave Height",
        "wave_direction" : "Wave Direction",
        "wave_period" : "Wave Period",

        "wind_wave_height" : "Wind Wave Height",
        "wind_wave_direction" : "Wind Wave Direction",
        "wind_wave_period" : "Wind Wave Period",
        "wind_wave_peak_period" : "Wind Wave Peak Period",

        "swell_wave_height" : "Swell Wave Height",
        "swell_wave_direction" : "Swell Wave Direction",
        "swell_wave_period" : "Swell Wave Period",
        "swell_wave_peak_period" : "Swell Wave Peak Period",
    },

    # Daily variables:
    "dly" : {
        "wave_height_max" : "Wave Height Max",
        "wave_direction_dominant" : "Wave Direction Dominant",
        "wave_period_max" : "Wave Period Max",

        "wind_wave_height_max" : "Wind Wave Height Max",
        "wind_wave_direction_dominant" : "Wind Wave Direction Dominant",
        "wind_wave_period_max" : "Wind Wave Period Max",
        "wind_wave_peak_period_max" : "Wind Wave Peak Period Max",

        "swell_wave_height_max" : "Swell Wave Height Max",
        "swell_wave_direction_dominant" : "Swell Wave Direction Dominant",
        "swell_wave_period_max" : "Swell Wave Period Max",
        "swell_wave_peak_period_max" : "Swell Wave Peak Period Max",
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
