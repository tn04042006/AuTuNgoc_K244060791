!pip -q install dash plotly requests
import requests
import pandas as pd

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go


# ============================================================
# API
# ============================================================

API_URL = "https://biquote.io/api/XAUUSD/ohlc"

PARAMS = {
    "interval": "1m",
    "limit": 30
}


# ============================================================
# LẤY DỮ LIỆU
# ============================================================

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


# ============================================================
# DASH APP
# ============================================================

app = Dash(__name__)


app.layout = html.Div(

    style={
        "width": "90%",
        "margin": "auto",
        "fontFamily": "Arial"
    },

    children=[

        html.H1(
            "Real-Time Gold Price Dashboard",
            style={"textAlign": "center"}
        ),

        html.H3(
            "XAU/USD - 1 Minute Candlestick",
            style={"textAlign": "center"}
        ),

        # Thông tin giá
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-around",
                "textAlign": "center",
                "margin": "20px"
            },

            children=[

                html.Div([
                    html.H4("Current Price"),
                    html.H2(id="current-price")
                ]),

                html.Div([
                    html.H4("Price Change"),
                    html.H2(id="price-change")
                ]),

                html.Div([
                    html.H4("Last Update"),
                    html.H2(id="last-update")
                ])
            ]
        ),

        # Biểu đồ
        dcc.Graph(
            id="candlestick"
        ),

        # Status
        html.Div(
            id="status",
            style={
                "textAlign": "center",
                "margin": "15px"
            }
        ),

        html.Hr(),

        html.Div(
            "Data Source: BiQuote API | "
            "Symbol: XAU/USD | "
            "Candle: 1 minute | "
            "Refresh: 3 seconds",

            style={
                "textAlign": "center",
                "fontSize": "14px"
            }
        ),

        # Cập nhật mỗi 3 giây
        dcc.Interval(
            id="interval",
            interval=3000,
            n_intervals=0
        )
    ]
)


# ============================================================
# CALLBACK
# ============================================================

@app.callback(

    [
        Output("candlestick", "figure"),
        Output("current-price", "children"),
        Output("price-change", "children"),
        Output("last-update", "children"),
        Output("status", "children")
    ],

    Input(
        "interval",
        "n_intervals"
    )
)


def update_graph(n):

    # Lấy dữ liệu mới từ API
    df = get_candles()

    # Cây nến mới nhất
    latest = df.iloc[-1]

    current_price = float(latest["close"])

    # Tính thay đổi giá
    if len(df) >= 2:

        previous_price = float(
            df.iloc[-2]["close"]
        )

        change = current_price - previous_price

        change_percent = (
            change / previous_price
        ) * 100

    else:

        change = 0
        change_percent = 0


    # Hiển thị Price Change
    if change >= 0:

        price_change = (
            f"+${change:.2f} "
            f"(+{change_percent:.2f}%)"
        )

    else:

        price_change = (
            f"${change:.2f} "
            f"({change_percent:.2f}%)"
        )


    # ========================================================
    # CANDLESTICK
    # ========================================================

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

        xaxis_rangeslider_visible=False,

        template="plotly_white"
    )


    # ========================================================
    # THỜI GIAN
    # ========================================================

    update_time = latest["openTime"].strftime(
        "%H:%M:%S"
    )


    # ========================================================
    # STATUS
    # ========================================================

    status = (

        f"Latest candle: {update_time} | "

        f"Open: ${latest['open']:.2f} | "

        f"High: ${latest['high']:.2f} | "

        f"Low: ${latest['low']:.2f} | "

        f"Close: ${latest['close']:.2f} | "

        f"Update #{n}"
    )


    # ========================================================
    # TRẢ KẾT QUẢ
    # ========================================================

    return (

        fig,

        f"${current_price:.2f}",

        price_change,

        update_time,

        status
    )


# ============================================================
# CHẠY APP
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )
