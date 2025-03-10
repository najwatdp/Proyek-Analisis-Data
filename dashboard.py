import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_df(df):
    daily_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_df = daily_df.reset_index()
    daily_df.rename(columns={
        "cnt": "daily_cnt"
    }, inplace=True)
    return daily_df

def create_season_df(df):
    season_df = df.groupby(by="season").cnt.sum().reset_index()
    season_df.rename(columns={
        "cnt": "total_rent"
    }, inplace=True)
    return season_df

def create_bytemp_df(df):
    bytemp_df = df.groupby(by="temp_group").cnt.sum().reset_index()
    bytemp_df.rename(columns={
        "cnt": "total_cnt"
    }, inplace=True)
    return bytemp_df

def create_workingday_df(df):
    workingday_df = df.groupby(by="workingday").cnt.sum().reset_index()
    workingday_df.rename(columns={
        "cnt": "total_rent"
    }, inplace=True)
    return workingday_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://st2.depositphotos.com/40527348/44435/v/450/depositphotos_444356130-stock-illustration-bicycle-rental-icons-set-logo.jpg")
   
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_df = create_daily_df(main_df)
season_df = create_season_df(main_df)
bytemp_df = create_bytemp_df(main_df)
workingday_df = create_workingday_df(main_df)

st.header('Bike Sharing Dashboard :sparkle:')

st.subheader('Daily Rent')

col1, col2 = st.columns(2)
 
with col1:
    total_rent = daily_df.daily_cnt.sum()
    st.metric("Total Rent", value=total_rent)
 
with col2:
    avg_rent = daily_df.daily_cnt.mean() 
    st.metric("Average Rent", value=avg_rent)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_df["dteday"],
    daily_df["daily_cnt"],
    marker='o', 
    linewidth=2,
    color="#FF7F00"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)
 
st.pyplot(fig)

st.subheader("Total Rent by Season")

fig, ax = plt.subplots(figsize=(35, 15))
 
colors = ["#FF7F00", "#FABE97", "#FABE97", "#FABE97"]
 
sns.barplot(x="total_rent", y="season", data=season_df, palette=colors)
ax.set_ylabel(None)
ax.set_xlabel("Number of Rent", fontsize=40)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Total Rent by Temperature")

fig, ax = plt.subplots(figsize=(35, 15))
 
colors = ["#FABE97", "#FABE97", "#FABE97", "#FF7F00"]
 
sns.barplot(x="temp_group", y="total_cnt", data=bytemp_df, palette=colors)
ax.set_xlabel(None)
ax.set_ylabel("Number of Rent", fontsize=40)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Total Rent by Type of Day")

fig, ax = plt.subplots(figsize=(35, 15))
 
colors = ["#FF7F00", "#FABE97"]
 
sns.barplot(x="workingday", y="total_rent", data=workingday_df, palette=colors)
ax.set_xlabel(None)
ax.set_ylabel("Number of Rent", fontsize=40)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.caption('Copyright (c) Bike Rent 2012')