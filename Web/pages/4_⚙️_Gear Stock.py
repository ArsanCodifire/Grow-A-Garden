import streamlit as st
import httpx
import os
from order import GEAR_ORDER
from rarity import rarity_data

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "Images")
API_URL = "https://gagapi.onrender.com/gear"

st.title("⚙️ Gear Stock")

# A dictionary to map the item name to its actual image filename
GEAR_IMAGE_MAP = {
    "Watering Can": "Watering_Can.png",
    "Trowel": "Trowel.png",
    "Trading Ticket": "TradingTicket.png",
    "Recall Wrench": "Recall_Wrench.png",
    "Basic Sprinkler": "Basic_Sprinkler.png",
    "Advanced Sprinkler": "Advanced_Sprinkler.png",
    "Magnifying Glass":"Magnifying_Glass_Icon.png",
    "Medium Treat": "MediumTreat.png",
    "Medium Toy": "MediumToy.png",
    "Godly Sprinkler": "Godly_Sprinkler.png",
    "Master Sprinkler": "Master_Sprinkler.png",
    "Cleaning Spray": "CleaningSpray.png",
    "Favorite Tool": "Favorite_Tool.png",
    "Harvest Tool": "Harvest_tool.png",
    "Friendship Pot": "Friendship_Pot.png",
    "Grandmaster Sprinkler": "GrandmasterSprinkler.png",
    "Level Up Lollipop": "LevelUpLollipop.png"
}

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
            # Use the mapping dictionary to get the correct image filename
            gear_img_filename = GEAR_IMAGE_MAP.get(name, f"{name}.png")
            gear_img = os.path.join(IMG_FOLDER, gear_img_filename)

            if os.path.exists(gear_img):
                st.image(gear_img, width=100, caption=" ")
            else:
                st.write("No Img")
        with cols_top[1]:
            st.write(name)
        with cols_top[2]:
            if rarity_icon:
                rarity_img = os.path.join(IMG_FOLDER, rarity_icon)
                if os.path.exists(rarity_img):
                    st.image(rarity_img, width=100, caption=" ")
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
