import streamlit as st
import httpx
import os
# from order import COSMETIC_ORDER # NOTE: Add COSMETIC_ORDER to order.py if sorting is needed
from rarity import rarity_data

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
# ASSUMED API ENDPOINT
API_URL = "https://gagapi.onrender.com/cosmetics" 
# ASSUMED IMAGE URL PATTERN
COSMETIC_IMAGE_BASE_URL = "https://growagardenpro.com/cosmetics/" 

st.title("✨ Cosmetic Stock")

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

    # NOTE: Uncomment the below line if you add a COSMETIC_ORDER list to order.py
    # data.sort(key=lambda x: COSMETIC_ORDER.index(x["name"]) if x["name"] in COSMETIC_ORDER else 999)  

    # Render cosmetics  
    for item in data:  
        name = item.get("name", "Unknown")  
        qty = item.get("quantity", 0)  
        # Cosmetics may not be in rarity.py, but we check for consistency
        rarity_name, rarity_icon, sheckle_cost = rarity_data.get(name, ("Unknown", None, 0))  

        cols_top = st.columns([1, 4, 1])  
        with cols_top[0]:  
            # 1. Convert cosmetic name to slug (lowercase and remove spaces)
            cosmetic_slug = name.lower().replace(' ', '')
            # 2. Construct the full URL: e.g., "https://growagardenpro.com/cosmetics/sunhat.webp"
            cosmetic_url = f"{COSMETIC_IMAGE_BASE_URL}{cosmetic_slug}.webp" 
            
            # 3. Load image with reduced width (75)
            st.image(cosmetic_url, width=75, caption=" ") 
            
        with cols_top[1]:  
            st.write(name)  

        with cols_top[2]:  
            # Rarity icons still use local files (if they exist)
            if rarity_icon:  
                rarity_img = os.path.join(IMG_FOLDER, rarity_icon)  
                if os.path.exists(rarity_img):  
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
    st.error(f"Failed to fetch Cosmetic Stock: {e}")
  
