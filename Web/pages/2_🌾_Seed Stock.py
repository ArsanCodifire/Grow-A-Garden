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
        resp = client.get(API_URL)
        try:
            data = resp.json()
        except Exception:
            st.error("API returned invalid JSON")
            st.stop()

    # Ensure data is a list of dicts
    if isinstance(data, dict):
        data = [{"name": k, **v} for k, v in data.items()]
    elif isinstance(data, list):
        data = [x for x in data if isinstance(x, dict)]
    else:
        st.error("API returned an unexpected format")
        st.stop()

    # Sort according to SEED_ORDER
    data.sort(key=lambda x: SEED_ORDER.index(x.get("name", "")) if x.get("name") in SEED_ORDER else 999)

    for item in data:
        name = item.get("name", "Unknown")
        qty = item.get("quantity", 0)

        # Fetch rarity info
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))

        # Top row: Seed Image | Name | Rarity Image
        cols_top = st.columns([1, 4, 1])
        with cols_top[0]:
            seed_img_path = os.path.join(IMG_FOLDER, f"{name}.png")
            if os.path.exists(seed_img_path):
                st.image(seed_img_path, width=40)
        with cols_top[1]:
            st.write(name)
        with cols_top[2]:
            if rarity_icon:
                rarity_img_path = os.path.join(IMG_FOLDER, rarity_icon)
                if os.path.exists(rarity_img_path):
                    st.image(rarity_img_path, width=30)

        # Bottom row: Stock | Cost
        cols_bottom = st.columns([1, 1])
        with cols_bottom[0]:
            st.write(f"Stock: {qty}")
        with cols_bottom[1]:
            st.write(f"Cost: {sheckle_cost} Sheckles")

        st.markdown("---")

except Exception as e:
    st.error(f"Failed to fetch Seed Stock: {e}")
