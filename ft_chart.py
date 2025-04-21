import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("The dollar usually moves in lockstep with US yields... until ‘liberation day’")

# === Load Merged Data ===
df = pd.read_csv("dgs10_usdindex_merged.csv")
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# === Sidebar inputs ===
st.sidebar.header("Customize the plot")

# Date range selector
start_date = pd.to_datetime(st.sidebar.date_input("Start date", df.index.min().date()))
end_date = pd.to_datetime(st.sidebar.date_input("End date", df.index.max().date()))

# Checkbox filters
show_usd = st.sidebar.checkbox("Show US Dollar Index", value=True)
show_yield = st.sidebar.checkbox("Show 10-Year US Yield", value=True)
show_lib_day = st.sidebar.checkbox("Mark Liberation Day (April 2, 2025)", value=True)

# Filter data
df_filtered = df.loc[start_date:end_date]

# === Plot ===
fig, ax1 = plt.subplots(figsize=(10, 6))

# US Dollar Index
if show_usd:
    ax1.plot(df_filtered.index, df_filtered['US_Dollar_Index'], color='crimson', label='US Dollar index')
    ax1.set_ylabel("US Dollar index", color='crimson')
    ax1.tick_params(axis='y', labelcolor='crimson')

# 10-Year Yield
if show_yield:
    ax2 = ax1.twinx()
    ax2.plot(df_filtered.index, df_filtered['10Y_US_Yield'], color='navy', label='10-year US yield (%)')
    ax2.set_ylabel("10-year US yield (%)", color='navy')
    ax2.tick_params(axis='y', labelcolor='navy')

# Liberation day line
if show_lib_day:
    liberation_day = pd.to_datetime("2025-04-02")
    if liberation_day >= start_date and liberation_day <= end_date:
        ax1.axvline(liberation_day, color='gray', linestyle='dotted')
        if show_usd:
            y_pos = ax1.get_ylim()[1] * 0.98
            ax = ax1
        elif show_yield:
            y_pos = ax2.get_ylim()[1] * 0.98
            ax = ax2
        else:
            y_pos = 1  # fallback value if neither is shown
            ax = ax1

    # Place the label
    ax.text(liberation_day, y_pos, 'Liberation Day', rotation=90, color='gray', fontsize=9)

# Title and layout
fig.tight_layout()
st.pyplot(fig)