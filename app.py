import streamlit as st
import pandas as pd
from preprocessing import preprocess_data

df = preprocess_data("data/zomato.csv")

st.set_page_config(page_title="Restaurant Recommender", layout="centered")

st.title("🍽️ Knowledge-Based Restaurant Recommender")
st.markdown("Select your preferences and get top restaurant recommendations.")


cuisine = st.selectbox("Preferred Cuisine", sorted(df["primary_cuisine"].unique()))
price = st.selectbox("Price Range", sorted(df["price_range"].unique()))
location = st.selectbox("Location", sorted(df["locality"].unique()))


if st.button("Get Recommendations"):
    filtered = df[
        (df["primary_cuisine"] == cuisine)
        & (df["price_range"] == price)
        & (df["locality"] == location)
    ]

    if not filtered.empty:
        st.success(f"Found {len(filtered)} matching restaurant(s).")
        for _, row in filtered.iterrows():
            st.subheader(row["restaurant_name"])
            st.write(f"📍 Location: {row['locality'].title()}")
            st.write(f"💰 Price: {row['price_range'].title()}")
            st.write("---")
    else:
        st.warning("No restaurants matched your preferences.")

    feedback = st.slider("How satisfied are you with the results?", 1, 5)
    st.text(f"Thanks! You rated us: {feedback}/5")
