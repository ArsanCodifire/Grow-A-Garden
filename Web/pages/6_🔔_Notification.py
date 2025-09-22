import streamlit as st
import json
import time
import firebase_admin
from firebase_admin import credentials, db, messaging
import httpx
import uuid
import extra_streamlit_components as stx
from order import SEED_ORDER, EGG_ORDER, GEAR_ORDER

# ---------------- Config ----------------
API_URLS = {
    "Gear": "https://gagapi.onrender.com/gear",
    "Seeds": "https://gagapi.onrender.com/seeds",
    "Eggs": "https://gagapi.onrender.com/eggs"
}
ORDER_MAPPING = {
    "Gear": GEAR_ORDER,
    "Seeds": SEED_ORDER,
    "Eggs": EGG_ORDER
}

# ---------------- Firebase Admin Setup ----------------
service_account_info = json.loads(st.secrets["firebase"]["serviceAccount"])
service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(service_account_info)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {"databaseURL": st.secrets["firebase"]["databaseURL"]})

# ---------------- Cookie / User ----------------
cookie_manager = stx.CookieManager()
if "user_id" not in st.session_state:
    stored_id = cookie_manager.get("user_id")
    if stored_id:
        st.session_state.user_id = stored_id
    else:
        st.session_state.user_id = f"{uuid.uuid4()}_{int(time.time())}"
        cookie_manager.set("user_id", st.session_state.user_id, key="set_user_id")
user_id = st.session_state.user_id

# ---------------- Handle token from query param ----------------
query_params = st.experimental_get_query_params()
if "token" in query_params:
    token = query_params["token"][0]
    db.reference(f"user_tokens/{user_id}/{token}").set(int(time.time()))

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="Grow A Garden Notifier", layout="centered")
st.title("🌱 Grow A Garden – Notifications")
st.write(f"Your persistent user ID: {user_id}")

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
        return {item["name"]: item.get("quantity", 0) for item in data}
    except Exception as e:
        st.error(f"Error fetching {category} stock: {e}")
        return {}

def send_notification(category, item, user_id):
    stock = get_stock(category)
    amount = stock.get(item, 0)
    message_text = f"{item} is in stock! Amount: {amount}"

    # Store in Firebase
    db.reference(f"notifications/{user_id}/{category}/{item}").set({
        "message": message_text,
        "timestamp": int(time.time())
    })

    # Push FCM notifications
    tokens = db.reference(f"user_tokens/{user_id}").get() or {}
    for token in tokens.keys():
        try:
            messaging.send(messaging.Message(
                notification=messaging.Notification(
                    title=f"{item} in Stock!",
                    body=message_text
                ),
                token=token
            ))
        except Exception as e:
            print("FCM error:", e)

    # Browser toast fallback
    st.toast(message_text)

# ---------------- Notification Button ----------------
if st.button("Check Notifications"):
    stock = get_stock(category)
    for item in selected_items:
        if stock.get(item, 0) > 0 and item not in st.session_state.notified:
            send_notification(category, item, user_id)
            st.session_state.notified.add(item)

    # Display notifications from Firebase
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

firebase_web_config = st.secrets["firebase"]["webApp"]

st.html(f"""
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-messaging-compat.js"></script>
<script>
const firebaseConfig = {{
    apiKey: "{firebase_web_config['apiKey']}",
    authDomain: "{firebase_web_config['authDomain']}",
    projectId: "{firebase_web_config['projectId']}",
    storageBucket: "{firebase_web_config['storageBucket']}",
    messagingSenderId: "{firebase_web_config['messagingSenderId']}",
    appId: "{firebase_web_config['appId']}",
    measurementId: "{firebase_web_config['measurementId']}"
}};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

async function registerToken() {{
    try {{
        await Notification.requestPermission();
        const token = await messaging.getToken({{ vapidKey: "{firebase_web_config['vapidKey']}" }});
        if(token){{
            // Redirect to Streamlit with token as query param
            const currentUrl = window.location.href.split('?')[0];
            window.location.href = currentUrl + '?token=' + token;
        }}
    }} catch(e) {{
        console.log(e);
    }}
}}
registerToken();
</script>
""", height=0)