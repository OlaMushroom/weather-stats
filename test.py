from requests import get
import streamlit

url_protocol = streamlit.radio('Select URL protocol', ('HTTP', 'HTTPS'), 1).lower()
streamlit.markdown('*Note: HTTP is faster but less secure & vice versa (HTTPS is recommended).*')
api_option = streamlit.selectbox('Select weather service', ('WeatherAPI.com', 'Open-Meteo (Under construction)'))

if api_option == 'WeatherAPI.com':
    api_service = 'api.weatherapi.com/v1/'
    api_token = 'key='
    weather_data_type = streamlit.selectbox('Select weather data type', ('Current', 'Forecast', 'History', 'Astronomy', 'Sports', 'Search')).lower()
    input_location = '&q=' + streamlit.text_input('Location')

#elif api_option == 'Open-Meteo':

request_url =  url_protocol + '://' + api_service + weather_data_type + '.json?' + api_token + input_location + "&aqi=yes"

if weather_data_type == 'history' or weather_data_type == 'astronomy':
    date = streamlit.date_input('Choose date').strftime("%Y-%m-%d")
    request_url += '&dt=' + date

data = get(request_url).json()

streamlit.write(data)
