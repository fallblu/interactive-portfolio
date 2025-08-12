from __future__ import annotations

import datetime as dt

import matplotlib
import mplfinance as mpf
import pandas as pd
import streamlit as st
import yfinance as yf

matplotlib.use("Agg")

st.set_page_config(page_title="Time Series Plotter", page_icon="📈", layout="centered")
my_style = mpf.make_mpf_style(base_mpf_style="mike", rc={"axes.labelsize": "medium"})

if "loaded_time_series" not in st.session_state:
    st.session_state.loaded_time_series = []
if "loaded_time_series_names" not in st.session_state:
    st.session_state.loaded_time_series_names = []
if "time_series_log" not in st.session_state:
    st.session_state.time_series_log = pd.DataFrame(
        {"Time Retrieved": [], "Ticker": [], "Interval": [], "Start": [], "End": []}
    )

ticker_col, interval_col, start_col, end_col = st.columns(4, vertical_alignment="top")

ticker = ticker_col.text_input("Ticker", key="ticker_input")
interval = interval_col.selectbox(
    "Interval", options=["1d", "5d", "1wk", "1mo", "3mo"], index=0, key="interval_input"
)
start = start_col.date_input("Start date", value=dt.date(2020, 1, 1), key="start_input")
end = end_col.date_input("End date", value=dt.date.today(), key="end_input")


@st.cache_data(show_spinner=False)
def fetch_history(ticker: str, start: dt.date, end: dt.date, interval: str) -> pd.DataFrame:
    t = yf.Ticker(ticker)
    df = t.history(start=start, end=end, interval=interval)
    if not df.empty:
        df.index = pd.to_datetime(df.index)
        keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
        df = df[keep]
    return df


if st.button("Retrieve Price Data", type="primary"):
    if not ticker:
        st.info("Enter a ticker first.")
    else:
        df = fetch_history(ticker, start, end, interval)
        if df.empty:
            st.warning("No data returned for that request.")
        else:
            name = f"{ticker.upper()} | {interval} | {start:%Y/%m/%d}–{end:%Y/%m/%d}"
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

st.dataframe(st.session_state.time_series_log, use_container_width=True)

if st.session_state.loaded_time_series:
    idx = st.selectbox(
        "Select a time series to plot",
        options=range(len(st.session_state.loaded_time_series)),
        format_func=lambda i: st.session_state.loaded_time_series_names[i],
        key="series_select",
    )
    df = st.session_state.loaded_time_series[idx]

    fig = mpf.figure(style=my_style, facecolor=(15.0 / 255.0, 17.0 / 255.0, 23.0 / 255.0))
    gs = matplotlib.gridspec.GridSpec(ncols=1, nrows=2, height_ratios=[5, 2])
    ax_price = fig.add_subplot(gs[0])
    ax_vol = fig.add_subplot(gs[1])
    mpf.plot(df, ax=ax_price, volume=ax_vol)
    ax_price.set_xticklabels(labels=[])
    ax_vol.yaxis.tick_right()
    ax_vol.yaxis.set_label_position("right")
    st.pyplot(fig)
else:
    st.info("No time series loaded yet.")
