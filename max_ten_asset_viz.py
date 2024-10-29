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

st.markdown("<h1 class='center'>Multi-Stock Comparision App</h1>", unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

st.markdown("<h3 class='center'>- Analysis to compare historical data of stocks</h3>" , unsafe_allow_html=True)
st.markdown("<h3 class='center'>- Stocks analyzed are identified by their ticker symbols</h3>", unsafe_allow_html=True)
st.markdown("<h3 class='center'>- All stock analysis done with data from Yahoo Finance</h3>" , unsafe_allow_html=True)

st.markdown("<h1 class='center'> </h1>", unsafe_allow_html=True)

ticker_symbol_data = {
    "Company Name": ["Apple", "NVIDIA", "Microsoft", "Alphabet", "Amazon", 
                     "Meta Platforms", "Berkshire Hathaway", "Broadcom", "Tesla", "Eli Lilly", 
                     "Walmart", "JPMorgan Chase", "Visa", "Exxon Mobil", "United Health", 
                     "Oracle", "Mastercard", "Procter & Gamble", "Costco", "Home Depot", 
                     "Johnson & Johnson", "AbbVie", "Bank of America", "Netflix", "Salesforce", 
                     "Coca-Cola", "Chevron", "Advanced Micro Devices", "Merck", "T-Mobile", 
                     "PepsiCo", "Accenture", "Linde", "Cisco Systems", "Wells Fargo", 
                     "Adobe", "McDonald's", "Thermo Fisher Scientific", "Philip Morris", "Abbott Laboratories", 
                     "ServiceNow", "QUALCOMM", "International Business Machines", "Texas Instruments", "Morgan Stanley", 
                     "American Express", "General Electric", "Caterpillar", "Intuitive Surgical", "Danaher"],
    "Ticker Symbol": ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN",
                      "META", "BRK.B", "AVGO", "TSLA", "LLY",
                      "WMT", "JPM", "V", "XOM", "UNH",
                      "ORCL", "MA", "PG", "COST", "HD",
                      "JNJ", "ABBV", "BAC", "NFLX", "CRM",
                      "KO", "CVX", "AMD", "MRK", "TMUS",
                      "PEP", "ACN", "LIN", "CSCO", "WFC",
                      "ADBE", "MCD", "TMO", "PM", "ABT",
                      "NOW", "QCOM", "IBM", "TXN", "MS",
                      "AXP", "GE", "CAT", "ISRG", "DHR",
                      ]
}

# Fetch stock data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    
    # Get the price on the start date
    start_price = data['Close'].iloc[0]
    
    # Get the price on the end date
    end_price = data['Close'].iloc[-1]
    
    # Calculate the difference
    price_difference = end_price - start_price

    # Return the data along with the new variables
    return {
        'data': data,
        'start_price': start_price,
        'end_price': end_price,
        'price_difference': price_difference
    }

# Create Streamlit app

col_list = st.columns([1, 2, 1, 2, 1])

# Initialize session state for the number of assets and tickers list
if "num_of_assets" not in st.session_state:
    st.session_state.num_of_assets = 1

if "tickers" not in st.session_state:
    st.session_state.tickers = []

with col_list[1]:
    st.title("Total Stocks")
    # Store the number of assets in session state
    st.session_state.num_of_assets = st.number_input("How many stocks do you want to analyze?", min_value=1, max_value=100)

with col_list[1]:
    st.write("")
    if st.button("Create Ticker Id Fields"):
        # Reset tickers list in session state based on the updated number of assets
        st.session_state.tickers = ["" for _ in range(st.session_state.num_of_assets)]

with col_list[3]:
    st.title("Date Range")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2023-12-31"))

# If tickers were created, display ticker input fields
if st.session_state.tickers:
    with col_list[1]:
        st.title("Stock Ids")
        for i in range(st.session_state.num_of_assets):
            # Use session state to keep values for each ticker input
            st.session_state.tickers[i] = st.text_input(f"Enter stock ticker #{i + 1} (e.g., AAPL)", st.session_state.tickers[i])

        st.write("")
        analysis_button = st.button("Perform Graphical Analysis")

    with col_list[3]:
        st.title("Ticker Id Ref.")
        st.write("50 top tickers of the S&P 500 Index")
        st.dataframe(ticker_symbol_data)
    
    if analysis_button:

####### Logic for Stock Price Display #######

        st.title("")
        st.markdown("<h3 class='center'>- To visualize changing price value, Close Price over time is displayed</h3>", unsafe_allow_html=True)

        # Initialize plot
        fig = go.Figure()

        for ticker in (st.session_state.tickers):
            if ticker:  # Ensure ticker input isn't empty
                stock_data = get_stock_data(ticker, start_date, end_date)
                df = stock_data['data']

                # Add each stock’s close price to the plot
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=ticker))

        # Display the plot
        fig.update_layout(title="Stock Prices by Close Price", xaxis_title="Date", yaxis_title="USD")
        st.plotly_chart(fig)

        # Create a new container for metrics display below the plot
        metric_col_list = st.columns(len(st.session_state.tickers))  # Create columns based on number of tickers
        metrics_container = st.container()

        for met_index, ticker in enumerate(st.session_state.tickers):
            if ticker:  # Ensure ticker input isn't empty
                stock_data = get_stock_data(ticker, start_date, end_date)

                # Round and extract values for metrics
                start_price = round(stock_data['start_price'], 2)
                end_price = round(stock_data['end_price'], 2)
                price_difference = round(stock_data['price_difference'], 2)

                # Display metrics in columns below the plot
                with metrics_container:
                    with metric_col_list[met_index]:  # Use met_index for correct column
                        st.metric(
                            label=f"Start: {start_price} | End: {end_price}",
                            value=f"{ticker}",
                            delta=price_difference
                        )


####### Logic for Total Percent Change Display #######

        st.title("")
        st.markdown("<h3 class='center'>-Equalizing Initial Value: Analysis of Total Percent Change</h3>", unsafe_allow_html=True)

        # Initialize plot
        fig = go.Figure()

        for ticker in st.session_state.tickers:
            if ticker:  # Ensure ticker input isn't empty
                stock_data = get_stock_data(ticker, start_date, end_date)
                df = stock_data['data']

                # Add each stock’s close price to the plot
                fig.add_trace(go.Scatter(
                    x=df.index, 
                    y=(df['Close'] / df['Close'].iloc[0] - 1) * 100, 
                    mode='lines', name=ticker)
                    )

        # Display the plot
        fig.update_layout(title="Total Percent Change",
                        xaxis_title="Date", 
                        yaxis_title="USD"
                        )
        st.plotly_chart(fig)

        # Create a new container for metrics display below the plot
        metric_col_list = st.columns(len(st.session_state.tickers))  # Create columns based on number of tickers
        metrics_container = st.container()

        for met_index, ticker in enumerate(st.session_state.tickers):
            if ticker:  # Ensure ticker input isn't empty
                stock_data = get_stock_data(ticker, start_date, end_date)

                # Round and extract values for metrics
                start_price = round(stock_data['start_price'], 2)
                end_price = round(stock_data['end_price'], 2)
                percent_change = round((end_price - start_price) / start_price * 100, 2)

               # Display metrics in columns below the plot
                with metrics_container:
                    with metric_col_list[met_index]:  # Use met_index for correct column
                        st.metric(
                            label=f"Start: {start_price} | End: {end_price}",
                            value=f"{ticker}",
                            delta=percent_change
                        )

####### Logic for Risk vs Return Display #######

        st.title("")
        st.markdown("<h3 class='center'>-To quantify risk, using pct returns, compare expected return with std of daily return</h3>", unsafe_allow_html=True)

        # Initialize plot
        fig = go.Figure()

        for ticker in st.session_state.tickers:
            if ticker:  # Ensure ticker input isn't empty
                stock_data = get_stock_data(ticker, start_date, end_date)
                df = stock_data['data']

                # Calculate daily returns
                df['Returns'] = df['Close'].pct_change()

                # Combine the returns into a single DataFrame for analysis
                rets = pd.DataFrame({
                    ticker: df['Returns']
                }).dropna()  # Drop rows with NaN values (i.e., where returns couldn't be calculated)

                # Calculate expected return (mean) and risk (standard deviation)
                expected_return = rets.mean()
                risk = rets.std()

                # Size of the points
                area = np.pi * 7

                fig.add_trace(go.Scatter(
                    x=expected_return, 
                    y=risk, 
                    mode='markers', 
                    marker=dict(size=area, color='lightpink', opacity=0.6),
                    text=rets.columns,  # Hover text (stock labels)
                    hovertemplate='<b>%{text}</b><br>Expected Return: %{x:.4f}<br>Risk (Std Dev): %{y:.4f}<extra></extra>'
                ))

                # Add annotations for each point using .iloc
                for i in range(len(rets.columns)):
                    ticker = rets.columns[i]  # Get ticker name
                    fig.add_annotation(
                        x=expected_return.iloc[i],  
                        y=risk.iloc[i],              
                        text=ticker,                 
                        showarrow=True,
                        arrowhead=0,
                        ax=0,
                        ay=-50,  # Adjust position of annotation
                        font=dict(color='black'),
                        bgcolor='white',
                        bordercolor='black',
                        borderwidth=1,
                        borderpad=4
                    )

        # Update layout with axis labels and title
        fig.update_layout(
            title="Expected Return vs Risk",
            xaxis_title="Expected Return",
            yaxis_title="Risk (Std Dev)",
            showlegend=False
        )

        # Display the Plotly chart
        st.plotly_chart(fig)

        # Create a new container for metrics display below the plot
        metric_col_list = st.columns(len(st.session_state.tickers))  # Create columns based on number of tickers
        metrics_container = st.container()

        for met_index, ticker in enumerate(st.session_state.tickers):
            if ticker:  # Ensure ticker input isn't empty

                # Calculate expected return (mean) and risk (standard deviation)
                expected_return = rets.mean().iloc[0]  # Use iloc to access the first position
                risk = rets.std().iloc[0]  # Use iloc to access the first position

                # Round the values for display
                expected_return = round(expected_return * 100, 2)  # Percent format
                risk = round(risk * 100, 2)  # Percent format

                # Display metrics
                with metrics_container:
                    with metric_col_list[met_index]:  # Use met_index for correct column
                        st.metric(
                            label=f'Expected Return {expected_return}%',
                            value=f"{ticker}",
                            delta=f"Risk (Std): {risk}%",
                            delta_color="inverse"  # Optional: inverse delta color for up/down
                        )
