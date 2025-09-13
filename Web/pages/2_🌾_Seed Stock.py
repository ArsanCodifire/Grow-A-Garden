import streamlit as st
import httpx
from rarity import rarity_data
import os

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "../images")

st.title("🌾 Seed Stock")

API_URL = "https://growagardenstock.vercel.app/api/stock/seeds"

try:
    with httpx.Client(timeout=10) as client:
        resp = client.get(API_URL)
        resp.raise_for_status()
        data = resp.json()
except Exception as e:
    st.error(f"Failed to fetch API: {e}")
    st.stop()

items = data.get("items", [])
if not items:
    st.warning("No seed stock available right now.")
else:
    for item in items:
        name = item.get("name", "Unknown")
        qty = item.get("quantity", 0)
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))

        cols = st.columns([1, 3, 2, 2])
        with cols[0]:
            if rarity_icon:
                img_path = os.path.join(IMG_FOLDER, rarity_icon)
                if os.path.exists(img_path):
                    st.image(img_path, width=30)
        with cols[1]:
            st.write(name)
        with cols[2]:
            st.write(rarity_name)
        with cols[3]:
            st.write(f"{sheckle_cost} Sheckles | Stock: {qty}")