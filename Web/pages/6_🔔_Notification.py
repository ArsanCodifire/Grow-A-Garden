import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import uuid
from order import SEED_ORDER, EGG_ORDER, GEAR_ORDER

# ---------------- Config ----------------
API_URLS = {
    "Weather": "https://gagapi.onrender.com/weather",
    "Gear": "https://gagapi.onrender.com/gear",
    "Seeds": "https://gagapi.onrender.com/seeds",
    "Eggs": "https://gagapi.onrender.com/eggs"
}

ORDER_MAPPING = {
    "Weather": ["Rainy", "Sunny", "Stormy", "Windy", "Foggy"],
    "Gear": GEAR_ORDER,
    "Seeds": SEED_ORDER,
    "Eggs": EGG_ORDER
}

CHECK_INTERVALS = {
    "Weather": 120,
    "Gear": 300,
    "Seeds": 300,
    "Eggs": 1800
}

# ---------------- Firebase Setup ----------------
service_account_info = json.loads(st.secrets["firebase"]["serviceAccount"])
service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(service_account_info)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {"databaseURL": st.secrets["firebase"]["databaseURL"]})

# ---------------- User ID via URL ----------------
user_id = st.query_params.get("user_id", [None])[0]
if not user_id:
    user_id = f"{uuid.uuid4()}_{int(time.time())}"

st.set_page_config(page_title="Grow A Garden Notifier", layout="centered")
st.title("🌱 Grow A Garden – Notifications")
st.write(f"Your anonymous user ID: {user_id}")

# ---------------- Streamlit UI ----------------
category = st.selectbox("Select category", list(API_URLS.keys()))
available_items = ORDER_MAPPING[category]
selected_items = st.multiselect("Select items to get notifications for", available_items)

if "notified" not in st.session_state:
    st.session_state.notified = set()
if "seen_notifications" not in st.session_state:
    st.session_state.seen_notifications = set()

notif_placeholder = st.empty()

# ---------------- Stock Functions ----------------
def get_stock(category):
    try:
        r = requests.get(API_URLS[category], headers={"accept": "application/json"})
        r.raise_for_status()
        data = r.json()
        if category == "Weather":
            return {item["name"]: 1 for item in data}
        return {item["name"]: item.get("quantity", 0) for item in data}
    except Exception as e:
        st.error(f"Error fetching {category} stock: {e}")
        return {}

def send_firebase_notification(category, item, user_id):
    path = f"notifications/{user_id}/{category}/{item}"
    db.reference(path).set({"message": f"{item} is now available!", "timestamp": int(time.time())})

# ---------------- Real-Time Notifications ----------------
if st.button("Activate Alerts"):
    st.info(f"Monitoring {category} for: {', '.join(selected_items)}")
    interval = CHECK_INTERVALS[category]
    while True:
        stock = get_stock(category)
        for item in selected_items:
            if stock.get(item, 0) > 0 and item not in st.session_state.notified:
                send_firebase_notification(category, item, user_id)
                st.session_state.notified.add(item)

        all_notifs = db.reference(f"notifications/{user_id}").get() or {}
        new_messages = []
        for cat, items in all_notifs.items():
            for itm, data in items.items():
                msg_id = f"{cat}_{itm}"
                if msg_id not in st.session_state.seen_notifications:
                    new_messages.append(f"{cat} → {itm}: {data['message']}")
                    st.session_state.seen_notifications.add(msg_id)
        if new_messages:
            notif_placeholder.write("\n".join(new_messages))

        time.sleep(interval)