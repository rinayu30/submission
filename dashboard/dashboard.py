#import library yang dibutuhkan

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#membuat fungsi untuk dataframe
def create_station_df(df):
    station_df = df.groupby("station").aqi.sum().sort_values(ascending=False).reset_index()
    return station_df

def create_count_df(df):
    count_df = df.groupby(by="station").air_quality.value_counts().reset_index(name="count")
    return count_df

def create_df_time(df):
    df_time = df
    return df_time

#mengambil dataset
aq_df = pd.read_csv("aq_df.csv")
aq_df.sort_values(by="datetime")
aq_df.reset_index(inplace=True)
aq_df["datetime"] = pd.to_datetime(aq_df["datetime"])

#filtering data by datetime
min_date = aq_df["datetime"].min()
max_date = aq_df["datetime"].max()

#membuat dashboard bagiann sidebar
with st.sidebar:
    st.image("https://static.vecteezy.com/system/resources/previews/008/996/254/original/aqi-logo-aqi-letter-aqi-letter-logo-design-initials-aqi-logo-linked-with-circle-and-uppercase-monogram-logo-aqi-typography-for-technology-business-and-real-estate-brand-vector.jpg")
    
    #Membuat start_date dan end_date dari inputan date
    start_date, end_date = st.date_input(
        label="Range Time",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = aq_df[(aq_df["datetime"] >= str(start_date)) &
                (aq_df["datetime"] <= str(end_date))]

station_df = create_station_df(main_df)
count_df = create_count_df(main_df)
time_df = create_df_time(main_df)

#membuat header dashboard
st.header('Air Quality Index Dashboard :cloud:')

st.subheader(' Air Quality Count by Station')

# Membuat list yang berisi kelipatan 5000 dari 0 sampai 30000
yticks = [x for x in range(0, 30001, 5000)]

fig, ax = plt.subplots(figsize=(30, 15))
sns.lineplot(
    x='station',
    y='count',
    data=count_df,
    hue='air_quality',
    linewidth=4 #mengubah ukuran line pada diagram
    )
ax.set_yticks(yticks)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=25)
 
st.pyplot(fig)

#membuat AQI berdasarkan ketentuan waktu
st.subheader("Air Quality Index by Variable Time")

col1, col2, col3, col4= st.columns(4)

with col1:
    max_year = time_df.groupby(by= "year").aqi.sum().idxmax()
    st.metric("Best Year", value=max_year)

with col2:
    max_month= time_df.groupby(by= "month").aqi.sum().idxmax()
    st.metric("Best Month", value=max_month)

with col3:
    max_day = time_df.groupby(by= "day").aqi.sum().idxmax()
    st.metric("Best Day", value=max_day)

with col4:
    max_hour = time_df.groupby(by= "hour").aqi.sum().idxmax()
    st.metric("Best Hour", value=max_hour)

#membuat list untuk label attribute visualisasi
label_var=["year", "month", "day", "hour"] 

# Membuat subplot grid
fig, ax= plt.subplots(nrows= 2, ncols= int(len(label_var)/2), figsize= (40,15))

# Looping untuk mengisi subplot grid dengan plots
l= 0
for i in range(2):
    for j in range(int(len(label_var)/2)):
        sns.barplot(y= time_df.groupby(by= label_var[l]).aqi.sum(),
                    x= time_df.groupby(by= label_var[l]).mean(numeric_only=True).index, ax= ax[i,j], palette= 'viridis')

        ax[i,j].set_title(f'{label_var[l].upper()}', fontsize= 30)
        ax[i,j].set_ylabel('')
        ax[i,j].set_xlabel('')
        ax[i,j].tick_params(axis='y', labelsize=30)
        ax[i,j].tick_params(axis='x', labelsize=25)
        plt.xticks(rotation=315)
        l+=1

st.pyplot(fig)

# membuat diagram AQI terburuk dan terbaik period 2013-2017
st.subheader("Best & Worst Air Quality Index (AQI)")

# membuat 2 kanvas untuk visualisasi data best & worst air quality by station
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))

#memberi warna bar
colors1 = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors2 = ["#E32925", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

#membuat diagram bar dengan inisialisasi ax[0]
sns.barplot(x="aqi", y="station", data=station_df.head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Air Quality Index (AQI)", loc="center", fontsize=25)
ax[0].tick_params(axis ='y', labelsize=20)
ax[0].tick_params(axis ='x', labelsize=20)

#membuat diagram bar dengan inisialisasi ax[1] 
sns.barplot(x="aqi", y="station", data=station_df.sort_values(by="aqi", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Air Quality Index (AQI)", loc="center", fontsize=25)
ax[1].tick_params(axis ='y', labelsize=20)
ax[1].tick_params(axis ='x', labelsize=20)
 
st.pyplot(fig)
