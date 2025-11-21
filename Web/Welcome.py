import streamlit as st

# The st_theme_changer plugin is used for persistent, global theme management.
from streamlit_plugins.components.theme_changer import st_theme_changer
from streamlit_plugins.components.theme_changer.entity import ThemeInfo, ThemeInput, ThemeBaseLight, ThemeBaseDark

# --- Theme Definitions (Only 2 Core Themes) ---

# Garden Oasis (Light)
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

# Midnight Flora (Dark)
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

# Dictionary containing ONLY the 2 core themes
init_theme_data = {
    'garden_light': garden_light_theme,
    'garden_dark': garden_dark_theme,
}


# 1. Initialize session state variables
if "theme_data" not in st.session_state:
    st.session_state["theme_data"] = init_theme_data

theme_data = st.session_state["theme_data"]


# 2. Theme Changer Initialization (Must run first to set the theme globally)
st_theme_changer(
    themes_data=theme_data, 
    render_mode="init", 
    default_init_theme_name="garden_dark", # <-- Default is now set to dark mode
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

    # 1. Quick Theme Picker (The 2 Core Themes)
    st.subheader("🎨 Theme Switch")
    
    # Renders the theme selection component
    st_theme_changer(
        themes_data=theme_data, 
        render_mode="pills", # A clean, pill-shaped UI for switching
        rerun_whole_st=True, 
        key="dialog_theme_picker"
    )
    
    st.markdown("---")

    # 2. Custom Theme Maker (Fully Functional)
    with st.expander("🛠️ Custom Theme Maker", expanded=False):
        st.caption("Edit the properties of your themes below.")
        
        # Tabs for each theme available in the data
        theme_keys = list(theme_data.keys())
        tabs = st.tabs([theme_data[k].name for k in theme_keys])
        
        for i, tab in enumerate(tabs):
            theme_key = theme_keys[i]
            current_theme = theme_data[theme_key]
            
            with tab:
                # We use a form to prevent reload on every single color change
                with st.form(key=f"edit_form_{theme_key}"):
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
                    submitted = st.form_submit_button("Save Changes")
                    
                    if submitted:
                        # Update the session state object
                        theme_data[theme_key].themeInfo.primaryColor = new_primary
                        theme_data[theme_key].themeInfo.textColor = new_text
                        theme_data[theme_key].themeInfo.backgroundColor = new_bg
                        theme_data[theme_key].themeInfo.secondaryBackgroundColor = new_sec_bg
                        theme_data[theme_key].themeInfo.widgetBackgroundColor = new_widget_bg
                        theme_data[theme_key].themeInfo.widgetBorderColor = new_widget_border
                        theme_data[theme_key].themeInfo.bodyFont = new_body_font
                        theme_data[theme_key].themeInfo.codeFont = new_code_font
                        
                        st.session_state["theme_data"] = theme_data
                        
                        # Force a rerun to apply the new colors immediately
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
    This dashboard provides a simple structure to let you keep up the the grow a garden stock! ☘️

    Click the **'⚙️'** button above to open the theme selector dialog and choose your theme.

    ### Dashboard Pages
    - **🌾 Seed Stock:** Info on the current seeds in stock.
    - **🥚 Egg Stock:** Info on the current eggs in stock.
    - **⚙️ Gear Stock:** Info on the current gear in stock.
    - **🌥️ Weather and Mutations:** Info on the current weather and mutations that can be applied to your plants.
    """
)
