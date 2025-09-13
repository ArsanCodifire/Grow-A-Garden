import streamlit as st
import httpx
from rarity import rarity_data
import os

IMG_FOLDER = "../images"

st.title("⚙️ Gear Stock")

API_URL = "https://growagardenstock.vercel.app/api/stock/gear"

with httpx.Client(timeout=10) as client:
    resp = client.get(API_URL)
    data = resp.json()

for item in data["items"]:
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
