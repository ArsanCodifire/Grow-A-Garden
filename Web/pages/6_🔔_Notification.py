import streamlit as st
import streamlit.components.v1 as components
import requests
import time
import json
from order import SEED_ORDER, EGG_ORDER, GEAR_ORDER

# ---------------- Config ----------------
APP_ID = st.secrets["app_id"]
API_KEY = st.secrets["api_key"]

API_URLS = {
    "Weather": "https://gagapi.onrender.com/weather",
    "Gear": "https://gagapi.onrender.com/gear",
    "Seeds": "https://gagapi.onrender.com/seeds",
    "Eggs": "https://gagapi.onrender.com/eggs"
}

ORDER_MAPPING = {
    "Weather": ["Rainy", "Sunny", "Stormy", "Windy", "Foggy"],  # example
    "Gear": GEAR_ORDER,
    "Seeds": SEED_ORDER,
    "Eggs": EGG_ORDER
}

CHECK_INTERVALS = {
    "Weather": 120,   # 2 min
    "Gear": 300,      # 5 min
    "Seeds": 300,     # 5 min
    "Eggs": 1800      # 30 min
}

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Grow A Garden Notifier", layout="centered")
st.title("🌱 Grow A Garden – Notifications")

# Step 1: Inject OneSignal SDK v16
components.html(f"""
<script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
<script>
  window.OneSignalDeferred = window.OneSignalDeferred || [];
  OneSignalDeferred.push(function(OneSignal) {{
    OneSignal.init({{
      appId: "{APP_ID}",
      notifyButton: {{ enable: true }},
    }});

    OneSignal.Notifications.addEventListener("permissionChange", function(e) {{
      if (e.to === "granted") {{
        OneSignal.User.PushSubscription.addEventListener("change", function(sub) {{
          if (sub && sub.token) {{
            window.parent.postMessage({{"token": sub.token}}, "*");
          }}
        }});
      }}
    }});
  }});
</script>
""", height=0)

# Step 2: Listen for token
token = st.session_state.get("push_token")
msg = st.query_params().get("msg", [""])[0]
if msg:
    try:
        data = json.loads(msg)
        if "token" in data:
            st.session_state["push_token"] = data["token"]
            token = data["token"]
    except:
        pass

# Step 3: Show subscription status
if token:
    st.success("✅ You are subscribed for notifications!")
else:
    st.warning("⚠️ Click 'Allow' when prompted to subscribe.")

# Step 4: Register user in OneSignal
if token:
    external_id = "user_123"  # replace with your own system’s user ID
    url = f"https://api.onesignal.com/apps/{APP_ID}/users"
    payload = {
        "identity": {"external_id": external_id},
        "properties": {"tags": {"garden_level": "beginner"}},
        "subscriptions": [
            {"type": "Push", "token": token, "enabled": True}
        ]
    }
    headers = {"Authorization": f"Basic {API_KEY}", "Content-Type": "application/json"}
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        st.success("🎉 User registered in OneSignal")
    else:
        st.error(f"❌ Error: {res.status_code} → {res.text}")

# ---------------- Stock Monitor ----------------
def get_stock(category):
    try:
        r = requests.get(API_URLS[category], headers={"accept": "application/json"})
        r.raise_for_status()
        data = r.json()
        if category == "Weather":
            return {item["name"]: 1 for item in data}
        return {item["name"]: item["quantity"] for item in data}
    except Exception as e:
        st.error(f"Error fetching {category} stock: {e}")
        return {}

def send_notification(category, item, external_id):
    url = f"https://api.onesignal.com/apps/{APP_ID}/notifications"
    headers = {"Authorization": f"Basic {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "app_id": APP_ID,
        "include_aliases": {"external_id": [external_id]},
        "headings": {"en": f"Grow A Garden: {category} Update!"},
        "contents": {"en": f"{item} is now available!"}
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.status_code, res.text

category = st.selectbox("Select category", list(API_URLS.keys()))
available_items = ORDER_MAPPING[category]
selected_items = st.multiselect("Select items to get notifications for", available_items)

if st.button("Activate Alerts") and token:
    notified = set()
    st.info(f"Monitoring {category} for: {', '.join(selected_items)}")
    interval = CHECK_INTERVALS[category]
    while True:
        stock = get_stock(category)
        for item in selected_items:
            if stock.get(item, 0) > 0 and item not in notified:
                code, txt = send_notification(category, item, external_id)
                if code == 200:
                    st.success(f"📢 Notification sent: {item}")
                else:
                    st.error(f"Error sending notification: {txt}")
                notified.add(item)
        time.sleep(interval)
