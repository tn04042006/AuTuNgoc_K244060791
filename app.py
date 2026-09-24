import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Real-Time Gold Monitor",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("📈 Real-Time Gold Monitor")

st.subheader(
    "XAU/USD Real-Time Price & Short-Term Market Analysis"
)

st.caption(
    "Live financial data monitoring dashboard using an external API."
)


# =========================================================
# REAL-TIME DASHBOARD
# =========================================================

html_code = """

<!DOCTYPE html>

<html>

<head>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>


<style>

/* ============================= */
/* GENERAL */
/* ============================= */

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: transparent;

}


/* ============================= */
/* STATUS */
/* ============================= */

.status-bar {

    display: flex;

    align-items: center;

    gap: 20px;

    margin-bottom: 15px;

    padding: 10px 15px;

    border-radius: 8px;

    background: rgba(0, 200, 100, 0.08);

}


.live-dot {

    display: inline-block;

    width: 10px;

    height: 10px;

    border-radius: 50%;

    background: #00c853;

    margin-right: 6px;

}


.status-text {

    font-size: 14px;

    font-weight: bold;

}


.update-time {

    font-size: 13px;

    color: #666;

}


/* ============================= */
/* METRIC CARDS */
/* ============================= */

.metrics {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 12px;

    margin-bottom: 20px;

}


.card {

    padding: 16px;

    border-radius: 10px;

    background: rgba(128, 128, 128, 0.08);

    border: 1px solid rgba(128, 128, 128, 0.15);

}


.card-title {

    font-size: 13px;

    color: #777;

    margin-bottom: 7px;

}


.card-value {

    font-size: 24px;

    font-weight: bold;

}


.card-change {

    margin-top: 5px;

    font-size: 13px;

}


/* ============================= */
/* ANALYSIS */
/* ============================= */

.analysis {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;

    margin-top: 15px;

    margin-bottom: 20px;

}


.analysis-card {

    padding: 15px;

    border-radius: 10px;

    background: rgba(128, 128, 128, 0.08);

    border: 1px solid rgba(128, 128, 128, 0.15);

}


.analysis-title {

    font-size: 13px;

    color: #777;

    margin-bottom: 8px;

}


.analysis-value {

    font-size: 20px;

    font-weight: bold;

}


/* ============================= */
/* ALERT */
/* ============================= */

.alert-box {

    padding: 18px;

    border-radius: 10px;

    background: rgba(255, 180, 0, 0.08);

    border: 1px solid rgba(255, 180, 0, 0.25);

    margin-top: 15px;

}


.alert-title {

    font-weight: bold;

    margin-bottom: 10px;

}


input {

    padding: 9px;

    border-radius: 6px;

    border: 1px solid #aaa;

    width: 180px;

}


button {

    padding: 9px 15px;

    border-radius: 6px;

    border: none;

    cursor: pointer;

    margin-left: 6px;

}


#alert-message {

    margin-top: 10px;

    font-weight: bold;

}


/* ============================= */
/* RESPONSIVE */
/* ============================= */

@media (max-width: 800px) {

    .metrics {

        grid-template-columns:
            repeat(2, 1fr);

    }

    .analysis {

        grid-template-columns:
            1fr;

    }

}

</style>

</head>


<body>


<!-- ===================================================== -->
<!-- STATUS BAR -->
<!-- ===================================================== -->

<div class="status-bar">

    <div class="status-text">

        <span class="live-dot"></span>

        LIVE

    </div>


    <div id="api-status">

        API: Connecting...

    </div>


    <div class="update-time">

        Last update:
        <span id="update-time">
            --
        </span>

    </div>

</div>


<!-- ===================================================== -->
<!-- METRICS -->
<!-- ===================================================== -->

<div class="metrics">


    <div class="card">

        <div class="card-title">

            Current Price

        </div>

        <div
            class="card-value"
            id="current-price"
        >

            --

        </div>

    </div>


    <div class="card">

        <div class="card-title">

            Price Change

        </div>

        <div
            class="card-value"
            id="price-change"
        >

            --

        </div>

        <div
            class="card-change"
            id="price-percent"
        >

            --

        </div>

    </div>


    <div class="card">

        <div class="card-title">

            Period High

        </div>

        <div
            class="card-value"
            id="period-high"
        >

            --

        </div>

    </div>


    <div class="card">

        <div class="card-title">

            Period Low

        </div>

        <div
            class="card-value"
            id="period-low"
        >

            --

        </div>

    </div>

</div>


<!-- ===================================================== -->
<!-- CHART -->
<!-- ===================================================== -->

<div id="chart"></div>


<!-- ===================================================== -->
<!-- ANALYSIS -->
<!-- ===================================================== -->

<div class="analysis">


    <div class="analysis-card">

        <div class="analysis-title">

            MA5

        </div>

        <div
            class="analysis-value"
            id="ma5"
        >

            --

        </div>

    </div>


    <div class="analysis-card">

        <div class="analysis-title">

            MA10

        </div>

        <div
            class="analysis-value"
            id="ma10"
        >

            --

        </div>

    </div>


    <div class="analysis-card">

        <div class="analysis-title">

            Short-Term Trend

        </div>

        <div
            class="analysis-value"
            id="trend"
        >

            --

        </div>

    </div>

</div>


<!-- ===================================================== -->
<!-- VOLATILITY -->
<!-- ===================================================== -->

<div class="analysis">


    <div class="analysis-card">

        <div class="analysis-title">

            Volatility

        </div>

        <div
            class="analysis-value"
            id="volatility"
        >

            --

        </div>

    </div>


    <div class="analysis-card">

        <div class="analysis-title">

            Candle Interval

        </div>

        <div class="analysis-value">

            1 minute

        </div>

    </div>


    <div class="analysis-card">

        <div class="analysis-title">

            Refresh Rate

        </div>

        <div class="analysis-value">

            3 seconds

        </div>

    </div>

</div>


<!-- ===================================================== -->
<!-- PRICE ALERT -->
<!-- ===================================================== -->

<div class="alert-box">

    <div class="alert-title">

        🔔 Price Alert

    </div>


    <input
        id="target-price"
        type="number"
        placeholder="Target price"
        step="0.01"
    >


    <button
        onclick="setAlert()"
    >

        Set Alert

    </button>


    <button
        onclick="clearAlert()"
    >

        Clear

    </button>


    <div id="alert-message">

        No alert configured.

    </div>

</div>


<script>


// =========================================================
// API
// =========================================================

const API_URL =
    "https://biquote.io/api/XAUUSD/ohlc?interval=1m&limit=30";


let targetPrice = null;

let chartInitialized = false;


// =========================================================
// PRICE ALERT
// =========================================================

function setAlert() {

    const input =
        document.getElementById(
            "target-price"
        );


    const value =
        parseFloat(input.value);


    if (
        isNaN(value) ||
        value <= 0
    ) {

        document.getElementById(
            "alert-message"
        ).innerHTML =
            "Please enter a valid target price.";

        return;

    }


    targetPrice = value;


    document.getElementById(
        "alert-message"
    ).innerHTML =
        "🔔 Alert set at $" +
        value.toFixed(2);

}


function clearAlert() {

    targetPrice = null;


    document.getElementById(
        "target-price"
    ).value = "";


    document.getElementById(
        "alert-message"
    ).innerHTML =
        "No alert configured.";

}


// =========================================================
// MOVING AVERAGE
// =========================================================

function movingAverage(
    values,
    period
) {

    const result = [];


    for (
        let i = 0;
        i < values.length;
        i++
    ) {

        if (
            i < period - 1
        ) {

            result.push(null);

            continue;

        }


        let sum = 0;


        for (
            let j = i - period + 1;
            j <= i;
            j++
        ) {

            sum += values[j];

        }


        result.push(
            sum / period
        );

    }


    return result;

}


// =========================================================
// VOLATILITY
// =========================================================

function calculateVolatility(
    closes
) {

    if (
        closes.length < 2
    ) {

        return 0;

    }


    const returns = [];


    for (
        let i = 1;
        i < closes.length;
        i++
    ) {

        const r =
            (
                closes[i] -
                closes[i - 1]
            ) /
            closes[i - 1];


        returns.push(r);

    }


    const mean =
        returns.reduce(
            (a, b) => a + b,
            0
        ) /
        returns.length;


    const variance =
        returns.reduce(
            (sum, value) =>
                sum +
                Math.pow(
                    value - mean,
                    2
                ),
            0
        ) /
        returns.length;


    return Math.sqrt(
        variance
    ) * 100;

}


// =========================================================
// UPDATE DASHBOARD
// =========================================================

async function updateDashboard() {

    try {

        const response =
            await fetch(API_URL);


        if (!response.ok) {

            throw new Error(
                "API request failed"
            );

        }


        const data =
            await response.json();


        const bars =
            data.bars;


        if (
            !bars ||
            bars.length === 0
        ) {

            throw new Error(
                "No market data received"
            );

        }


        // =================================================
        // PREPARE DATA
        // =================================================

        const times = [];

        const opens = [];

        const highs = [];

        const lows = [];

        const closes = [];


        bars.forEach(
            bar => {

                times.push(
                    bar.openTime
                );

                opens.push(
                    Number(bar.open)
                );

                highs.push(
                    Number(bar.high)
                );

                lows.push(
                    Number(bar.low)
                );

                closes.push(
                    Number(bar.close)
                );

            }
        );


        // =================================================
        // CURRENT PRICE
        // =================================================

        const currentPrice =
            closes[
                closes.length - 1
            ];


        const previousPrice =
            closes[
                closes.length - 2
            ];


        const change =
            currentPrice -
            previousPrice;


        const changePercent =
            (
                change /
                previousPrice
            ) * 100;


        // =================================================
        // HIGH / LOW
        // =================================================

        const periodHigh =
            Math.max(...highs);


        const periodLow =
            Math.min(...lows);


        // =================================================
        // MOVING AVERAGES
        // =================================================

        const ma5 =
            movingAverage(
                closes,
                5
            );


        const ma10 =
            movingAverage(
                closes,
                10
            );


        const latestMA5 =
            ma5[
                ma5.length - 1
            ];


        const latestMA10 =
            ma10[
                ma10.length - 1
            ];


        // =================================================
        // TREND
        // =================================================

        let trend = "Neutral";


        if (
            latestMA5 >
            latestMA10
        ) {

            trend =
                "🟢 Uptrend";

        }
        else if (
            latestMA5 <
            latestMA10
        ) {

            trend =
                "🔴 Downtrend";

        }
        else {

            trend =
                "🟡 Neutral";

        }


        // =================================================
        // VOLATILITY
        // =================================================

        const volatility =
            calculateVolatility(
                closes
            );


        // =================================================
        // UPDATE METRICS
        // =================================================

        document.getElementById(
            "current-price"
        ).innerHTML =
            "$" +
            currentPrice.toFixed(2);


        document.getElementById(
            "price-change"
        ).innerHTML =
            "$" +
            change.toFixed(2);


        document.getElementById(
            "price-percent"
        ).innerHTML =
            changePercent.toFixed(2) +
            "%";


        document.getElementById(
            "period-high"
        ).innerHTML =
            "$" +
            periodHigh.toFixed(2);


        document.getElementById(
            "period-low"
        ).innerHTML =
            "$" +
            periodLow.toFixed(2);


        document.getElementById(
            "ma5"
        ).innerHTML =
            latestMA5
                ? "$" +
                  latestMA5.toFixed(2)
                : "--";


        document.getElementById(
            "ma10"
        ).innerHTML =
            latestMA10
                ? "$" +
                  latestMA10.toFixed(2)
                : "--";


        document.getElementById(
            "trend"
        ).innerHTML =
            trend;


        document.getElementById(
            "volatility"
        ).innerHTML =
            volatility.toFixed(3) +
            "%";


        // =================================================
        // STATUS
        // =================================================

        document.getElementById(
            "api-status"
        ).innerHTML =
            "API: Connected";


        document.getElementById(
            "update-time"
        ).innerHTML =
            new Date()
                .toLocaleTimeString();


        // =================================================
        // PRICE ALERT
        // =================================================

        if (
            targetPrice !== null
        ) {

            if (
                currentPrice >=
                targetPrice
            ) {

                document.getElementById(
                    "alert-message"
                ).innerHTML =
                    "🔔 PRICE ALERT: XAU/USD has reached $" +
                    currentPrice.toFixed(2);

            }
            else {

                document.getElementById(
                    "alert-message"
                ).innerHTML =
                    "Target: $" +
                    targetPrice.toFixed(2) +
                    " | Current: $" +
                    currentPrice.toFixed(2);

            }

        }


        // =================================================
        // CHART DATA
        // =================================================

        const candleTrace = {

            x: times,

            open: opens,

            high: highs,

            low: lows,

            close: closes,

            type: "candlestick",

            name: "XAU/USD"

        };


        const ma5Trace = {

            x: times,

            y: ma5,

            type: "scatter",

            mode: "lines",

            name: "MA5",

            line: {
                width: 2
            }

        };


        const ma10Trace = {

            x: times,

            y: ma10,

            type: "scatter",

            mode: "lines",

            name: "MA10",

            line: {
                width: 2
            }

        };


        // =================================================
        // CHART LAYOUT
        // =================================================

        const layout = {

            title:
                "XAU/USD Real-Time Price",

            xaxis: {

                title: "Time",

                rangeslider: {
                    visible: false
                }

            },

            yaxis: {

                title:
                    "Price (USD)"

            },

            height: 600,

            margin: {

                l: 60,

                r: 30,

                t: 60,

                b: 50

            },

            legend: {

                orientation: "h",

                y: 1.05

            }

        };


        // =================================================
        // UPDATE PLOT
        // =================================================

        const chart =
            document.getElementById(
                "chart"
            );


        if (
            !chartInitialized
        ) {

            Plotly.newPlot(

                chart,

                [
                    candleTrace,
                    ma5Trace,
                    ma10Trace
                ],

                layout,

                {
                    responsive: true,
                    displaylogo: false
                }

            );


            chartInitialized = true;

        }
        else {

            Plotly.react(

                chart,

                [
                    candleTrace,
                    ma5Trace,
                    ma10Trace
                ],

                layout,

                {
                    responsive: true,
                    displaylogo: false
                }

            );

        }


    }
    catch (error) {

        document.getElementById(
            "api-status"
        ).innerHTML =
            "API: Error";


        console.error(error);

    }

}


// =========================================================
// INITIAL LOAD
// =========================================================

updateDashboard();


// =========================================================
// REAL-TIME UPDATE
// =========================================================

setInterval(
    updateDashboard,
    3000
);

</script>

</body>

</html>
"""


# =========================================================
# RENDER HTML / JAVASCRIPT
# =========================================================

components.html(
    html_code,
    height=1250,
    scrolling=False
)


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "Data Source: BiQuote API | "
    "Symbol: XAU/USD | "
    "OHLC Interval: 1 minute | "
    "Dashboard Update: every 3 seconds"
)
