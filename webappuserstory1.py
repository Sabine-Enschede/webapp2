import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.title("Numbers of reviews per city in 2023")

DB_USER = "deliverable_taskforce"
DB_PASSWORD = "learn_sql_2024"
DB_HOSTNAME = "training.postgres.database.azure.com"
DB_NAME = "deliverable"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:5432/{DB_NAME}")

df = pd.read_sql_query(
    """
    select r2.location_city as location, r.datetime::date as "date", count(r.datetime::date) as "number of reviews"
        from reviews r
        inner join restaurants r2 on r.restaurant_id = r2.restaurant_id
        where (r2.location_city like 'Groningen'
            or r2.location_city like 'Rotterdam'
            or r2.location_city like 'Amsterdam')
            and r.datetime > '2023-01-01' and r.datetime < '2024-01-01'
        group by "date", location
    """,
    con=engine,
)

minvalue = df["date"].min()
maxvalue = df["date"].max()
mindate, maxdate = st.sidebar.slider(
    "Select time window", min_value=minvalue, max_value=maxvalue, value=(minvalue, maxvalue)
)
df_new = df[(df["date"] >= mindate) & (df["date"] <= maxdate)]

avg = df_new.groupby(["location"])["number of reviews"].mean().round(0)
avg = avg.to_frame()
avg.columns = ["Average number of reviews per day"]

if st.checkbox("Show average"):
    st.write(avg)
    barchart = st.bar_chart(data=avg, y="Average number of reviews per day")
else:
    st.write(df_new)
    barchart = st.bar_chart(data=df_new, x="location", y="number of reviews")

chart = st.line_chart(data=df_new, x="date", y="number of reviews", color="location")
