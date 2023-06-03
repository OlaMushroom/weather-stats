from requests import get
from geocoder import ip

dict_in_opt = {
    'opt_loc': "Location",
    'opt_coord': "Coordinates",
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
    'west': "West",
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

def forecast(model, lat, long, parameter): return get('https://api.open-meteo.com/v1/' + model + '?latitude=' + lat + '&longitude=' + long + parameter).json()

def ensemble(model, lat, long, parameter): return get('https://ensemble-api.open-meteo.com/v1/ensemble?' + '?latitude=' + lat + '&longitude=' + long + parameter).json()

def historical(lat, long, parameter): return get('https://archive-api.open-meteo.com/v1/archive?latitude=' + lat + '&longitude=' + long + parameter).json()

def climate(lat, long, parameter): return get('https://climate-api.open-meteo.com/v1/climate?latitude=' + lat + '&longitude=' + long + parameter).json()

def marine(lat, long, parameter): return get('https://marine-api.open-meteo.com/v1/marine?latitude=' + lat + '&longitude=' + long + parameter).json()

def flood(lat, long, parameter): return get('https://flood-api.open-meteo.com/v1/flood?latitude=' + lat + '&longitude=' + long + parameter).json()

def aq(lat, long, parameter): return get('https://air-quality-api.open-meteo.com/v1/air-quality?latitude=' + lat + '&longitude=' + long + parameter).json()