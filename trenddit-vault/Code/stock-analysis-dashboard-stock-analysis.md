## Stock Analysis Dashboard
A stock analysis dashboard using open APIs with metrics for various growth indicators, interactive graphs, and filters.

## Install script
```bash
#!/bin/bash
mkdir stock_analysis_dashboard
cd stock_analysis_dashboard
python -m venv venv
source venv/bin/activate
pip install streamlit pandas yfinance plotly streamlit-option-menu requests numpy
```

## Run script
```bash
#!/bin/bash
streamlit run app.py
```

## File: app.py
```python
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Stock Analysis Dashboard")

selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Technical Analysis", "Fundamentals"],
    icons=["house", "graph-up", "clipboard-data"],
    orientation="horizontal",
)

def load_stock_data(symbol, period='1y'):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return stock, hist

def plot_stock_price(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))
    fig.update_layout(
        title="Stock Price Movement",
        yaxis_title="Price",
        xaxis_title="Date"
    )
    return fig

def calculate_metrics(df):
    metrics = {
        'Current Price': df['Close'][-1],
        'Daily Return': ((df['Close'][-1] - df['Close'][-2]) / df['Close'][-2]) * 100,
        'Volume': df['Volume'][-1],
        'YTD Return': ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
    }
    return metrics

if selected == "Dashboard":
    st.title("Stock Analysis Dashboard")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        symbol = st.text_input("Enter Stock Symbol", value="AAPL")
        period = st.selectbox("Select Time Period", 
                            ['1mo', '3mo', '6mo', '1y', '2y', '5y'])
    
    if symbol:
        stock, hist = load_stock_data(symbol, period)
        
        metrics = calculate_metrics(hist)
        
        cols = st.columns(4)
        for i, (label, value) in enumerate(metrics.items()):
            cols[i].metric(label, f"{value:.2f}")
        
        st.plotly_chart(plot_stock_price(hist), use_container_width=True)
        
        vol_fig = px.bar(hist, x=hist.index, y='Volume', title='Trading Volume')
        st.plotly_chart(vol_fig, use_container_width=True)

elif selected == "Technical Analysis":
    st.title("Technical Analysis")
    
    symbol = st.text_input("Enter Stock Symbol", value="AAPL")
    
    if symbol:
        stock, hist = load_stock_data(symbol)
        
        hist['MA20'] = hist['Close'].rolling(window=20).mean()
        hist['MA50'] = hist['Close'].rolling(window=50).mean()
        hist['MA200'] = hist['Close'].rolling(window=200).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Price'))
        fig.add_trace(go.Scatter(x=hist.index, y=hist['MA20'], name='20 MA'))
        fig.add_trace(go.Scatter(x=hist.index, y=hist['MA50'], name='50 MA'))
        fig.add_trace(go.Scatter(x=hist.index, y=hist['MA200'], name='200 MA'))
        
        fig.update_layout(title="Moving Averages", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)

elif selected == "Fundamentals":
    st.title("Fundamentals")
    
    symbol = st.text_input("Enter Stock Symbol", value="AAPL")
    
    if symbol:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Company Info")
            st.write(f"Sector: {info.get('sector', 'N/A')}")
            st.write(f"Industry: {info.get('industry', 'N/A')}")
            st.write(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
            
        with col2:
            st.subheader("Key Metrics")
            st.write(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
            st.write(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
            st.write(f"PEG Ratio: {info.get('pegRatio', 'N/A')}")
```

## File: requirements.txt
```
streamlit
pandas
yfinance
plotly
streamlit-option-menu
requests
numpy
```