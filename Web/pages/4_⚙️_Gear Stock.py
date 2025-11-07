import streamlit as st
import httpx
import os
from order import GEAR_ORDER
from rarity import rarity_data

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
API_URL = "https://gagapi.onrender.com/gear"
# NEW: Base URL for gear images
GEAR_IMAGE_BASE_URL = "https://growagardenpro.com/gear/"

st.title("⚙️ Gear Stock")

# The GEAR_IMAGE_MAP is no longer needed and has been removed.

try:
    with httpx.Client(timeout=10) as client:
        data = client.get(API_URL).json()

    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, str):
        st.error("API returned a string, not JSON list/dict.")
        st.stop()

    data = [x for x in data if isinstance(x, dict)]

    data.sort(key=lambda x: GEAR_ORDER.index(x["name"]) if x["name"] in GEAR_ORDER else 999)

    for item in data:
        name = item.get("name", "Unknown")
        qty = item.get("quantity", 0)
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))

        cols_top = st.columns([1, 4, 1])
        with cols_top[0]:
            # --- MODIFIED LOGIC: Use external URL for gear image ---
            # 1. Convert gear name to slug (lowercase and remove spaces)
            gear_slug = name.lower().replace(' ', '')
            # 2. Construct the full URL: e.g., "https://growagardenpro.com/gear/mastersprinkler.webp"
            gear_url = f"{GEAR_IMAGE_BASE_URL}{gear_slug}.webp" 
            
            # 3. Streamlit loads the image directly from the URL with width=75
            st.image(gear_url, width=75, caption=" ") 
            
        with cols_top[1]:
            st.write(name)
        with cols_top[2]:
            if rarity_icon:
                rarity_img = os.path.join(IMG_FOLDER, rarity_icon)
                if os.path.exists(rarity_img):
                    # Rarity icon also reduced to width=75
                    st.image(rarity_img, width=75, caption=" ") 
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
    st.error(f"Failed to fetch Gear Stock: {e}")
    
