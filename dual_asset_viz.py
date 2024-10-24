import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# CSS to center the elements
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centering the headers
st.markdown("<h1 class='center'>An EsteStyle Streamlit Page<br>Where Python Wiz Meets Data Viz!</h1>", unsafe_allow_html=True)
st.markdown("<h1 class='center'></h1>", unsafe_allow_html=True)

st.markdown("<img src='https://1drv.ms/i/s!ArWyPNkF5S-foZspwsary83MhqEWiA?embed=1&width=307&height=307' width='300' style='display: block; margin: 0 auto;'>" , unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

st.markdown("<h1 class='center'>Two Asset Comparision App</h1>", unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

st.markdown("<h3 class='center'>- Analysis to compare historical data of 2 assets</h3>" , unsafe_allow_html=True)
st.markdown("<h3 class='center'>- Allocations considered are identified by their ticker symbols</h3>", unsafe_allow_html=True)
st.markdown("<h3 class='center'>- All asset analysis done wit historical data from Yahoo Finance</h3>" , unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

# Fetch stock data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

# Create Streamlit app
st.markdown("<h3 class='center'>Stock IDs & Date Range</h3>" , unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

col_list = st.columns([1, 2, 2, 1])

with col_list[1]:
    
    ticker1 = st.text_input("Enter first stock ticker (e.g., AAPL, GOOGL)", "AAPL")
    ticker2 = st.text_input("Enter second stock ticker (e.g., AAPL, GOOGL)", "AAPL")

with col_list[2]:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-12-31"))

#with col2:
with col_list[1]:
    activation_achieved = st.button("Perform Graphical Analysis")

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

output_area = st.empty()

if activation_achieved:
    st.markdown("<h3 class='center'>- To quantify value, Close Price over time is displayed</h3>" , unsafe_allow_html=True)

    data1 = get_stock_data(ticker1, start_date, end_date)
    data2 = get_stock_data(ticker2, start_date, end_date)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data1.index, y=data1['Close'], mode='lines', name=f'{ticker1}'))
    fig.add_trace(go.Scatter(x=data2.index, y=data2['Close'], mode='lines', name=f'{ticker2}'))
    fig.update_layout(
        title=f"{ticker1} vs {ticker2}<br>Close Price", 
        xaxis_title='Date', 
        yaxis_title='USD')

    st.plotly_chart(fig)

    st.markdown("<h3 class='center'>- To estimate earning potential, Total Percent Return is claculated</h3>" , unsafe_allow_html=True)

    # Calculate the total percent change relative to the first date
    data1['Total Percent Change'] = (data1['Close'] / data1['Close'].iloc[0] - 1) * 100
    data2['Total Percent Change'] = (data2['Close'] / data2['Close'].iloc[0] - 1) * 100

    fig = go.Figure()

    # Add the first stock's total percent change line
    fig.add_trace(go.Scatter(x=data1.index, y=data1['Total Percent Change'], mode='lines', name=f'{ticker1}'))

    # Add the second stock's total percent change line
    fig.add_trace(go.Scatter(x=data2.index, y=data2['Total Percent Change'], mode='lines', name=f'{ticker2}'))

    # Update the layout of the chart
    fig.update_layout(
        title=f"{ticker1} vs {ticker2}<br>Total Percent Change",
        xaxis_title='Date',
        yaxis_title='Total Change (%)'
    )

    # Display the Plotly chart
    st.plotly_chart(fig)

    st.markdown("<h3 class='center'>- To quantify risk, using pct returns, compare expected return with std of daily return</h3>", unsafe_allow_html=True)

    # Calculate daily returns
    data1['Returns'] = data1['Close'].pct_change()
    data2['Returns'] = data2['Close'].pct_change()

    # Combine the returns into a single DataFrame for analysis
    rets = pd.DataFrame({
        ticker1: data1['Returns'],
        ticker2: data2['Returns']
    }).dropna()  # Drop rows with NaN values (i.e., where returns couldn't be calculated)

    # Calculate expected return (mean) and risk (standard deviation)
    expected_return = rets.mean()
    risk = rets.std()

    # Size of the points
    area = np.pi * 10

    # Create a Plotly scatter plot
    fig = go.Figure()

    # Add the scatter points (Expected return vs Risk)
    fig.add_trace(go.Scatter(
        x=expected_return, 
        y=risk, 
        mode='markers', 
        marker=dict(size=area, color='blue', opacity=0.6),
        text=rets.columns,  # Hover text (stock labels)
        hovertemplate='<b>%{text}</b><br>Expected Return: %{x:.4f}<br>Risk (Std Dev): %{y:.4f}<extra></extra>'
    ))

    # Update layout with axis labels and title
    fig.update_layout(
        title="Expected Return vs Risk (Standard Deviation)",
        xaxis_title="Expected Return",
        yaxis_title="Risk (Std Dev)",
        showlegend=False
    )

    # Display the Plotly chart
    st.plotly_chart(fig)