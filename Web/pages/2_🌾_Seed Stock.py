import streamlit as st
import httpx
import os
from order import SEED_ORDER
from rarity import rarity_data

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
API_URL = "https://gagapi.onrender.com/seeds"

st.title("🌾 Seed Stock")

try:
    with httpx.Client(timeout=10) as client:
        data = client.get(API_URL).json()

    # Debug: show the raw API data
    st.subheader("Debug: API Response")
    st.write(data)

    # Force data into a list of dicts
    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, str):
        st.error("API returned a string, not JSON list/dict.")
        st.stop()

    data = [x for x in data if isinstance(x, dict)]

    # Debug: show cleaned data
    st.subheader("Debug: Cleaned Data")
    st.write(data)

    # Sort according to SEED_ORDER
    data.sort(key=lambda x: SEED_ORDER.index(x["name"]) if x["name"] in SEED_ORDER else 999)

    # Render seeds
    for item in data:
        name = item.get("name", "Unknown")
        qty = item.get("quantity", 0)
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))

        cols_top = st.columns([1, 4, 1])
        with cols_top[0]:
            seed_img = os.path.join(IMG_FOLDER, f"{name}.png")
            if os.path.exists(seed_img):
                st.image(seed_img, width=100)
            else:
                st.write("No Img")
        with cols_top[1]:
            st.write(name)
        with cols_top[2]:
            if rarity_icon:
                rarity_img = os.path.join(IMG_FOLDER, rarity_icon)
                if os.path.exists(rarity_img):
                    st.image(rarity_img, width=100)
                else:
                    st.write(rarity_name)
            else:
                st.write(rarity_name)

        cols_bottom = st.columns([1, 1])
        with cols_bottom[0]:
            st.write(f"Stock: {qty}")
        with cols_bottom[1]:
            st.write(f"Cost: {sheckle_cost} Sheckles")

        st.markdown("---")

except Exception as e:
    st.error(f"Failed to fetch Seed Stock: {e}")