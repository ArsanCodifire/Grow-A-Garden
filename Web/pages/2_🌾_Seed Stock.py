import streamlit as st
import httpx
from rarity import rarity_data
import os

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
API_URL = "https://gagapi.onrender.com/seeds"

st.title("🌾 Seed Stock")

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
                icon_path = os.path.join(IMG_FOLDER, rarity_icon)
                if os.path.isfile(icon_path):
                    st.image(icon_path, width=30)
                else:
                    st.write("❓")
        with cols[1]:
            st.write(name)
        with cols[2]:
            st.write(rarity_name)
        with cols[3]:
            st.write(f"{sheckle_cost} Sheckles | Stock: {qty}")

except Exception as e:
    st.error(f"Failed to fetch Seed Stock: {e}")