import streamlit as st

# The st_theme_changer plugin is used for persistent, global theme management.
from streamlit_plugins.components.theme_changer import st_theme_changer
from streamlit_plugins.components.theme_changer.entity import ThemeInfo, ThemeInput, ThemeBaseLight, ThemeBaseDark

# --- Configuration ---
# Define theme keys that are protected from editing
PROTECTED_THEMES = ['garden_light', 'garden_dark']
CUSTOM_THEME_KEY = 'custom_theme_key'
DEFAULT_INIT_THEME = 'garden_dark'

# --- Theme Definitions ---

# Garden Oasis (Light) - CORE THEME
garden_light_theme = ThemeInput(
    name="Garden Oasis (Light)",
    icon="🌿", 
    order=1,
    themeInfo=ThemeInfo(
        base=ThemeBaseLight.base, primaryColor="#388E3C", backgroundColor="#F9FFF5", 
        secondaryBackgroundColor="#E8F5E9", textColor="#000000", widgetBackgroundColor="#FFFFFF",
        widgetBorderColor="#81C784", skeletonBackgroundColor="#C8E6C9", bodyFont=ThemeBaseLight.bodyFont,
        codeFont=ThemeBaseLight.codeFont, fontFaces=ThemeBaseLight.fontFaces
    )
)

# Midnight Flora (Dark) - CORE THEME
garden_dark_theme = ThemeInput(
    name="Midnight Flora (Dark)",
    icon="🌙", 
    order=2,
    themeInfo=ThemeInfo(
        base=ThemeBaseDark.base, primaryColor="#8BC34A", backgroundColor="#1C301C", 
        secondaryBackgroundColor="#2E482E", textColor="#E8F5E9", widgetBackgroundColor="#3A573A", 
        widgetBorderColor="#A5D6A7", skeletonBackgroundColor="#556B55", bodyFont=ThemeBaseDark.bodyFont,
        codeFont=ThemeBaseDark.codeFont, fontFaces=ThemeBaseDark.fontFaces
    )
)

# Custom Theme - HIDDEN/EDITABLE THEME (Starts based on dark theme)
custom_theme = ThemeInput(
    name="Custom Theme",
    icon="🖌️", 
    order=3,
    themeInfo=ThemeInfo(
        base=ThemeBaseDark.base, primaryColor="#FF5722", backgroundColor="#212121", 
        secondaryBackgroundColor="#3A3A3A", textColor="#FFFFFF", widgetBackgroundColor="#424242", 
        widgetBorderColor="#FF9800", skeletonBackgroundColor="#4E4E4E", bodyFont=ThemeBaseDark.bodyFont,
        codeFont=ThemeBaseDark.codeFont, fontFaces=ThemeBaseDark.fontFaces
    )
)


# Dictionary containing ALL themes (Core + Custom)
init_theme_data = {
    'garden_light': garden_light_theme,
    'garden_dark': garden_dark_theme,
    CUSTOM_THEME_KEY: custom_theme,
}


# 1. Initialize session state variables
if "theme_data" not in st.session_state:
    st.session_state["theme_data"] = init_theme_data

theme_data = st.session_state["theme_data"]


# 2. Theme Changer Initialization (Must run first to set the theme globally)
st_theme_changer(
    themes_data=theme_data, 
    render_mode="init", 
    default_init_theme_name=DEFAULT_INIT_THEME,
    key="theme_init"
)


# --- Settings Dialogue DEFINITION (using the @st.dialog decorator) ---

@st.dialog("App Settings", width="small")
def open_settings_dialog():
    """
    Defines the content shown inside the modal dialog.
    """
    # Removed st.header("App Settings") to fix the duplicate title issue.
    st.markdown("---")

    # 1. Quick Theme Picker (Excluding the hidden custom theme)
    st.subheader("🎨 Theme Switch")
    st.caption("Quickly switch between protected core themes.")
    
    # Filter the themes to only show selectable themes (excluding custom_theme_key)
    selectable_themes = {k: v for k, v in theme_data.items() if k != CUSTOM_THEME_KEY}

    # Renders the theme selection component
    st_theme_changer(
        themes_data=selectable_themes, 
        render_mode="pills",
        rerun_whole_st=True, 
        key="dialog_theme_picker"
    )
    
    st.markdown("---")

    # 2. Custom Theme Maker (Focus on the new custom_theme)
    with st.expander("🛠️ Custom Theme Maker", expanded=False):
        st.info("Edit the colors of the dedicated 'Custom Theme'. Saving changes automatically activates it.")
        
        current_theme = theme_data[CUSTOM_THEME_KEY]
        
        # --- START EDITING FORM for CUSTOM_THEME_KEY ---
        with st.form(key=f"edit_form_{CUSTOM_THEME_KEY}"):
            st.markdown(f"**Editing: {current_theme.name}**")
            
            # COLORS
            c1, c2 = st.columns(2)
            new_primary = c1.color_picker("Primary Color", current_theme.themeInfo.primaryColor)
            new_text = c2.color_picker("Text Color", current_theme.themeInfo.textColor)
            
            c3, c4 = st.columns(2)
            new_bg = c3.color_picker("Background", current_theme.themeInfo.backgroundColor)
            new_sec_bg = c4.color_picker("Sidebar/Secondary", current_theme.themeInfo.secondaryBackgroundColor)
            
            c5, c6 = st.columns(2)
            new_widget_bg = c5.color_picker("Widget Background", current_theme.themeInfo.widgetBackgroundColor)
            new_widget_border = c6.color_picker("Widget Border", current_theme.themeInfo.widgetBorderColor)

            # FONTS (Simple Text Inputs)
            st.markdown("---")
            st.caption("Font Settings")
            f1, f2 = st.columns(2)
            new_body_font = f1.text_input("Body Font", value=current_theme.themeInfo.bodyFont)
            new_code_font = f2.text_input("Code Font", value=current_theme.themeInfo.codeFont)

            # SAVE BUTTON
            if st.form_submit_button("💾 Save Changes and Apply"):
                # Update the session state object with new values
                theme_data[CUSTOM_THEME_KEY].themeInfo.primaryColor = new_primary
                theme_data[CUSTOM_THEME_KEY].themeInfo.textColor = new_text
                theme_data[CUSTOM_THEME_KEY].themeInfo.backgroundColor = new_bg
                theme_data[CUSTOM_THEME_KEY].themeInfo.secondaryBackgroundColor = new_sec_bg
                theme_data[CUSTOM_THEME_KEY].themeInfo.widgetBackgroundColor = new_widget_bg
                theme_data[CUSTOM_THEME_KEY].themeInfo.widgetBorderColor = new_widget_border
                theme_data[CUSTOM_THEME_KEY].themeInfo.bodyFont = new_body_font
                theme_data[CUSTOM_THEME_KEY].themeInfo.codeFont = new_code_font
                
                st.session_state["theme_data"] = theme_data
                
                # --- AUTO-SELECT CUSTOM THEME ---
                # We update the component's internal state to force selection of the newly edited theme.
                st.session_state["theme_init_active_theme"] = CUSTOM_THEME_KEY 
                st.toast("Custom theme saved and applied!")
                st.rerun()

    st.markdown("---")
    
    # 3. Music Option (Placeholder)
    st.subheader("🎵 Other Settings")
    st.toggle("Enable Background Music", value=False, disabled=True, help="Coming soon!")
    
    if st.button("Close Settings"):
        st.rerun()
        
# --- Main Application Layout ---

# Use columns to place the title and the settings button on the same line
col_title, col_settings = st.columns([10, 1])

with col_title:
    st.title("🌱 Grow a Garden Stock Dashboard")

with col_settings:
    # 4. Button to open the dialog
    if st.button("⚙️", key="settings_button"):
        open_settings_dialog()


# 5. Display main app content
st.header("Welcome!")
st.markdown(
    """
    This dashboard provides a simple structure to let you keep up with the **Grow a Garden** stock! ☘️

    Click the **'⚙️'** button above to open the settings dialog. You can customize the app's look by editing the **Custom Theme Maker**; saving changes will automatically apply your new look!

    ### Dashboard Pages
    - **🌾 Seed Stock:** Info on the current seeds in stock.
    - **🥚 Egg Stock:** Info on the current eggs in stock.
    - **⚙️ Gear Stock:** Info on the current gear in stock.
    - **✨ Cosmetic Sock:** Info on the current cosmetics in stock.
    - **🌥️ Weather and Mutations:** Info on the current weather and mutations that can be applied to your plants.
    """
)
