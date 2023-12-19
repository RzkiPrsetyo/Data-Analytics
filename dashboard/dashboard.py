import pandas as pd
import streamlit as st
import plotly.express as px

my_df = pd.read_csv('https://raw.githubusercontent.com/RzkiPrsetyo/Data-Analytics/main/dashboard/main_data.csv')
df = my_df[['year', 'month', 'day','hour','PM2.5','PM10','CO','O3','TEMP','PRES','DEWP','station']]
df['date'] = df['day'].astype(str) + '/' + df['month'].astype(str) + '/' + df['year'].astype(str)

st.set_page_config(page_title="Air Quality Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")


# ----- SIDEBAR ------
# st.sidebar.image("https://hlassets.paessler.com/common/files/graphics/iot/sub-visual_iot-monitoring_air-quality-monitoring-v1.png")

st.sidebar.header("Filter:")
st_filter = st.sidebar.multiselect(
    "Station:",
    options=df["station"].unique(),
    default=df["station"].unique()
)

year_filter = st.sidebar.multiselect(
    "Year:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

temp_filter = st.sidebar.slider(
    "Temperature °C:",
    min_value=df["TEMP"].min(),  
    max_value=df["TEMP"].max(), 
)

df_selection = df.query(
    "station == @st_filter & year == @year_filter & TEMP >= @temp_filter"
)

# ----- MAINPAGE -----
st.title(":bar_chart: Air Quality Dashboard")
st.markdown("##")

day_count = df_selection["date"].nunique()
average_temp = round(df_selection["TEMP"].mean(), 1)
average_pres = round(df_selection["PRES"].mean(), 2)

left_column, mid_column, mid2_column, right_column = st.columns(4)
with left_column:
    st.subheader("Days in Total:")
    st.subheader(day_count)
with mid_column:
    st.subheader("Average Temp °C:")
    st.subheader(average_temp)
with mid2_column:
    st.subheader("Average Pressure:")
    st.subheader(average_pres)
with right_column:
    st.subheader("PM2.5/PM10/CO:")
    st.subheader("50/60/700⚠️")

st.markdown("---")

# ----- CHART -----
grouped = df_selection.groupby(['year', 'station'])[['PM2.5', 'PM10', 'CO','O3']].mean().reset_index()
fig = px.line(grouped, x="year", y="PM2.5", color="station", markers=True, title='Average PM2.5 Particles').update_layout(xaxis_title="Year", yaxis_title="PM2.5 (μg/m³)")
#st.plotly_chart(fig)

fig2 = px.line(grouped, x="year", y="PM10", color="station", markers=True, title='Average PM10 Particles').update_layout(xaxis_title="Year", yaxis_title="PM10 (μg/m³)")

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig3 = px.line(grouped, x="year", y="CO", color="station", markers=True, title='Average CO (Carbon Monoxide)').update_layout(xaxis_title="Year", yaxis_title="Carbon Monoxide (μg/m³)")
#st.plotly_chart(fig3)

fig4 = px.bar(grouped, x='year', y='O3', color="station", title='Average O3 (Ozon)').update_layout(xaxis_title="Year", yaxis_title="Ozon (DU)", width=520)

# image_url = 'https://www.howardluksmd.com/wp-content/uploads/2021/11/AQi-PM-2.5-levels-health-effects.jpeg'

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig3, use_container_width=True)
right_column.plotly_chart(fig4, use_column_width=True)

st.write(
    """
    <div style='text-align:center;'>
        <h5>The higher values of PM2.5, PM10, CO, and O3, the worse air quality.</h5>
    </div>
    """,
    unsafe_allow_html=True
)
st.image(image_url, use_column_width=True)

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
