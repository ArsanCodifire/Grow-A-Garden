import streamlit as st

# --- Theme CSS Definitions ---
# CSS to style Streamlit elements (buttons, radio, slider, sidebar)
CSS_THEMES = {
    "Default (Red Accent)": {
        "name": "Default (Red Accent)",
        "css": """
            <style>
                /* Primary Accent Color (Buttons/Radio/Slider) */
                /* Button Border */
                section.main button { border-color: #FF4B4B; }
                /* Radio Button Indicator (using pseudo-class) */
                div[data-testid="stRadio"] label span:first-child::after { 
                    background-color: #FF4B4B; 
                }
                /* Slider Track Fill */
                div[data-testid="stSlider"] div[data-testid="stTrackBackground"] > div {
                    background-color: #FF4B4B !important;
                }
                
                /* Secondary Background Color (Sidebar/Code Blocks) */
                .st-emotion-cache-16txto3 { background-color: #F0F2F6; }
            </style>
        """
    },
    "Blue Sky Accent": {
        "name": "Blue Sky Accent",
        "css": """
            <style>
                /* Blue Accent */
                section.main button { border-color: #1E90FF; }
                /* Radio Button Indicator */
                div[data-testid="stRadio"] label span:first-child::after { 
                    background-color: #1E90FF; 
                }
                /* Slider Track Fill */
                div[data-testid="stSlider"] div[data-testid="stTrackBackground"] > div {
                    background-color: #1E90FF !important;
                }
                
                /* Secondary Background */
                .st-emotion-cache-16txto3 { background-color: #DDEEFF; }
            </style>
        """
    },
    "Green Forest Accent": {
        "name": "Green Forest Accent",
        "css": """
            <style>
                /* Green Accent */
                section.main button { border-color: #228B22; }
                /* Radio Button Indicator */
                div[data-testid="stRadio"] label span:first-child::after { 
                    background-color: #228B22; 
                }
                /* Slider Track Fill */
                div[data-testid="stSlider"] div[data-testid="stTrackBackground"] > div {
                    background-color: #228B22 !important;
                }
                
                /* Secondary Background */
                .st-emotion-cache-16txto3 { background-color: #E6FFE6; }
            </style>
        """
    }
}
DEFAULT_THEME = CSS_THEMES["Default (Red Accent)"]

# --- Session State Initialization ---
if 'current_css' not in st.session_state:
    st.session_state.current_css = DEFAULT_THEME["css"]
    st.session_state.current_theme_name = DEFAULT_THEME["name"]
    
if 'custom_primary_color' not in st.session_state:
    st.session_state.custom_primary_color = "#800080"
if 'custom_secondary_color' not in st.session_state:
    st.session_state.custom_secondary_color = "#F0FFFF"

## --- Dialog Function ---
@st.dialog("🎨 Theme Selector")
def theme_selector_dialog():
    st.markdown("### Choose a Preset Theme")
    
    # 1. Preset Theme Selector
    preset_keys = list(CSS_THEMES.keys())
    preset_selection = st.radio(
        "Select an option:",
        preset_keys,
        index=preset_keys.index(st.session_state.current_theme_name) 
        if st.session_state.current_theme_name in preset_keys else 0,
        key="preset_radio"
    )

    if st.button("Apply Preset Theme", use_container_width=True, type="primary"):
        theme_data = CSS_THEMES[preset_selection]
        st.session_state.current_css = theme_data["css"]
        st.session_state.current_theme_name = theme_data["name"]
        st.rerun() 

    st.markdown("---")
    st.markdown("### Or Define a Custom Color Scheme")
    
    # 2. Custom Color Pickers
    primary_color = st.color_picker(
        "Primary Accent Color (Buttons/Radio/Slider):", 
        st.session_state.custom_primary_color,
        key="primary_picker"
    )
    secondary_color = st.color_picker(
        "Secondary Background Color (Sidebar):", 
        st.session_state.custom_secondary_color,
        key="secondary_picker"
    )

    st.session_state.custom_primary_color = primary_color
    st.session_state.custom_secondary_color = secondary_color
    
    if st.button("Apply Custom Colors", use_container_width=True):
        # Dynamically generate CSS with the user's chosen colors
        custom_css = f"""
        <style>
            /* Custom Primary Accent */
            section.main button {{ border-color: {primary_color}; }}
            div[data-testid="stRadio"] label span:first-child::after {{ 
                background-color: {primary_color}; 
            }}
            div[data-testid="stSlider"] div[data-testid="stTrackBackground"] > div {{
                background-color: {primary_color} !important;
            }}
            /* Custom Secondary Background */
            .st-emotion-cache-16txto3 {{ background-color: {secondary_color}; }}
        </style>
        """
        st.session_state.current_css = custom_css
        st.session_state.current_theme_name = f"Custom Theme (Accent: {primary_color})"
        st.rerun() 
        
    st.markdown("---")
    
    # 3. Reset Option
    if st.button("🔄 Reset to Default Theme", use_container_width=True):
        st.session_state.current_css = DEFAULT_THEME["css"]
        st.session_state.current_theme_name = DEFAULT_THEME["name"]
        st.rerun()

# =================================================================
# === MAIN APPLICATION LAYOUT STARTS HERE ===========================
# =================================================================

# 🛑 STEP 1: INJECT THE CUSTOM CSS
st.markdown(st.session_state.current_css, unsafe_allow_html=True)

st.set_page_config(page_title="Grow a Garden Stock", layout="wide")
st.title("🌱 Grow a Garden Stock Dashboard")

# --- Column Setup for Welcome Text and Settings Button ---
col_text, col_settings_button = st.columns([0.9, 0.1])

# --- Main Welcome Content in the wider column ---
with col_text:
    st.markdown(
        """
        Welcome to the Grow a Garden Stock Dashboard!
        
        Use the pages on the left to view:
        - 🌾 Seed Stock
        - 🥚 Egg Stock
        - ⚙️ Gear Stock
        - 🌥️ Weather and Mutations
        """)
    st.info(f"Active Theme: **{st.session_state.current_theme_name}**")
    st.slider("Slider Example", 0, 10, key="main_slider")
    st.radio("Radio Example", ["Option A", "Option B"], key="main_radio")

# --- Settings Button in the narrow column ---
with col_settings_button:
    st.empty() 
    
    # Place the icon-only button and call the dialog function on click
    if st.button("⚙️", help="Open Theme Selector", key="settings_button"):
        theme_selector_dialog()
