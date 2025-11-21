import streamlit as st

# The st_theme_changer plugin is used for persistent, global theme management.
from streamlit_plugins.components.theme_changer import st_theme_changer
from streamlit_plugins.components.theme_changer.entity import ThemeInfo, ThemeInput, ThemeBaseLight, ThemeBaseDark

# --- Theme Definitions (Only 3 Core Themes) ---

# Garden Oasis (Light)
garden_light_theme = ThemeInput(
    name="Garden Oasis (Light)",
    icon="🌿", 
    order=1,
    themeInfo=ThemeInfo(
        base=ThemeBaseLight.base, primaryColor="#388E3C", backgroundColor="#F9FFF5", 
        secondaryBackgroundColor="#E8F5E9", textColor="#000000", widgetBackgroundColor="#FFFFFF",
        widgetBorderColor="#81C784", skeletonBackgroundColor="#C8E6C9",
    )
)

# Midnight Flora (Dark)
garden_dark_theme = ThemeInput(
    name="Midnight Flora (Dark)",
    icon="🌙", 
    order=2,
    themeInfo=ThemeInfo(
        base=ThemeBaseDark.base, primaryColor="#8BC34A", backgroundColor="#1C301C", 
        secondaryBackgroundColor="#2E482E", textColor="#E8F5E9", widgetBackgroundColor="#3A573A", 
        widgetBorderColor="#A5D6A7", skeletonBackgroundColor="#556B55",
    )
)

# System Default (Auto) - Mandatory for theme changer auto-detection
system_default_theme = ThemeInput(
    name="System Default (Auto)",
    icon="✨", 
    order=0, 
    themeInfo=garden_light_theme.themeInfo 
)


# Dictionary containing ONLY the 3 core themes
init_theme_data = {
    'system_default_theme': system_default_theme,
    'garden_light': garden_light_theme,
    'garden_dark': garden_dark_theme,
}


# 1. Initialize session state variables
if "theme_data" not in st.session_state:
    st.session_state["theme_data"] = init_theme_data

theme_data = st.session_state["theme_data"]


# 2. Theme Changer Initialization (Mandatory: Must run first to set the theme globally)
st_theme_changer(
    themes_data=theme_data, 
    render_mode="init", 
    default_init_theme_name="system_default_theme", 
    key="theme_init"
)


# --- Settings Dialogue DEFINITION (using the @st.dialog decorator) ---

@st.dialog("App Settings", width="small")
def open_settings_dialog():
    """
    Defines the content shown inside the modal dialog.
    """
    st.header("App Settings")
    st.markdown("---")

    # 1. Quick Theme Picker (The 3 Core Themes)
    st.subheader("🎨 Theme Switch")
    st.markdown("Select your preferred core theme.")
    
    # Renders the theme selection component
    st_theme_changer(
        themes_data=theme_data, 
        render_mode="pills", # A clean, pill-shaped UI for switching
        rerun_whole_st=True, 
        key="dialog_theme_picker"
    )
    
    st.markdown("---")

    # 2. Theme Editor (Placeholder, now removed for stability/simplicity)
    st.subheader("🛠️ Custom Theme Maker")
    st.warning("The custom theme editor is currently disabled for stability. Use the switches above.")
    
    st.markdown("---")
    
    # 3. Music Option (Placeholder)
    st.subheader("🎵 Other Settings")
    st.info("Future settings like notifications or music will appear here.")
    
    # Note: Dialog dismissal is handled by the "x" button or st.rerun() from theme change.


# --- Main Application Layout ---

# Use columns to place the title and the settings button on the same line
col_title, col_settings = st.columns([10, 1])

with col_title:
    st.title("🌱 Grow a Garden Stock Dashboard")

with col_settings:
    # 4. Button to open the dialog
    # We call the decorated function directly when the button is pressed.
    if st.button("⚙️ Settings", key="settings_button"):
        open_settings_dialog()


# 5. Display main app content
st.header("Welcome!")
st.markdown(
    """
    This dashboard provides a simple structure to manage your garden-related stocks.

    Click the **'⚙️ Settings'** button above to open the theme selector dialog and choose between **Garden Oasis (Light)** and **Midnight Flora (Dark)**.

    ### Dashboard Pages (Sidebar)
    - **🌾 Seed Stock:** Inventory of available seeds.
    - **🥚 Egg Stock:** Inventory of creature eggs.
    - **⚙️ Gear Stock:** Tools and equipment inventory.
    - **🌥️ Weather and Mutations:** Analysis of environmental factors.
    """
)
