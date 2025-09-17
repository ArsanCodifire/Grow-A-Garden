import streamlit as st
import requests
import time
from order import SEED_ORDER, EGG_ORDER, GEAR_ORDER

# ---------------- Config ----------------
ONE_SIGNAL_APP_ID = st.secrets["onesignal"]["app_id"]
ONE_SIGNAL_API_KEY = st.secrets["onesignal"]["api_key"]
CHECK_INTERVAL = 60
API_URLS = {
    "Seeds": "https://gagapi.onrender.com/seeds",
    "Gear": "https://gagapi.onrender.com/gear",
    "Eggs": "https://gagapi.onrender.com/eggs"
}
ORDER_MAPPING = {
    "Seeds": SEED_ORDER,
    "Gear": GEAR_ORDER,
    "Eggs": EGG_ORDER
}

# ---------------- Helper Functions ----------------
def get_stock(category):
    try:
        response = requests.get(API_URLS[category], headers={"accept": "application/json"})
        response.raise_for_status()
        data = response.json()
        return {item["name"]: item["quantity"] for item in data}
    except Exception as e:
        st.error(f"Error fetching {category} stock: {e}")
        return {}

def send_notification(item):
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Authorization": f"Basic {ONE_SIGNAL_API_KEY}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "app_id": ONE_SIGNAL_APP_ID,
        "included_segments": ["All"],
        "headings": {"en": "Grow A Garden: Stock Alert!"},
        "contents": {"en": f"{item} is in stock! Buy before it runs out!"}
    }
    requests.post(url, json=payload, headers=headers)

# ---------------- Streamlit UI ----------------
st.title("Grow A Garden: Stock Notifier")
category = st.selectbox("Select stock category", list(API_URLS.keys()))
available_items = ORDER_MAPPING[category]
selected_items = st.multiselect("Select items to get notifications for", available_items)

if st.button("Start Monitoring"):
    notified = set()
    st.info(f"Monitoring {category} stock for: {', '.join(selected_items)}")
    while True:
        stock = get_stock(category)
        for item in selected_items:
            if stock.get(item, 0) > 0 and item not in notified:
                send_notification(item)
                st.success(f"Notification sent: {item}")
                notified.add(item)
        time.sleep(CHECK_INTERVAL)
