from requests import get
from geocoder import ip

dict_in_opt = {
    'opt_loc': "Location",
    'opt_coord': "Coordinates"
}

dict_loc_opt = {
    'loc_name': "Name/Postal code",
    'loc_ip': "IP address"
}

dict_coord_opt = {
    'dec_deg': "Decimal degrees",
    'dms': "Sexagesimal (DMS)"
}

dict_cardinal_dir = {
    'north': "North",
    'south': "South",
    'east': "East",
    'west': "West"
}

dict_wx_opt = {
    'fcst' : "Forecast",
    'ens' : "Ensemble",
    'hist' : "Historical",
    'clim' : "Climate",
    'mar' : "Marine",
    'fld' : "Flood",
    'aq' : "Air Quality"
}

dict_temp_unit = {
    'C': "Celsius (°C)",
    'F': "Fahrenheit (°F)"
}

dict_prec_unit = {
    'mm': "Millimeter",
    'in': "Inch"
}

dict_ws_unit = {
    'kmh': "Km/h",
    'ms': "m/s",
    'mph': "mi/h (Mph)",
    'kn': "Knots"
}

dflt_param = '&timezone=auto&timeformat=unixtime'

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

def param(lat, long): return '?timeformat=unixtime&timezone=auto&latitude=' + lat + '&longitude=' + long

def forecast(lat, long, model): return get('https://api.open-meteo.com/v1/' + model + param(lat, long)).json()

def ensemble(lat, long, model): return get('https://ensemble-api.open-meteo.com/v1/ensemble' + param(lat, long)).json()

def historical(lat, long): return get('https://archive-api.open-meteo.com/v1/archive' + param(lat, long)).json()

def climate(lat, long): return get('https://climate-api.open-meteo.com/v1/climate' + param(lat, long)).json()

def marine(lat, long): return get('https://marine-api.open-meteo.com/v1/marine' + param(lat, long)).json()

def flood(lat, long): return get('https://flood-api.open-meteo.com/v1/flood' + param(lat, long)).json()

def aq(lat, long): return get('https://air-quality-api.open-meteo.com/v1/air-quality' + param(lat, long)).json()