import streamlit as st
import httpx
import os
from rarity import rarity_data

# Auto-detect images folder: first try Web/images, fallback to current folder
BASE_DIR = os.path.dirname(__file__)
IMG_FOLDERS = [
    os.path.join(BASE_DIR, "..", "images"),  # original location
    BASE_DIR,                               # fallback: inside pages/
]

def find_image(filename):
    for folder in IMG_FOLDERS:
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            return path
    return None

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
                icon_path = find_image(rarity_icon)
                if icon_path:
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