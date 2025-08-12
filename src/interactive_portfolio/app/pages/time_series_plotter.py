from __future__ import annotations

import datetime as dt

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# Page layout: wide + no page scroll, large centered chart
st.set_page_config(page_title="Time Series Plotter", page_icon="📈", layout="wide")
st.markdown(
    """
    <style>
      /* Lock app to viewport height and prevent scrolling */
      html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        height: 100vh !important; overflow: hidden !important;
      }
      /* So the canvas uses the screen well */
      .block-container { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
# Tighten spacing beneath widgets and style our custom under-labels
st.markdown(
    """
<style>
/* Reduce extra space under all Streamlit widgets */
[data-testid="stWidget"] { margin-bottom: 0.25rem !important; }
/* Compact label that sits right under the widget */
.underlabel { margin-top: 0.rem; font-size: 0.85rem; opacity: 0.75; }
</style>
""",
    unsafe_allow_html=True,
)


def underlabel(widget_fn, label, *args, **kwargs):
    kwargs.setdefault("label_visibility", "collapsed")
    val = widget_fn(label, *args, **kwargs)
    st.markdown(f'<div class="underlabel">{label}</div>', unsafe_allow_html=True)
    return val


# Session state
if "loaded_time_series" not in st.session_state:
    st.session_state.loaded_time_series = []
if "loaded_time_series_names" not in st.session_state:
    st.session_state.loaded_time_series_names = [""]
if "time_series_log" not in st.session_state:
    st.session_state.time_series_log = pd.DataFrame(
        {"Time Retrieved": [], "Ticker": [], "Interval": [], "Start": [], "End": []}
    )
if "line_style" not in st.session_state:
    st.session_state.line_style = "Candlestick"

st.divider()
_, settings_column = st.columns(spec=[0.75, 0.25])
popover_container = settings_column.container(horizontal=True)

with popover_container.popover("Retrieve Data", use_container_width=True):
    st.caption("Retrieval log")
    st.dataframe(st.session_state.time_series_log, use_container_width=True)

    c1, c2, c3, c4, c5 = st.columns(spec=[0.15, 0.2, 0.25, 0.25, 0.15], vertical_alignment="top")

    with c1:
        ticker = underlabel(st.text_input, "Ticker", key="ticker_input", placeholder="AAPL")
    with c2:
        interval = underlabel(
            st.selectbox,
            "Interval",
            options=["1d", "5d", "1wk", "1mo", "3mo"],
            key="interval_input",
        )
    with c3:
        start = underlabel(st.date_input, "Start", key="start_date")
    with c4:
        end = underlabel(st.date_input, "End", key="end_date")

    retrieve = c5.button(
        "Retrieve",
        type="primary",
        width="stretch",
    )

    @st.cache_data(show_spinner=False)
    def fetch_history(ticker: str, start: dt.date, end: dt.date, interval: str) -> pd.DataFrame:
        t = yf.Ticker(ticker)
        df = t.history(start=start, end=end, interval=interval)
        if not df.empty:
            df.index = pd.to_datetime(df.index)
            keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
            df = df[keep]
        return df

    if retrieve:
        if not ticker:
            st.info("Enter a ticker first.")
        else:
            df = fetch_history(ticker, start, end, interval)
            if df.empty:
                st.warning("No data returned for that request.")
            else:
                name = f"| {ticker.upper()} | {interval} | {start:%Y/%m/%d}–{end:%Y/%m/%d} |"
                st.session_state.loaded_time_series.append(df)
                st.session_state.loaded_time_series_names.append(name)
                st.session_state.time_series_log = pd.concat(
                    [
                        st.session_state.time_series_log,
                        pd.DataFrame(
                            {
                                "Time Retrieved": [dt.datetime.now()],
                                "Ticker": [ticker.upper()],
                                "Interval": [interval],
                                "Start": [start],
                                "End": [end],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
                st.success(f"Added {name}")


with popover_container.popover("Plot Time Series", use_container_width=True):
    # Selection & style controls moved here too
    if st.session_state.loaded_time_series:
        st.selectbox(
            "Select a time series to plot",
            options=range(len(st.session_state.loaded_time_series) + 1),
            format_func=lambda i: st.session_state.loaded_time_series_names[i],
            key="series_select",
        )
        st.radio(
            "Line Style",
            ["Candlestick", "OHLC"],
            key="line_style",
            horizontal=True,
        )


if st.session_state.loaded_time_series and st.session_state.get("series_select", 0) != 0:
    idx = st.session_state.get("series_select", 0) - 1
    idx = max(0, min(idx, len(st.session_state.loaded_time_series) - 1))
    df = st.session_state.loaded_time_series[idx]
    line_style = st.session_state.get("line_style", "Candlestick")

    try:
        fragment = st.fragment
    except AttributeError:

        def fragment(func):
            return func

    @fragment
    def render_chart(_df: pd.DataFrame, _style: str):
        trace_cls = {"Candlestick": go.Candlestick, "OHLC": go.Ohlc}[_style]
        trace = trace_cls(
            x=_df.index, open=_df["Open"], high=_df["High"], low=_df["Low"], close=_df["Close"]
        )

        fig = go.Figure(data=[trace])
        fig.update_layout(
            autosize=True,
            height=600,
            margin=dict(l=8, r=8, t=0, b=8),
            xaxis_rangeslider_visible=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    render_chart(df, line_style)
