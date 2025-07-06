## Marketing Landing Page
A marketing landing page

## Install script
```bash
#!/bin/bash
mkdir marketing_landing_page
cd marketing_landing_page
python -m venv venv
source venv/bin/activate
pip install streamlit
pip install streamlit-lottie
pip install requests
pip install streamlit-option-menu
```

## Run script
```bash
#!/bin/bash
streamlit run app.py
```

## File: app.py
```python
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Marketing Landing Page", page_icon=":rocket:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

with st.container():
    st.subheader("Hi, Welcome :wave:")
    st.title("A Digital Marketing Agency")
    st.write("We help businesses grow their online presence")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What We Do")
        st.write("##")
        st.write(
            """
            We offer comprehensive digital marketing solutions:
            - Social Media Marketing
            - Search Engine Optimization
            - Content Marketing
            - Email Marketing
            - Pay-Per-Click Advertising
            """
        )
        st.write("[Learn More >](https://example.com)")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")

with st.container():
    st.write("---")
    st.header("Our Services")
    st.write("##")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Social Media Marketing")
        st.write("Boost your brand presence across all social platforms")
    with col2:
        st.subheader("SEO Optimization")
        st.write("Improve your search engine rankings")
    with col3:
        st.subheader("Content Strategy")
        st.write("Create engaging content that converts")

with st.container():
    st.write("---")
    st.header("Contact Us")
    st.write("##")
    
    contact_form = """
    <form action="https://formsubmit.co/your@email.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

## File: style.css
```css
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap');

* {
    font-family: 'Roboto', sans-serif;
}

input[type=text], input[type=email], textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    margin-top: 6px;
    margin-bottom: 16px;
    resize: vertical;
}

button[type=submit] {
    background-color: #04AA6D;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button[type=submit]:hover {
    background-color: #45a049;
}
```