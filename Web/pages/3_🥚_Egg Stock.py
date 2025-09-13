import streamlit as st
import httpx
from rarity import rarity_data
import os

IMG_FOLDER = "Web/images"
API_URL = "https://gagapi.onrender.com/eggs"

st.title("🥚 Egg Stock")

try:
    with httpx.Client(timeout=10) as client:
        data = client.get(API_URL).json()

    for item in data:
        name = item["name"]
        qty = item.get("quantity", 0)
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))

        cols = st.columns([1, 3, 2, 2])
        with cols[0]:
            if rarity_icon:
                st.image(os.path.join(IMG_FOLDER, rarity_icon), width=30)
        with cols[1]:
            st.write(name)
        with cols[2]:
            st.write(rarity_name)
        with cols[3]:
            st.write(f"{sheckle_cost} Sheckles | Stock: {qty}")

except Exception as e:
    st.error(f"Failed to fetch Egg Stock: {e}")