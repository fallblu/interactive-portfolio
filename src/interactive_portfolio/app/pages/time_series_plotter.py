from __future__ import annotations

import datetime as dt
from collections.abc import Callable
from datetime import timezone
from typing import ParamSpec, TypeVar, cast

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

P = ParamSpec("P")
R = TypeVar("R")


def fragment(func: Callable[P, R]) -> Callable[P, R]:
    """
    Wrapper that uses st.fragment if available; otherwise a no-op.
    Preserves the signature of the wrapped function for type checkers.
    """
    st_fragment = getattr(st, "fragment", None)
    if st_fragment is None:
        return func
    # st.fragment is a decorator; cast it to the compatible callable type
    return cast(Callable[[Callable[P, R]], Callable[P, R]], st_fragment)(func)


# --- Minimal, safer CSS (avoid data-testid & global overflow locks) ---
st.markdown(
    """
    <style>
      .block-container { padding-top: 0.5rem; padding-bottom: 0.5rem; }
      .underlabel { margin-top: 0rem; font-size: 0.85rem; opacity: 0.75; }
    </style>
    """,
    unsafe_allow_html=True,
)


def underlabel(widget_fn, label, *args, **kwargs):
    kwargs.setdefault("label_visibility", "collapsed")
    val = widget_fn(label, *args, **kwargs)
    st.markdown(f'<div class="underlabel">{label}</div>', unsafe_allow_html=True)
    return val


# ---- Session state ----
ss = st.session_state
ss.setdefault("loaded_time_series", [])
ss.setdefault("loaded_time_series_names", ["None Selected"])
ss.setdefault(
    "time_series_log",
    pd.DataFrame({"Time Retrieved": [], "Ticker": [], "Interval": [], "Start": [], "End": []}),
)
ss.setdefault("line_style", "Candlestick")

st.divider()
_, retrieve_column, plot_settings_column = st.columns(spec=[0.5, 0.25, 0.25])

with retrieve_column.popover("Retrieve Data", use_container_width=True):
    st.caption("Retrieval log")
    st.dataframe(ss.time_series_log, use_container_width=True)

    c1, c2, c3, c4, c5 = st.columns(spec=[0.15, 0.2, 0.25, 0.25, 0.15], vertical_alignment="top")
    today = dt.date.today()
    default_start = today.replace(year=today.year - 1)

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
        start = underlabel(st.date_input, "Start", key="start_date", value=default_start)
    with c4:
        end = underlabel(st.date_input, "End", key="end_date", value=today)

    retrieve = c5.button("Retrieve", type="primary", use_container_width=True)

    @st.cache_data(ttl=3600, show_spinner=False)
    def fetch_history(ticker: str, start: dt.date, end: dt.date, interval: str) -> pd.DataFrame:
        t = yf.Ticker(ticker)
        df = t.history(start=start, end=end, interval=interval)
        if df is None or df.empty:
            return pd.DataFrame()
        df.index = pd.to_datetime(df.index)
        keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
        return df[keep]

    if retrieve:
        tkr = (ticker or "").strip().upper()
        if not tkr:
            st.info("Enter a ticker first.")
        elif start > end:
            st.error("Start date must be on or before End date.")
        else:
            try:
                df = fetch_history(tkr, start, end, interval)
            except Exception as e:
                st.error(f"Data request failed: {e}")
                df = pd.DataFrame()

            if df.empty:
                st.warning("No data returned for that request.")
            else:
                name = f"{tkr} | {interval} | {start:%Y/%m/%d}–{end:%Y/%m/%d}"
                ss.loaded_time_series.append(df)
                ss.loaded_time_series_names.append(name)
                ss.time_series_log = pd.concat(
                    [
                        ss.time_series_log,
                        pd.DataFrame(
                            {
                                "Time Retrieved": [dt.datetime.now(timezone.utc)],
                                "Ticker": [tkr],
                                "Interval": [interval],
                                "Start": [start],
                                "End": [end],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
                st.success(f"Added {name}")

with plot_settings_column.popover("Plot Time Series", use_container_width=True):
    if ss.loaded_time_series:
        st.selectbox(
            "Select a time series to plot",
            options=range(len(ss.loaded_time_series) + 1),
            format_func=lambda i: ss.loaded_time_series_names[i],
            key="series_select",
        )
        st.radio("Line Style", ["Candlestick", "OHLC"], key="line_style", horizontal=True)

if ss.loaded_time_series and ss.get("series_select", 0) != 0:
    idx = max(0, min(ss["series_select"] - 1, len(ss.loaded_time_series) - 1))
    df = ss.loaded_time_series[idx]
    line_style = ss.get("line_style", "Candlestick")

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
            hovermode="x unified",
            uirevision="keep-zoom",  # preserve zoom when toggling style
        )
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})

    render_chart(df, line_style)
