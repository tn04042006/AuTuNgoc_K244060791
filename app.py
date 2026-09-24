import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Real-Time Gold Price",
    layout="wide"
)

API_URL = "https://biquote.io/api/XAUUSD/ohlc"

PARAMS = {
    "interval": "1m",
    "limit": 30
}


def get_candles():
    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data["bars"])

    df["openTime"] = pd.to_datetime(df["openTime"])

    df = df.sort_values("openTime")

    return df


st.title("Real-Time Gold Price Dashboard")
st.subheader("XAU/USD - 1 Minute Candlestick")

st.caption(
    "The dashboard automatically updates every 5 seconds "
    "using real-time data from an external API."
)


@st.fragment(run_every="5s")
def realtime_dashboard():

    try:
        # Get latest data
        df = get_candles()

        # Latest candle
        latest = df.iloc[-1]

        current_price = float(latest["close"])

        # Calculate price change
        if len(df) >= 2:

            previous_price = float(df.iloc[-2]["close"])

            change = current_price - previous_price

            change_percent = (
                change / previous_price
            ) * 100

        else:

            change = 0

            change_percent = 0


        # Metrics
        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Current Price",
                f"${current_price:.2f}"
            )


        with col2:

            st.metric(
                "Price Change",
                f"${change:.2f}",
                f"{change_percent:.2f}%"
            )


        with col3:

            update_time = latest["openTime"].strftime(
                "%H:%M:%S"
            )

            st.metric(
                "Last Update",
                update_time
            )


        # Candlestick chart
        fig = go.Figure()


        fig.add_trace(
            go.Candlestick(
                x=df["openTime"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="XAU/USD"
            )
        )


        fig.update_layout(
            title="XAU/USD Real-Time Candlestick",
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            height=600,
            xaxis_rangeslider_visible=False
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Latest candle information
        st.info(
            f"Latest candle: {update_time} | "
            f"Open: ${latest['open']:.2f} | "
            f"High: ${latest['high']:.2f} | "
            f"Low: ${latest['low']:.2f} | "
            f"Close: ${latest['close']:.2f}"
        )


        # Data source
        st.caption(
            "Data Source: BiQuote API | "
            "Symbol: XAU/USD | "
            "Candle Interval: 1 minute | "
            "Dashboard Refresh: 5 seconds"
        )


    except Exception as e:

        st.error(
            f"Unable to retrieve data from API: {e}"
        )


# Start realtime dashboard
realtime_dashboard()
