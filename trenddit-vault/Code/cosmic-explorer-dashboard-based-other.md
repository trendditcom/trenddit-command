## Cosmic Explorer
A dashboard app based on data from Nasa, Webb, and other open API sources which displays data about astronomical entities and events.

## Install script
```bash
#!/bin/bash
mkdir cosmic_explorer
cd cosmic_explorer
python -m venv venv
source venv/bin/activate
pip install streamlit pandas requests plotly streamlit-option-menu streamlit-lottie streamlit-extras pillow
```

## Run script
```bash
#!/bin/bash
cd cosmic_explorer
source venv/bin/activate
streamlit run app.py
```

## File: app.py
```python
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from datetime import datetime, timedelta

st.set_page_config(page_title="Cosmic Explorer", layout="wide")

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def fetch_apod():
    nasa_api_key = "DEMO_KEY"
    url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
    response = requests.get(url)
    return response.json()

def fetch_neo():
    nasa_api_key = "DEMO_KEY"
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={nasa_api_key}"
    response = requests.get(url)
    return response.json()

def fetch_webb_images():
    url = "https://api.jwst-hub.com/images"
    response = requests.get(url)
    return response.json()

lottie_space = load_lottie("https://assets5.lottiefiles.com/packages/lf20_XiFKrK.json")

with st.sidebar:
    st_lottie(lottie_space, height=200)
    selected = option_menu(
        "Navigation",
        ["Home", "APOD", "Near Earth Objects", "Webb Telescope"],
        icons=["house", "camera", "globe", "telescope"]
    )

if selected == "Home":
    st.title("Welcome to Cosmic Explorer")
    st.write("Explore the wonders of space through NASA's data")
    
elif selected == "APOD":
    st.title("Astronomy Picture of the Day")
    apod_data = fetch_apod()
    st.image(apod_data["url"], caption=apod_data["title"])
    st.write(apod_data["explanation"])

elif selected == "Near Earth Objects":
    st.title("Near Earth Objects")
    neo_data = fetch_neo()
    today = datetime.today().strftime('%Y-%m-%d')
    
    asteroids = []
    for asteroid in neo_data["near_earth_objects"][today]:
        asteroids.append({
            "name": asteroid["name"],
            "diameter": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
            "hazardous": asteroid["is_potentially_hazardous_asteroid"],
            "miss_distance": float(asteroid["close_approach_data"][0]["miss_distance"]["kilometers"])
        })
    
    df = pd.DataFrame(asteroids)
    
    fig = px.scatter(df, x="diameter", y="miss_distance", 
                    color="hazardous", hover_data=["name"],
                    title="NEO Close Approaches")
    st.plotly_chart(fig)

elif selected == "Webb Telescope":
    st.title("James Webb Space Telescope Images")
    webb_data = fetch_webb_images()
    
    cols = st.columns(3)
    for idx, image in enumerate(webb_data[:9]):
        with cols[idx % 3]:
            st.image(image["image_url"], caption=image["title"])
```

## File: .gitignore
```
venv/
__pycache__/
.env
*.pyc
.DS_Store
```

## File: requirements.txt
```
streamlit
pandas
requests
plotly
streamlit-option-menu
streamlit-lottie
streamlit-extras
pillow
```