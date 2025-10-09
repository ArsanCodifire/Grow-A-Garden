import streamlit as st
import json
import time
import firebase_admin
from firebase_admin import credentials, db, messaging
import httpx
import uuid
import extra_streamlit_components as stx
import streamlit.components.v1 as components

# NOTE: Assumes 'order.py' is a file with simple list/tuple constants
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
# Define the path for global stock status in Firebase
STOCK_STATUS_REF = "global_stock_status"

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
        # persistent user ID, will not change
        st.session_state.user_id = f"{uuid.uuid4()}"
        cookie_manager.set("user_id", st.session_state.user_id, key="set_user_id")
user_id = st.session_state.user_id

# ---------------- Handle token from query param (FIXED: Added st.query_params access protection) ----------------
query_params = st.query_params
if "token" in query_params and query_params["token"]:
    token = query_params["token"][0]
    # Store token with a unique key
    db.reference(f"user_tokens/{user_id}/{token}").set(int(time.time()))
    # Remove the token from the query params to prevent continuous reloading
    # This is not a full stop, but it prevents the token logic from re-running on subsequent interactions.
    st.query_params.pop("token")


# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="Grow A Garden Notifier", layout="centered")
st.title("🌱 Grow A Garden – Notifications")
st.write(f"Your persistent user ID: **`{user_id}`**")

# ---------------- Streamlit UI ----------------
category = st.selectbox("Select category", list(API_URLS.keys()))
available_items = ORDER_MAPPING[category]
# Get current subscriptions from Firebase to pre-select
user_subs = db.reference(f"user_subscriptions/{user_id}/{category}").get() or {}
pre_selected = [item for item in available_items if item in user_subs]

selected_items = st.multiselect("Select items to get notifications for", available_items, default=pre_selected)

# Save/Update subscriptions to Firebase and clean up unselected items
current_subs_ref = db.reference(f"user_subscriptions/{user_id}/{category}")
# Set all selected items to True
for item in selected_items:
    # Set to True (instead of time.time()) for cleaner storage
    current_subs_ref.child(item).set(True)

# Remove unselected items
for item in set(available_items) - set(selected_items):
    if item in user_subs:
        current_subs_ref.child(item).delete()


if "seen_notifications" not in st.session_state:
    st.session_state.seen_notifications = set()

notif_placeholder = st.empty()

# ---------------- Stock Functions ----------------
@st.cache_data(ttl=10) # Cache stock data for 10 seconds to limit API calls
def get_current_stock(category):
    """Fetches current stock from external API."""
    try:
        # Use a short timeout for better UX
        r = httpx.get(API_URLS[category], headers={"accept": "application/json"}, timeout=5.0)
        r.raise_for_status()
        data = r.json()
        return {item["name"]: item.get("quantity", 0) for item in data}
    except Exception as e:
        # Log the error but don't stop the app
        st.error(f"Error fetching {category} stock: {e}")
        return {}

def update_global_stock_status(category, current_stock):
    """Updates the persistent stock status in Firebase."""
    global_ref = db.reference(STOCK_STATUS_REF).child(category)
    
    # Fetch previous status
    prev_status = global_ref.get() or {}
    
    updates = {}
    for item, quantity in current_stock.items():
        is_in_stock = quantity > 0
        prev_in_stock = prev_status.get(item, {}).get("in_stock", False)

        # Only update if status has changed
        if is_in_stock != prev_in_stock:
            updates[item] = {
                "in_stock": is_in_stock,
                "timestamp": int(time.time()),
                "quantity": quantity
            }
        elif is_in_stock:
             # Optionally update quantity/timestamp even if status is same
             updates[item] = {
                "in_stock": True,
                "timestamp": int(time.time()),
                "quantity": quantity
            }
    
    if updates:
        # Use update() to only modify the changing items
        global_ref.update(updates)
        return updates # Return changes to trigger notifications
    return {}


def send_notification(category, item, quantity):
    """Sends notification and removes stale tokens."""
    message_text = f"{item} is in stock ({quantity})!"
    
    # 1. Fetch all users subscribed to this item (only checking for True value)
    all_subs_data = db.reference(f"user_subscriptions").get() or {}
    
    for u_id, cats in all_subs_data.items():
        if category in cats and item in cats[category] and cats[category][item] is True:
            # Store notification
            db.reference(f"notifications/{u_id}/{category}/{item}").set({
                "message": message_text,
                "timestamp": int(time.time())
            })
            
            # 2. Send FCM
            tokens_ref = db.reference(f"user_tokens/{u_id}")
            tokens = tokens_ref.get() or {}
            
            for t in list(tokens.keys()): # Iterate over a copy of keys
                try:
                    messaging.send(messaging.Message(
                        notification=messaging.Notification(
                            title=f"📦 {item} is in Stock!",
                            body=message_text
                        ),
                        token=t
                    ))
                except firebase_admin.exceptions.InvalidArgument:
                    # Token format is bad, remove it
                    tokens_ref.child(t).delete()
                    print(f"Removed invalid token for {u_id}")
                except firebase_admin.messaging.UnregisteredError:
                    # Token is stale/expired, remove it
                    tokens_ref.child(t).delete()
                    print(f"Removed unregistered token for {u_id}")
                except Exception as e:
                    print(f"FCM error for {u_id}:", e)
            
            # 3. Browser toast if this is the current user
            if u_id == user_id:
                st.toast(message_text, icon="🎉")


# ---------------- Notification Button Logic ----------------
if st.button("Check Stock & Send Notifications", type="primary"):
    with st.spinner("Checking external API and processing notifications..."):
        # 1. Get current stock from the external API
        current_stock = get_current_stock(category)
        
        # 2. Update persistent global stock status and get items that just came in stock
        # This is the core fix for persistent notification logic.
        stock_changes = update_global_stock_status(category, current_stock)

        # 3. Process notifications for items that just came IN stock
        for item, data in stock_changes.items():
            if data['in_stock'] is True:
                # Send notifications to ALL subscribed users globally
                send_notification(category, item, data['quantity'])
                st.success(f"Stock update for **{item}**: NOW IN STOCK! Notifications sent.")
            elif data['in_stock'] is False:
                st.info(f"Stock update for **{item}**: OUT OF STOCK.")


    # 4. Display received notifications for current user (RE-RUNS on every button click)
    all_notifs = db.reference(f"notifications/{user_id}").get() or {}
    new_messages = []
    
    # Iterate through all stored notifications for the user
    for cat, items in all_notifs.items():
        for itm, data in items.items():
            msg_id = f"{cat}_{itm}_{data['timestamp']}" # Include timestamp for unique ID
            
            # Only display notifications not seen in this session
            if msg_id not in st.session_state.seen_notifications:
                # Format the message
                timestamp_str = time.strftime('%H:%M:%S', time.localtime(data['timestamp']))
                new_messages.append(f"⏰ **{timestamp_str}** | {cat} → **{itm}**: {data['message']}")
                st.session_state.seen_notifications.add(msg_id)

    if new_messages:
        notif_placeholder.markdown("### 🔔 New Notifications")
        # Display the newest notifications at the top
        notif_placeholder.info("\n\n".join(reversed(new_messages)))
    else:
        notif_placeholder.info("No new notifications yet.")

# ---------------- Firebase Web Push Setup ----------------
firebase_web_config = st.secrets["firebase_web"]

# Note: The original JS forced a page reload which is bad. The Python side is
# now modified to handle the query param, but the JS should not reload the page
# if possible. Here, we keep the original intent (redirect to pass token)
# but acknowledge it's an anti-pattern.
components.html(f"""
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
    // Check if token already exists in URL to avoid re-registering and reloading
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('token')) return;

    try {{
        // Wait for permission
        const permission = await Notification.requestPermission();
        if (permission !== 'granted') return;

        // Get the token
        const token = await messaging.getToken({{ vapidKey: "{firebase_web_config['vapidKey']}" }});
        if(token){{
            // Redirect to Streamlit with token as query param
            const currentUrl = window.location.href.split('?')[0];
            window.location.href = currentUrl + '?token=' + token;
        }}
    }} catch(e) {{
        console.error("FCM Token Registration Error:", e);
    }}
}}
registerToken();
</script>
""", height=0)
