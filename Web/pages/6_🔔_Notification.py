import streamlit as st
import requests
import time
import streamlit.components.v1 as components
from order import SEED_ORDER, EGG_ORDER, GEAR_ORDER

# ---------------- Config ----------------
ONE_SIGNAL_APP_ID = st.secrets["app_id"]
ONE_SIGNAL_API_KEY = st.secrets["api_key"]

API_URLS = {
    "Seeds": "https://gagapi.onrender.com/seeds",
    "Gear": "https://gagapi.onrender.com/gear",
    "Eggs": "https://gagapi.onrender.com/eggs",
    "Weather": "https://gagapi.onrender.com/weather"
}

ORDER_MAPPING = {
    "Seeds": SEED_ORDER,
    "Gear": GEAR_ORDER,
    "Eggs": EGG_ORDER
}

# Update intervals in seconds
CATEGORY_INTERVALS = {
    "Weather": 120,  # 2 minutes
    "Seeds": 300,    # 5 minutes
    "Gear": 300,     # 5 minutes
    "Eggs": 1800     # 30 minutes
}

# ---------------- OneSignal JS for mobile Chrome ----------------
components.html(f"""
<script src="https://cdn.onesignal.com/sdks/OneSignalSDK.js" async=""></script>
<script>
  window.OneSignal = window.OneSignal || [];
  OneSignal.push(function() {{
    OneSignal.init({{
      appId: "{ONE_SIGNAL_APP_ID}",
      notifyButton: {{ enable: true }}
    }});
    OneSignal.showNativePrompt();
  }});
</script>
""", height=100)

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
    response = requests.post(url, json=payload, headers=headers)
    st.write("OneSignal API response:", response.status_code, response.text)

# ---------------- Streamlit UI ----------------
st.title("Grow A Garden: Stock Notifier")

category = st.selectbox("Select stock category", list(API_URLS.keys()))
available_items = ORDER_MAPPING.get(category, [])
selected_items = st.multiselect("Select items to get notifications for", available_items)

if st.button("Activate Alerts"):
    st.info(f"Monitoring {category} stock for: {', '.join(selected_items)}")
    previous_stock = {}
    interval = CATEGORY_INTERVALS.get(category, 60)
    
    while True:
        stock = get_stock(category)
        for item in selected_items:
            prev_qty = previous_stock.get(item, 0)
            curr_qty = stock.get(item, 0)
            if prev_qty == 0 and curr_qty > 0:
                send_notification(item)
                st.success(f"Notification sent: {item}")
            previous_stock[item] = curr_qty
        time.sleep(interval)
