import streamlit as st

# The st_theme_changer plugin is used for persistent, global theme management.
from streamlit_plugins.components.theme_changer import st_theme_changer
from streamlit_plugins.components.theme_changer.entity import ThemeInfo, ThemeInput, ThemeBaseLight, ThemeBaseDark

# --- Theme Definitions (Simplified: Only 3 Core Themes) ---

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
    # Must point to a valid ThemeInfo; using light as default appearance
    themeInfo=garden_light_theme.themeInfo 
)


# Dictionary containing ONLY the 3 core themes
init_theme_data = {
    'system_default_theme': system_default_theme,
    'garden_light': garden_light_theme,
    'garden_dark': garden_dark_theme,
}


# --- Settings Dialogue (st.dialog) Logic ---

def render_settings_dialog():
    """
    Renders the content of the st.dialog, providing a theme picker
    and an editor for the current theme.
    """
    st.header("App Settings")
    st.markdown("---")

    # 1. Quick Theme Picker (The 3 Core Themes)
    st.subheader("🎨 Quick Theme Switch")
    st.markdown("Select your preferred core theme.")
    
    st_theme_changer(
        themes_data=init_theme_data, 
        render_mode="pills", # A clean, pill-shaped UI for switching
        rerun_whole_st=True, 
        key="dialog_theme_picker"
    )
    
    st.markdown("---")

    # 2. Theme Editor (Allows editing the current theme)
    with st.expander("🛠️ Theme Color Editor", expanded=False):
        st.info("Edit the color palette of the currently active theme.")
        
        # This part requires some advanced logic, but for simplicity, we'll use placeholders
        # since the full editing feature requires complex state management across theme keys.
        st.warning("The Theme Editor functionality is temporarily disabled for stability. Please use the Quick Theme Switch above.")
        
    st.markdown("---")
    
    # Placeholder for other settings
    st.subheader("🎵 Other Settings")
    st.info("Future settings like notifications or music will appear here.")
    
    # The dialog closes automatically when the user clicks 'X' or when st.rerun() is called
    # (which happens when the theme is changed above).


# --- Application Logic ---

# 1. Initialize session state variables
if "theme_data" not in st.session_state:
    st.session_state["theme_data"] = init_theme_data
if "show_settings_dialog" not in st.session_state:
    st.session_state["show_settings_dialog"] = False

theme_data = st.session_state["theme_data"]


# 2. Theme Changer Initialization (Mandatory: Must run first to set the theme globally)
st_theme_changer(
    themes_data=theme_data, 
    render_mode="init", 
    default_init_theme_name="system_default_theme", 
    key="theme_init"
)


# --- Main Application Layout ---

# Use columns to place the title and the settings button on the same line
col_title, col_settings = st.columns([10, 1])

with col_title:
    st.title("🌱 Grow a Garden Stock Dashboard")

with col_settings:
    # --- The Settings Button ---
    if st.button("⚙️ Settings", key="settings_button"):
        st.session_state["show_settings_dialog"] = True
        st.rerun() 


# 3. Handle the st.dialog
# --- The Dialog Trigger ---
if st.session_state.get("show_settings_dialog"):
    st.dialog("settings_dialog_id", title="App Settings", func=render_settings_dialog)


# 4. Display main app content
st.header("Welcome!")
st.markdown(
    """
    This dashboard provides a simple structure to manage your garden-related stocks.

    If you want to change the look of the application, click the **'⚙️ Settings'** button above to open the theme selector dialog.

    ### Dashboard Pages (Sidebar)
    - **🌾 Seed Stock:** Inventory of available seeds.
    - **🥚 Egg Stock:** Inventory of creature eggs.
    - **⚙️ Gear Stock:** Tools and equipment inventory.
    - **🌥️ Weather and Mutations:** Analysis of environmental factors.
    """
)
