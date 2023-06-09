from requests import get
from geocoder import ip

dict_loc_opt = {
    'loc' : "Location",
    'coord' : "Coordinates",
    'name' : "Name/Postal code",
    'ip' : "IP address",
    'dd' : "Decimal degrees",
    'dms' : "Sexagesimal (DMS)",
}

dict_cd_dir = {
    'N' : "North",
    'S' : "South",
    'E' : "East",
    'W' : "West",
}

dict_unit = {
    'C' : "Celsius (°C)",
    'F' : "Fahrenheit (°F)",
    'm' : "Metric",
    'imp' : "Imperial",
    'mm' : "Millimeter",
    'in' : "Inch",
    'kmh' : "Km/h",
    'ms' : "m/s",
    'mph' : "mi/h (Mph)",
    'kn' : "Knots",
}

dict_wx = {
    'fcst' : "Forecast",
    'ens' : "Ensemble",
    'hist' : "Historical",
    'clim' : "Climate",
    'mar' : "Marine",
    'fld' : "Flood",
    'aq' : "Air Quality",
}

dict_clim = {
    'temp' : {
        'mn' : "temperature_2m_mean,",
        'max' : "temperature_2m_max,",
        'min' : "temperature_2m_min,",
    },

    'ws' : {
        'mn' : "windspeed_10m_mean,",
        'max' : "windspeed_10m_max,",
    },

    'hmd' : {
        'mn' : "relative_humidity_2m_mean,",
        'max' : "relative_humidity_2m_max,",
        'min' : "relative_humidity_2m_min,",
    },

    'dp' : {
        'mn' : "dewpoint_2m_mean,",
        'max' : "dewpoint_2m_max,",
        'min' : "dewpoint_2m_min,",
    },

    'swr' : "shortwave_radiation_sum,",
    'prec' : "precipitation_sum,",
    'ra' : "rain_sum,",
    'snwfl' : "snowfall_sum,",
    'cc' : "cloudcover_mean,",
    'sm' : "soil_moisture_0_to_10cm_mean,",
    'slp' : "pressure_msl_mean,",
    'vpd' : "vapor_pressure_deficit_mean,",
    'ref_ET0' : "et0_fao_evapotranspiration_sum,",


    #models:
    'EC' : "EC_Earth3P_HR,",
    'MRI' : "MRI_AGCM3_2_S,",
    'MIROC' : "NICAM16_8S,",
    'CMCC' : "CMCC_CM2_VHR4,",
    'MPI' : "MPI_ESM1_2_XR,",
    'AS-RCEC' : "HiRAM_SIT_HR,",
    'CAS' : "FGOALS_f3_H,",
}

dict_mar = {
    'hrly' : {
        'mn' : {
            'ht' : "wave_height,",
            'dir' : "wave_direction,",
            'prd' : "wave_period,",
        },
        'wnd' : {
            'ht' : "wind_wave_height,",
            'dir' : "wind_wave_direction,",
            'prd' : "wind_wave_period,",
            'prd_pk' : "wind_wave_peak_period,",
        },
        'swll' : {
            'ht' : "swell_wave_height,",
            'dir' : "swell_wave_direction,",
            'prd' : "swell_wave_period,",
            'prd_pk' : "swell_wave_peak_period,",
        },
    },

    'dly' : {
        'mn' : {
            'ht' : "wave_height_max,",
            'dir' : "wave_direction_dominant,",
            'prd' : "wave_period_max,",
        },
        'wnd' : {
            'ht' : "wind_wave_height_max,",
            'dir' : "wind_wave_direction_dominant,",
            'prd' : "wind_wave_period_max,",
            'prd_pk' : "wind_wave_peak_period_max,",
        },
        'swll' : {
            'ht' : "swell_wave_height_max,",
            'dir' : "swell_wave_direction_dominant,",
            'prd' : "swell_wave_period_max,",
            'prd_pk' : "swell_wave_peak_period_max,",
        },
    },

    #units:
    'unit' : "&length_unit=",
    'm' : "metric",
    'imp' : "imperial",
}

dict_fld = {
    'dc' : "river_discharge,",
    'med' : "river_discharge_median,",
    'max' : "river_discharge_max,",
    'min' : "river_discharge_min,",
    'p25' : "river_discharge_p25,",
    'p75' : "river_discharge_p75,",
    'ens' : "&ensemble=true",

    #models:
    'v3' : {
        'smls' : "seamless_v3,",
        'fcst' : "forecast_v3,",
        'consol' : "consolidated_v3,",
    },
    'v4' : {
        'smls' : "seamless_v4,",
        'fcst' : "forecast_v4,",
        'consol' : "consolidated_v4,",
    },
}

dict_aq = {
    'uv' : "uv_index,",
    'uv_cs' : "uv_index_clear_sky,",
    'du' : "dust,",
    'aod' : "aerosol_optical_depth,",
    'pm10' : "pm10,",
    'pm2.5' : "pm2_5,",
    'co' : "carbon_monoxide,",
    'no2' : "nitrogen_dioxide,",
    'so2' : "sulphur_dioxide,",
    'o3' : "ozone,",
    
    #Europe:
    'nh3' : "ammonia,",
    'aldr' : "alder_pollen,",
    'bp' : "birch_pollen,",
    'gp' : "grass_pollen,",
    'mp' : "mugwort_pollen,",
    'ol' : "olive_pollen,",
    'rw' : "ragweed_pollen,",

    #European AQI:
    'eu' : "european_aqi,",
    'eu_pm10' : "european_aqi_pm10,",
    'eu_pm2.5' : "european_aqi_pm2_5,",
    'eu_no2' : "european_aqi_no2,",
    'eu_so2' : "european_aqi_so2,",
    'eu_o3' : "european_aqi_o3,",

    #US AQI:
    'us' : "us_aqi,",
    'us_pm10' : "us_aqi_pm10,",
    'us_pm2.5' : "us_aqi_pm2_5,",
    'us_co' : "us_aqi_co,",
    'us_no2' : "us_aqi_no2,",
    'us_so2' : "us_aqi_so2,",
    'us_o3' : "us_aqi_o3,",
}

def dd(dec, min, sec): return round(dec + min/60 + sec/3600, 4)

def find_ip(loc):
    g = ip(loc)
    return {
        'ip': g.ip,
        'lat': g.latlng[0],
        'long': g.latlng[1],
        'city': g.city,
        'state': g.state,
        'country': g.country,
    }

def find_name(loc): return get('https://geocoding-api.open-meteo.com/v1/search?name=' + loc + '&count=1&language=en&format=json').json()['results'][0]

def forecast(param, model): return get('https://api.open-meteo.com/v1/' + model + param).json()

def ensemble(param): return get('https://ensemble-api.open-meteo.com/v1/ensemble' + param).json()

def historical(param): return get('https://archive-api.open-meteo.com/v1/archive' + param).json()

def climate(param): return get('https://climate-api.open-meteo.com/v1/climate' + param).json()

def marine(param): return get('https://marine-api.open-meteo.com/v1/marine?' + param).json()

def flood(param): return get('https://flood-api.open-meteo.com/v1/flood?' + param).json()

def aq(param): return get('https://air-quality-api.open-meteo.com/v1/air-quality?' + param).json()
