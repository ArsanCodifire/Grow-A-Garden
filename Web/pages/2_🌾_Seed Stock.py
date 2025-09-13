import streamlit as st
import httpx
import os
from order import SEED_ORDER
from rarity import rarity_data

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
API_URL = "https://gagapi.onrender.com/seed"

st.title("🌾 Seed Stock")

try:
    with httpx.Client(timeout=10) as client:
        data = client.get(API_URL).json()
        data.sort(key=lambda x: SEED_ORDER.index(x["name"]) if x["name"] in SEED_ORDER else 999)

    for item in data:
        name = item["name"]
        qty = item.get("quantity", 0)
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))

        cols_top = st.columns([1, 4, 1])
        with cols_top[0]:
            st.image(os.path.join(IMG_FOLDER, f"{name}.png"), width=40)
        with cols_top[1]:
            st.write(name)
        with cols_top[2]:
            if rarity_icon:
                st.image(os.path.join(IMG_FOLDER, rarity_icon), width=30)

        cols_bottom = st.columns([1, 1])
        with cols_bottom[0]:
            st.write(f"Stock: {qty}")
        with cols_bottom[1]:
            st.write(f"Cost: {sheckle_cost} Sheckles")

        st.markdown("---")

except Exception as e:
    st.error(f"Failed to fetch Seed Stock: {e}")
