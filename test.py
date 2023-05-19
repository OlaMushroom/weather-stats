#import modules:
import datetime
import requests
import json
import streamlit

#uhh...the app's title i guess
streamlit.title("WEATHER")

#specify URL protocol:
url_protocol = streamlit.radio('Select URL protocol', ('HTTP', 'HTTPS'), 1).lower() + '://'
streamlit.markdown('*Note: HTTP is faster but less secure & vice versa (HTTPS is recommended).*')

api_option = streamlit.selectbox('Select weather service', ('WeatherAPI.com', 'Open-Meteo (Under construction)')) #specify weather API service
input_location = streamlit.text_input('Location') #input location


streamlit.divider() #display a horizontal rule
progress_bar = streamlit.progress(0, '# Progress: Fetching data...') #display a funny progress bar
streamlit.divider()

#WeatherAPI.com:
if api_option == 'WeatherAPI.com':
    api_service = 'api.weatherapi.com/v1/'
    api_request = '.json?key=&q='

#Open-Meteo (In progress):
#elif api_option == 'Open-Meteo':

#function to return API's requesting URL:
def url_request(weather_data_type, parameter):
    return url_protocol + api_service + weather_data_type + api_request + input_location + parameter #return URL

#function to return date if requested:
def date_request(date_min, date_max, key_value):
    date = streamlit.date_input('Choose date', min_value=date_min, max_value=date_max, key=key_value, help='Used for History/Astronomy') #input date
    return '&dt=' + date.strftime("%Y-%m-%d") #return date

data = requests.get(url_request('timezone','')).json() #get general data of input_location from timezone.json using url_request()
progress_bar.progress(100, '# Progress: Done!') #set the progress to 100% lmao

#output the location and country:
location = data["location"]["name"]
country = data["location"]["country"]

streamlit.write('##', location + ', ' + country)

#insert Streamlit's containers seperated into tabs:
tab_info, tab_current, tab_forecast, tab_history, tab_astronomy, tab_sports, tab_search = streamlit.tabs(["Info", "Current", "Forecast", "History", "Astronomy", "Sports", "Search"])

#manage tab_info ("Info"):
with tab_info:
    #output information from data:
    region = data["location"]["region"]
    latitude = data["location"]["lat"]
    longitude = data["location"]["lon"]
    timezone_id = data["location"]["tz_id"]
    local_time = data["location"]["localtime"]
    local_time_unix = data["location"]["localtime_epoch"]

    streamlit.subheader("Location's information") #display tab's title

    streamlit.write("Region:", region)
    streamlit.write("Latitude:", str(latitude))
    streamlit.write("Latitude:", str(longitude))
    streamlit.write("Time zone ID:", timezone_id)
    streamlit.write("Local time:", local_time)
    streamlit.write("Local time in Unix time:", str(local_time_unix))

with tab_current:
    data_current = requests.get(url_request('current','&aqi=yes')).json()

    streamlit.subheader("Current weather")

    streamlit.write(data_current) #output current.json (for debugging)

with tab_forecast:
    data_forecast = requests.get(url_request('forecast','&aqi=yes&alerts=yes')).json()

    streamlit.subheader("Forecast weather")

    #streamlit.write(data_forecast) #output forecast.json (for debugging)

#manage tab_history ("History"):
with tab_history:
    date_history = datetime.datetime.now() - datetime.timedelta(7)
    data_history = requests.get(url_request('history', date_request(date_history, datetime.datetime.now(), 'history date_input'))).json()

    streamlit.subheader("Historical weather")

    #streamlit.write(data_history) #output history.json (for debugging)

#manage tab_astronomy ("Astronomy"):
with tab_astronomy:
    data_astro = requests.get(url_request('astronomy', date_request(None, None, 'astronomy date_input'))).json()
    
    sunrise = data_astro["astronomy"]["astro"]["sunrise"]
    sunset = data_astro["astronomy"]["astro"]["sunset"]
    moonrise = data_astro["astronomy"]["astro"]["moonrise"]
    moonset = data_astro["astronomy"]["astro"]["moonset"]
    moon_phase = data_astro["astronomy"]["astro"]["moon_phase"]
    moon_illumination = data_astro["astronomy"]["astro"]["moon_illumination"]
    sun_up = data_astro["astronomy"]["astro"]["is_sun_up"]
    moon_up = data_astro["astronomy"]["astro"]["is_moon_up"]

    streamlit.subheader("Astronomy")

    streamlit.write('Sunrise time:', sunrise)
    streamlit.write('Sunset time:', sunset)
    streamlit.write('Moonrise time:', moonrise)
    streamlit.write('Moonset time:', moonset)
    streamlit.write('Moon phase:', moon_phase)
    streamlit.write('Moon illumination:', moon_illumination)

codeblock_example1 = '''
#manage tab_example ("Example"):
with tab_example:
    data_example = requests.get(url_request('example','')).json() #get data of input_location from example.json using url_request()

    #output information from data_example:

    streamlit.subheader("Example")

    streamlit.write(data_example) #output example.json (for debugging)
'''
streamlit.code(codeblock_example1)

data_condition = requests.get('https://www.weatherapi.com/docs/weather_conditions.json').json()
#streamlit.write(data_condition)
