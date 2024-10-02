# +================================================================+
# +          CREATE DASHBOARD BIKE SHARING USING STREAMLIT         +
# +          ---------------------------------------------         +
# + Nama          : Kevin Arya Swardhana                           +
# + Email         : kevinaryastarigan@gmail.com                    +
# + Id Dicoding   : dicoding.com/users/kevinaryaswardhana/         +
# + Created       : 14 Juni 2024 (RENEW) 01 Oktober 2024           +
# +================================================================+

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os

# +---------------+
# +   LOAD DATA   +
# +---------------+
@st.cache_data
def load_data():
    df_day = pd.read_csv("path_to_day.csv")
    df_hour = pd.read_csv("path_to_hour.csv")
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    return df_day, df_hour

df_day, df_hour = load_data()

# +---------------------+
# +   TITLE DASHBOARD   +
# +---------------------+
st.title("Bike Share Dashboard")

# +-------------+
# +   SIDEBAR   +
# +-------------+
st.sidebar.title("Filters")

# Choose between daily or hourly data
data_choice = st.sidebar.radio("Select Data Type", ("Daily", "Hourly"))

if data_choice == "Daily":
    data = df_day
else:
    data = df_hour

# Select season or weather filter
filter_choice = st.sidebar.radio("Filter by", ("Season", "Weather"))

# Sidebar: Filter by season
if filter_choice == "Season":
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    data["season_label"] = data["season"].map(season_mapping)
    selected_season = st.sidebar.multiselect("Choose Season", data["season_label"].unique(), default=data["season_label"].unique())
    filtered_data = data[data["season_label"].isin(selected_season)]
else:
    # Sidebar: Filter by weather situation
    weather_mapping = {
        1: "Clear, Few clouds", 
        2: "Mist + Cloudy", 
        3: "Light Snow, Light Rain", 
        4: "Heavy Rain + Thunderstorm"
    }
    data["weather_label"] = data["weathersit"].map(weather_mapping)
    selected_weather = st.sidebar.multiselect("Choose Weather", data["weather_label"].unique(), default=data["weather_label"].unique())
    filtered_data = data[data["weather_label"].isin(selected_weather)]

# Sidebar Personal Info
st.sidebar.title("Personal Information")
st.sidebar.markdown("""
**• Nama: Kevin Arya Swardhana**  
**• Email: [kevinaryastarigan@gmail.com](mailto:kevinaryastarigan@gmail.com)**  
**• Dicoding: [kevinaryaswardhana](https://www.dicoding.com/users/kevinaryaswardhana/)**  
**• LinkedIn: [Kevin Arya Swardhana](https://www.linkedin.com/in/kevinaryaswardhana/)**  
""")

# +-------------------+
# +   VISUALIZATION   +
# +-------------------+
st.header("Visualizations")

# Create layout with three columns
col1, col2, col3 = st.columns(3)

# Column 1: Bike count by season/weather
with col1:
    if filter_choice == "Season":
        season_count = filtered_data.groupby("season_label")["cnt"].sum().reset_index()
        fig_season_go = go.Figure(data=[
            go.Bar(name='Bike Rentals', x=season_count["season_label"], y=season_count["cnt"], marker_color='indigo')
        ])
        fig_season_go.update_layout(title="Bike Rentals by Season", xaxis_title="Season", yaxis_title="Total Rentals", template="plotly_white")
        st.plotly_chart(fig_season_go, use_container_width=True)
    else:
        weather_count = filtered_data.groupby("weather_label")["cnt"].sum().reset_index()
        fig_weather_go = go.Figure(data=[
            go.Bar(name='Bike Rentals', x=weather_count["weather_label"], y=weather_count["cnt"], marker_color='orange')
        ])
        fig_weather_go.update_layout(title="Bike Rentals by Weather", xaxis_title="Weather", yaxis_title="Total Rentals", template="plotly_white")
        st.plotly_chart(fig_weather_go, use_container_width=True)

# Column 2: Bike rentals by hour or day
with col2:
    if data_choice == "Hourly":
        hourly_count = filtered_data.groupby("hr")["cnt"].sum().reset_index()
        fig_hour_go = go.Figure()
        fig_hour_go.add_trace(go.Scatter(x=hourly_count["hr"], y=hourly_count["cnt"], mode='lines+markers', name='Hourly Rentals', line=dict(color='royalorange')))
        fig_hour_go.update_layout(title="Hourly Bike Rentals", xaxis_title="Hour", yaxis_title="Total Rentals", template="plotly_white")
        st.plotly_chart(fig_hour_go, use_container_width=True)
    else:
        daily_count = filtered_data.groupby("dteday")["cnt"].sum().reset_index()
        fig_day_go = go.Figure()
        fig_day_go.add_trace(go.Scatter(x=daily_count["dteday"], y=daily_count["cnt"], mode='lines+markers', name='Daily Rentals', line=dict(color='green')))
        fig_day_go.update_layout(title="Daily Bike Rentals", xaxis_title="Date", yaxis_title="Total Rentals", template="plotly_white")
        st.plotly_chart(fig_day_go, use_container_width=True)

# Column 3: Binning (Cluster Analysis)
with col3:
    bins = [0, 100, 300, 500, 1000]
    labels = ['Low', 'Medium', 'High', 'Very High']
    filtered_data['Rentals_Binned'] = pd.cut(filtered_data['cnt'], bins=bins, labels=labels)
    binned_count = filtered_data['Rentals_Binned'].value_counts().reset_index()
    binned_count.columns = ['Rental Category', 'Total']

    fig_binned_go = go.Figure(data=[
        go.Bar(name='Bike Rentals', x=binned_count['Rental Category'], y=binned_count['Total'], marker_color='crimson')
    ])
    fig_binned_go.update_layout(title='Clustered Bike Rentals', xaxis_title='Rental Category', yaxis_title='Total', template="plotly_white")
    st.plotly_chart(fig_binned_go, use_container_width=True)

# Show data
if st.sidebar.checkbox("Show Dataset"):
    st.write(filtered_data)
