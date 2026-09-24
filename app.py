import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Real-Time Gold Price",
    layout="wide"
)

st.title("Real-Time Gold Price Dashboard")
st.subheader("XAU/USD - Real-Time Candlestick")

html_code = """
<!DOCTYPE html>
<html>
<head>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: white;
}

#chart {
    width: 100%;
    height: 600px;
}

#status {
    padding: 10px;
    font-size: 14px;
}

</style>

</head>

<body>

<div id="chart"></div>

<div id="status">
    Connecting to XAU/USD API...
</div>


<script>

const API_URL =
    "https://biquote.io/api/XAUUSD/ohlc?interval=1m&limit=30";


async function updateChart() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        const bars = data.bars;

        const times = [];
        const opens = [];
        const highs = [];
        const lows = [];
        const closes = [];


        bars.forEach(bar => {

            times.push(bar.openTime);

            opens.push(Number(bar.open));

            highs.push(Number(bar.high));

            lows.push(Number(bar.low));

            closes.push(Number(bar.close));

        });


        const latestPrice =
            closes[closes.length - 1];


        const previousPrice =
            closes[closes.length - 2];


        const change =
            latestPrice - previousPrice;


        const changePercent =
            (change / previousPrice) * 100;


        const trace = {

            x: times,

            open: opens,

            high: highs,

            low: lows,

            close: closes,

            type: "candlestick",

            name: "XAU/USD"

        };


        const layout = {

            title: "XAU/USD Real-Time Candlestick",

            xaxis: {
                title: "Time",
                rangeslider: {
                    visible: false
                }
            },

            yaxis: {
                title: "Price (USD)"
            },

            height: 600,

            margin: {
                l: 60,
                r: 30,
                t: 60,
                b: 50
            }

        };


        const chart =
            document.getElementById("chart");


        if (!chart.data) {

            Plotly.newPlot(
                chart,
                [trace],
                layout,
                {
                    responsive: true
                }
            );

        } else {

            Plotly.react(
                chart,
                [trace],
                layout,
                {
                    responsive: true
                }
            );

        }


        document.getElementById("status").innerHTML =
            "Current Price: $" +
            latestPrice.toFixed(2) +
            " &nbsp; | &nbsp; Change: $" +
            change.toFixed(2) +
            " (" +
            changePercent.toFixed(2) +
            "%) &nbsp; | &nbsp; Updated: " +
            new Date().toLocaleTimeString();

    }

    catch (error) {

        document.getElementById("status").innerHTML =
            "Unable to retrieve data: " +
            error.message;

    }

}


// First update
updateChart();


// Update every 3 seconds
setInterval(
    updateChart,
    3000
);

</script>

</body>
</html>
"""


components.html(
    html_code,
    height=700,
    scrolling=False
)


st.caption(
    "Data Source: BiQuote API | "
    "Symbol: XAU/USD | "
    "Update Interval: 3 seconds"
)
