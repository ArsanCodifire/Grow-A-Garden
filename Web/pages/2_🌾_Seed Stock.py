import streamlit as st
import httpx
import os
from order import SEED_ORDER
from rarity import rarity_data

# Existing local folder for rarity icons (kept for compatibility)
IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
API_URL = "https://gagapi.onrender.com/seeds"

# Base URL for seed images
SEED_IMAGE_BASE_URL = "https://growagardenpro.com/seeds/" 

st.title("🌾 Seed Stock")

try:
    with httpx.Client(timeout=10) as client:
        data = client.get(API_URL).json()

    # Force data into a list of dicts  
    if isinstance(data, dict):  
        data = [data]  
    elif isinstance(data, str):  
        st.error("API returned a string, not JSON list/dict.")  
        st.stop()  

    data = [x for x in data if isinstance(x, dict)]  

    # Sort according to SEED_ORDER  
    data.sort(key=lambda x: SEED_ORDER.index(x["name"]) if x["name"] in SEED_ORDER else 999)  

    # Render seeds  
    for item in data:  
        name = item.get("name", "Unknown")  
        qty = item.get("quantity", 0)  
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))  

        cols_top = st.columns([1, 4, 1])  
        
        # --- MODIFIED LOGIC: Use external URL for seed image ---
        with cols_top[0]:  
            # 1. Convert seed name to slug (lowercase and remove spaces)
            seed_slug = name.lower().replace(' ', '') 
            # 2. Construct the full URL: e.g., "https://growagardenpro.com/seeds/dragonfruitseed.webp"
            seed_url = f"{SEED_IMAGE_BASE_URL}{seed_slug}seed.webp"
            
            # 3. Streamlit loads the image directly from the URL with width=75
            st.image(seed_url, width=75)
        # --- END MODIFIED LOGIC ---

        with cols_top[1]:  
            st.write(name)  

        with cols_top[2]:  
            # Rarity icons still use local files (if they exist)
            if rarity_icon:  
                rarity_img = os.path.join(IMG_FOLDER, rarity_icon)  
                if os.path.exists(rarity_img):  
                    # Rarity icon also reduced to width=75
                    st.image(rarity_img, width=75)  
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
    
