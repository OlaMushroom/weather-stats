import streamlit as st
from datetime import datetime, timedelta
from requests import get


location = ''

'''
if 'ss_key_location' not in st.session_state:
    st.session_state.ss_key_location = ''
if st.session_state.ss_key_location != st.session_state.ss_key_input_location and st.session_state.ss_key_input_location != '':
    st.session_state.ss_key_location = st.session_state.ss_key_input_location
if location != st.session_state.ss_key_location:
    location = st.session_state.ss_key_location
else:
    pass
'''
  
progress_bar = st.sidebar.progress(0, '# Progress: Fetching data...') #display a funny progress bar

#function to return API's requesting URL:
def url_request(weather_data_type, parameter):
    return 'https://api.weatherapi.com/v1/' + weather_data_type + '.json?key=d4da2a259d0f490b89a144656231405&q=' + location + parameter #return URL

#function to return date if requested:
def date_request(date_min, date_max, key_value):
    date = st.date_input('Choose date', min_value=date_min, max_value=date_max, key=key_value, help='Used for History/Astronomy') #input date
    return '&dt=' + date.strftime("%Y-%m-%d") #return date

data = get(url_request('timezone','')).json() #get general data of location from timezone.json using url_request()
st.write(data)
progress_bar.progress(100, '# Progress: Done!') #set the progress to 100% lmao

#output the location and country:
location = data["location"]["name"]
country = data["location"]["country"]

st.write('##', location + ', ' + country)

#insert st's containers seperated into tabs:
tab_info, tab_current, tab_forecast, tab_history, tab_astronomy, tab_sports, tab_search = st.tabs(["Info", "Current", "Forecast", "History", "Astronomy", "Sports", "Search"])

#manage tab_info ("Info"):
with tab_info:
    #output information from data:
    region = data["location"]["region"]
    latitude = data["location"]["lat"]
    longitude = data["location"]["lon"]
    timezone_id = data["location"]["tz_id"]
    local_time = data["location"]["localtime"]
    local_time_unix = data["location"]["localtime_epoch"]

    st.subheader("Location's information") #display tab's title

    st.write("Region:", region)
    st.write("Latitude:", str(latitude))
    st.write("Latitude:", str(longitude))
    st.write("Time zone ID:", timezone_id)
    st.write("Local time:", local_time)
    st.write("Local time in Unix time:", str(local_time_unix))

with tab_current:
    data_current = get(url_request('current','&aqi=yes')).json()

    st.subheader("Current weather")

    st.write(data_current) #output current.json (for debugging)

with tab_forecast:
    data_forecast = get(url_request('forecast','&aqi=yes&alerts=yes')).json()

    st.subheader("Forecast weather")

    #st.write(data_forecast) #output forecast.json (for debugging)

with tab_history:
    date_history = datetime.now() - timedelta(7)
    data_history = get(url_request('history', date_request(date_history, datetime.now(), 'history date_input'))).json()

    st.subheader("Historical weather")

    #st.write(data_history) #output history.json (for debugging)

codeblock_example1 = '''
#manage tab_example ("Example"):
with tab_example:
    data_example = get(url_request('example','')).json() #get data of location from example.json using url_request()

    #output information from data_example:

    st.subheader("Example")

    st.write(data_example) #output example.json (for debugging)
'''
st.code(codeblock_example1)

data_condition = get('https://www.weatherapi.com/docs/weather_conditions.json').json()
#st.write(data_condition)
