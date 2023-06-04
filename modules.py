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

dict_wx_opt = {
    'fcst' : "Forecast",
    'ens' : "Ensemble",
    'hist' : "Historical",
    'clim' : "Climate",
    'mar' : "Marine",
    'fld' : "Flood",
    'aq' : "Air Quality",
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

dict_mar = {
    'len_unit' : {
        'dflt' : "&length_unit=",
        'm' : "metric",
        'imp' : "imperial",
    },
    'hrly' : {
        'dflt' : "&hourly=",

        'mean' : {
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

        'swell' : {
            'ht' : "swell_wave_height,",
            'dir' : "swell_wave_direction,",
            'prd' : "swell_wave_period,",
            'prd_pk' : "swell_wave_peak_period,",
        }
    },

    'dly' : {
        'dflt' : "&daily=",
    },
}

dict_fld = {
    'dly' : {
        'dflt' : "&daily=",
        'riv_dc' : "river_discharge,",
        'riv_dc_med' : "river_discharge_median,",
        'riv_dc_max' : "river_discharge_max,",
        'riv_dc_min' : "river_discharge_min,",
        'riv_dc_p25' : "river_discharge_p25,",
        'riv_dc_p75' : "river_discharge_p75,",
        'ens' : "&ensemble=true"
    },

    'mdl' : {
        'dflt': "&models=",

        'v3' : {
            'smls' : "seamless_v3,",
            'fcst' : "forecast_v3,",
            'consol' : "consolidated_v3,",
        },

        'v4' : {
            'smls' : "seamless_v4,",
            'fcst' : "forecast_v4,",
            'consol' : "consolidated_v4,",
        }
    },
}

def dec_deg(dec, min, sec): return round(dec + min/60 + sec/3600, 4)

def find_ip(loc):
    g = ip(loc)
    return {
        'ip': g.ip,
        'lat': g.latlng[0],
        'long': g.latlng[1],
        'city': g.city,
        'state': g.state,
        'country': g.country
    }

def find_name(loc): return get('https://geocoding-api.open-meteo.com/v1/search?name=' + loc + '&count=1&language=en&format=json').json()['results'][0]

def forecast(param, model): return get('https://api.open-meteo.com/v1/' + model + param).json()

def ensemble(param): return get('https://ensemble-api.open-meteo.com/v1/ensemble' + param).json()

def historical(param): return get('https://archive-api.open-meteo.com/v1/archive' + param).json()

def climate(param): return get('https://climate-api.open-meteo.com/v1/climate' + param).json()

def marine(param): return get('https://marine-api.open-meteo.com/v1/marine' + param).json()

def flood(param): return get('https://flood-api.open-meteo.com/v1/flood' + param).json()

def aq(param): return get('https://air-quality-api.open-meteo.com/v1/air-quality' + param).json()