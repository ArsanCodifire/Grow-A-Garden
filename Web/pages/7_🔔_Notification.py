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
from rarity import rarity_data

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
# Use st.cache_resource for Firebase initialization to run once
@st.cache_resource
def initialize_firebase():
    try:
        service_account_info = json.loads(st.secrets["firebase"]["serviceAccount"])
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(service_account_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {"databaseURL": st.secrets["firebase"]["databaseURL"]})
        return True
    except Exception as e:
        st.error(f"Failed to initialize Firebase Admin SDK. Check `st.secrets`: {e}")
        return False

# ---------------- Stock Check Functions ----------------

# This function updates the global stock status in Firebase
def update_global_stock_status():
    """Fetches current stock from APIs and updates the global status in Firebase."""
    if not initialize_firebase():
        return

    ref = db.reference(STOCK_STATUS_REF)
    new_status = {}
    
    for category, api_url in API_URLS.items():
        try:
            with httpx.Client(timeout=5) as client:
                data = client.get(api_url).json()
            
            # Filter for items that are currently in stock (quantity > 0)
            in_stock_names = [
                item.get("name") 
                for item in data 
                if isinstance(item, dict) and item.get("quantity", 0) > 0
            ]
            
            # Only store items that are in stock
            if in_stock_names:
                new_status[category] = in_stock_names

        except Exception as e:
            # Log error but continue with other categories
            print(f"Error fetching {category} stock: {e}") 
            
    # Update Firebase with current stock status and timestamp
    ref.set({
        "timestamp": time.time(),
        "status": new_status
    })
    
    return new_status

# ---------------- Cookie / User ----------------
cookie_manager = stx.CookieManager()

def get_user_id():
    if "user_id" not in st.session_state:
        stored_id = cookie_manager.get("user_id")
        if stored_id:
            st.session_state["user_id"] = stored_id
        else:
            new_id = str(uuid.uuid4())
            st.session_state["user_id"] = new_id
            cookie_manager.set("user_id", new_id, expires_at=time.time() + 3600 * 24 * 365) # 1 year
    return st.session_state["user_id"]

USER_ID = get_user_id()

# ---------------- Frontend ----------------

st.title("🔔 Notification Settings")
st.markdown("Enable push notifications to get alerts when rare items restock!")

# Check for FCM Token in URL parameters (redirected from JavaScript)
fcm_token = st.query_params.get("token", [None])[0]

if fcm_token:
    if initialize_firebase():
        # Store the token in Firebase under the user's ID
        try:
            user_ref = db.reference(f"users/{USER_ID}")
            user_ref.update({"fcm_token": fcm_token, "last_active": time.time()})
            st.success("✅ Notifications successfully activated and linked to your account!")
        except Exception as e:
            st.error(f"Error saving token to database: {e}")
    
    # Clean the URL to avoid re-triggering the logic on every run
    st.query_params


# ---------------- Subscription Management UI ----------------
if initialize_firebase():
    user_ref = db.reference(f"users/{USER_ID}")
    user_data = user_ref.get() or {}
    
    subscribed_token = user_data.get("fcm_token")
    subscriptions = user_data.get("subscriptions", {})

    st.subheader("Your Subscription Status")
    
    if subscribed_token:
        st.info("You are currently subscribed to notifications.")
        st.write(f"**Your ID:** `{USER_ID}`")
        st.write("---")
        
        st.subheader("Select Items for Notifications")
        
        # Display selection options grouped by category
        for category, item_order in ORDER_MAPPING.items():
            st.markdown(f"**{category}**")
            
            # Filter the list to only include Rare, Legendary, Mythical, Divine, Prismatic
            item_checkbox_cols = st.columns(3)
            col_index = 0
            
            for item_name in item_order:
                rarity, _, _ = rarity_data.get(item_name, ("Unknown", None, 0))
                
                # Check for high rarity items
                if rarity in ["Rare", "Legendary", "Mythical", "Divine", "Prismatic", "Special"]:
                    
                    # Check if the user is already subscribed to this item
                    is_subscribed = subscriptions.get(item_name, False)
                    
                    # Create the checkbox
                    new_state = item_checkbox_cols[col_index % 3].checkbox(
                        item_name, 
                        value=is_subscribed,
                        key=f"subscribe_{item_name}"
                    )

                    # Update subscriptions state if it changed
                    if new_state != is_subscribed:
                        subscriptions[item_name] = new_state
                        user_ref.child("subscriptions").update({item_name: new_state})
                        st.session_state["_subscriptions_updated"] = True
                        st.experimental_rerun()
                        
                    col_index += 1

        if st.session_state.get("_subscriptions_updated"):
            st.success("Subscription settings updated!")
            del st.session_state["_subscriptions_updated"]
            
    else:
        st.warning("You are not currently subscribed. Click the button below to enable notifications in your browser.")

# ---------------- Client-side JavaScript for Token Registration ----------------

# The client-side script must be displayed if the token is NOT found.
if not fcm_token and not (user_data.get("fcm_token") if initialize_firebase() else False):
    if st.button("Activate Notifications"):
        firebase_web_config = st.secrets["firebase_web"]
        
        # HTML/JavaScript to handle FCM token registration
        # NOTE: This HTML block is a copy/paste of the original file's snippet,
        # but triggered only when necessary via st.button.
        html_content = f"""
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
        """
        components.html(html_content, height=0, width=0)

# Optional: Button to run the stock checker manually
if st.button("Manually Check Stock Now (For Testing)"):
    with st.spinner("Checking and updating global stock status..."):
        updated_status = update_global_stock_status()
        st.success("Global stock status updated! (This doesn't send notifications, but prepares the data.)")
        # st.json(updated_status) # Uncomment for debug
        
