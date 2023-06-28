
from datetime import datetime
#from dateutil.relativedelta import relativedelta as rltvD
from dateutil.parser import isoparse
import json
#from pandas import DataFrame
import streamlit as st
from meteostat import Point, Daily

# Get daily data:
data = Daily(
    loc = Point(49.2497, -123.1193, 70), # Create Point for Vancouver, BC
    start = datetime(2018, 1, 1),
    end = datetime(2018, 1, 2)
).fetch() 

data = data.to_json(
    path_or_buf = None,
    orient = "split",
    date_format = 'iso',
    date_unit = 's',
    indent = 4
)
data = json.loads(data)

for i in data["index"]:
    st.write(isoparse(i))

st.write(data) # debug
