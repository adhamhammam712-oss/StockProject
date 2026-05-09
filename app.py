import streamlit as st
import yfinance as yf
import pandas as pd  


def get_stock_data(symbol, period):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        if df.empty:
            return None, None
            
        return df, ticker.info
    except Exception as e:
        return None, None


def main():
    st.set_page_config(page_title="Stock Market Analyzer", layout="wide")
    st.title(" Simple Stock Market Analyzer")
    
    symbol = st.text_input("Enter Stock Symbol:", "AAPL").upper()
    time_range = st.selectbox("Select Time Range:", ["7d", "1mo"])

    
    raw_data, info = get_stock_data(symbol, time_range)

    if raw_data is not None:
        
        data = pd.DataFrame(raw_data) 
        
        
        data.index = pd.to_datetime(data.index)
        
        
        data['MA_3'] = data['Close'].rolling(window=3).mean()

        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Company: {info.get('longName', symbol)}")
        with col2:
            current_price = data['Close'].iloc[-1]
            st.metric("Current Price", f"${current_price:.2f}")

        st.subheader("Price Trend (Close vs. 3-Day Moving Average)")
        st.line_chart(data[['Close', 'MA_3']])

        with st.expander("View Cleaned Historical Data"):
            
            clean_df = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            st.dataframe(clean_df)
            
    else:
        st.error(f"Error: Could not find data for '{symbol}'.")

if __name__ == "__main__":
    main()