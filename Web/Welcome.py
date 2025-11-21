import streamlit as st

# Import the necessary classes from Streamlit Plugins
from streamlit_plugins.components.theme_changer import get_active_theme_key, st_theme_changer
from streamlit_plugins.components.theme_changer.entity import ThemeInfo, ThemeInput, ThemeBaseLight, ThemeBaseDark

# --- Theme Definitions (53 Themes) ---

# --- Core Themes (3) ---

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

# System Default (Auto) - This is always mandatory for theme changer auto-detection
system_default_theme = ThemeInput(
    name="System Default (Auto)",
    icon="✨", 
    order=0, 
    themeInfo=garden_light_theme.themeInfo 
)


# --- 50 EXTRA THEMES (Hidden/Editable "Notepad" Themes) ---
extra_themes_data = dict(
    forest_moss=ThemeInput(name="Forest Moss", icon="🍄", order=10, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#558B2F", backgroundColor="#1B5E20", secondaryBackgroundColor="#388E3C", textColor="#E8F5E9", widgetBackgroundColor="#4CAF50", widgetBorderColor="#8BC34A", skeletonBackgroundColor="#66BB6A")),
    desert_dusk=ThemeInput(name="Desert Dusk", icon="🏜️", order=11, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#FFAB40", backgroundColor="#424242", secondaryBackgroundColor="#5D4037", textColor="#FFECB3", widgetBackgroundColor="#795548", widgetBorderColor="#FFB74D", skeletonBackgroundColor="#A1887F")),
    sky_serenity=ThemeInput(name="Sky Serenity", icon="☁️", order=12, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#03A9F4", backgroundColor="#E1F5FE", secondaryBackgroundColor="#B3E5FC", textColor="#212121", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#4FC3F7", skeletonBackgroundColor="#81D4FA")),
    ocean_mist=ThemeInput(name="Ocean Mist", icon="🐋", order=13, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#00BCD4", backgroundColor="#E0F7FA", secondaryBackgroundColor="#B2EBF2", textColor="#006064", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#4DD0E1", skeletonBackgroundColor="#80DEEA")),
    mountain_peak=ThemeInput(name="Mountain Peak", icon="🏔️", order=14, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#607D8B", backgroundColor="#F5F5F5", secondaryBackgroundColor="#CFD8DC", textColor="#263238", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#90A4AE", skeletonBackgroundColor="#B0BEC5")),
    volcano_ash=ThemeInput(name="Volcano Ash", icon="🌋", order=15, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#FF9800", backgroundColor="#212121", secondaryBackgroundColor="#424242", textColor="#FFCC80", widgetBackgroundColor="#616161", widgetBorderColor="#FFB74D", skeletonBackgroundColor="#757575")),
    lavender_field=ThemeInput(name="Lavender Field", icon="💜", order=16, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#9C27B0", backgroundColor="#F3E5F5", secondaryBackgroundColor="#E1BEE7", textColor="#4A148C", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#CE93D8", skeletonBackgroundColor="#E1BEE7")),
    golden_hour=ThemeInput(name="Golden Hour", icon="🌅", order=17, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FFC107", backgroundColor="#FFFDE7", secondaryBackgroundColor="#FFF9C4", textColor="#FF6F00", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FFD54F", skeletonBackgroundColor="#FFF176")),
    deep_sea=ThemeInput(name="Deep Sea", icon="🔱", order=18, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#0097A7", backgroundColor="#00334C", secondaryBackgroundColor="#004D66", textColor="#B2EBF2", widgetBackgroundColor="#006080", widgetBorderColor="#4DB6AC", skeletonBackgroundColor="#80CBC4")),
    stone_gray=ThemeInput(name="Stone Gray", icon="🗿", order=19, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#757575", backgroundColor="#FAFAFA", secondaryBackgroundColor="#EEEEEE", textColor="#424242", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#BDBDBD", skeletonBackgroundColor="#D6D6D6")),
    amethyst_dark=ThemeInput(name="Amethyst Dark", icon="🔮", order=20, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#D81B60", backgroundColor="#311B92", secondaryBackgroundColor="#4527A0", textColor="#F8BBD0", widgetBackgroundColor="#512DA8", widgetBorderColor="#8E24AA", skeletonBackgroundColor="#7E57C2")),
    emerald_light=ThemeInput(name="Emerald Light", icon="💎", order=21, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#00C853", backgroundColor="#E8F5E9", secondaryBackgroundColor="#C8E6C9", textColor="#1B5E20", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#69F0AE", skeletonBackgroundColor="#A5D6A7")),
    ruby_red=ThemeInput(name="Ruby Red", icon="❤️", order=22, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#F44336", backgroundColor="#3F0000", secondaryBackgroundColor="#5C0000", textColor="#FFCDD2", widgetBackgroundColor="#790000", widgetBorderColor="#EF9A9A", skeletonBackgroundColor="#E57373")),
    sapphire_deep=ThemeInput(name="Sapphire Deep", icon="🔷", order=23, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#2979FF", backgroundColor="#0D47A1", secondaryBackgroundColor="#1565C0", textColor="#BBDEFB", widgetBackgroundColor="#1976D2", widgetBorderColor="#64B5F6", skeletonBackgroundColor="#90CAF9")),
    polished_steel=ThemeInput(name="Polished Steel", icon="⚙️", order=24, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#78909C", backgroundColor="#ECEFF1", secondaryBackgroundColor="#CFD8DC", textColor="#455A64", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#B0BEC5", skeletonBackgroundColor="#D0D0D0")),
    brushed_aluminum=ThemeInput(name="Brushed Aluminum", icon="🔩", order=25, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#B0BEC5", backgroundColor="#37474F", secondaryBackgroundColor="#455A64", textColor="#ECEFF1", widgetBackgroundColor="#546E7A", widgetBorderColor="#78909C", skeletonBackgroundColor="#90A4AE")),
    copper_patina=ThemeInput(name="Copper Patina", icon="💰", order=26, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#BF360C", backgroundColor="#FBE9E7", secondaryBackgroundColor="#FFCCBC", textColor="#4E342E", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FF8A65", skeletonBackgroundColor="#FFAB91")),
    jade_green=ThemeInput(name="Jade Green", icon="🟢", order=27, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#1DE9B6", backgroundColor="#E0F2F1", secondaryBackgroundColor="#B2DFDB", textColor="#004D40", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#64FFDA", skeletonBackgroundColor="#84FFFF")),
    opal_white=ThemeInput(name="Opal White", icon="⚪", order=28, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#80CBC4", backgroundColor="#FFFFFF", secondaryBackgroundColor="#F0F0F0", textColor="#424242", widgetBackgroundColor="#FAFAFA", widgetBorderColor="#B2DFDB", skeletonBackgroundColor="#D6D6D6")),
    obsidian=ThemeInput(name="Obsidian", icon="⚫", order=29, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#757575", backgroundColor="#0A0A0A", secondaryBackgroundColor="#1F1F1F", textColor="#E0E0E0", widgetBackgroundColor="#333333", widgetBorderColor="#424242", skeletonBackgroundColor="#616161")),
    vaporwave=ThemeInput(name="Vaporwave", icon="🌃", order=30, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#FF00FF", backgroundColor="#000033", secondaryBackgroundColor="#330055", textColor="#00FFFF", widgetBackgroundColor="#550077", widgetBorderColor="#FF4081", skeletonBackgroundColor="#8800AA")),
    cyberpunk=ThemeInput(name="Cyberpunk", icon="🤖", order=31, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#00E676", backgroundColor="#000000", secondaryBackgroundColor="#1A1A1A", textColor="#FFEB3B", widgetBackgroundColor="#333333", widgetBorderColor="#FF3D00", skeletonBackgroundColor="#69F0AE")),
    soft_glow=ThemeInput(name="Soft Glow", icon="💡", order=32, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FF80AB", backgroundColor="#FFF3E0", secondaryBackgroundColor="#FFCCBC", textColor="#795548", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FFAB91", skeletonBackgroundColor="#FFE0B2")),
    fire_ice=ThemeInput(name="Fire & Ice", icon="🔥", order=33, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#E53935", backgroundColor="#000033", secondaryBackgroundColor="#1E88E5", textColor="#FFEBEE", widgetBackgroundColor="#424242", widgetBorderColor="#FF8A80", skeletonBackgroundColor="#90CAF9")),
    solarized_dark=ThemeInput(name="Solarized Dark", icon="⚫", order=34, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#2AA198", backgroundColor="#002B36", secondaryBackgroundColor="#073642", textColor="#839496", widgetBackgroundColor="#073642", widgetBorderColor="#B58900", skeletonBackgroundColor="#586E75")),
    solarized_light=ThemeInput(name="Solarized Light", icon="⚪", order=35, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#2AA198", backgroundColor="#FDF6E3", secondaryBackgroundColor="#EEE8D5", textColor="#657B83", widgetBackgroundColor="#EEE8D5", widgetBorderColor="#B58900", skeletonBackgroundColor="#839496")),
    monokai=ThemeInput(name="Monokai", icon="💻", order=36, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#FFD700", backgroundColor="#272822", secondaryBackgroundColor="#49483E", textColor="#F8F8F2", widgetBackgroundColor="#49483E", widgetBorderColor="#F92672", skeletonBackgroundColor="#75715E")),
    material_deep_purple=ThemeInput(name="Material Purple", icon="🟣", order=37, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#673AB7", backgroundColor="#21004A", secondaryBackgroundColor="#450090", textColor="#E1BEE7", widgetBackgroundColor="#6A1B9A", widgetBorderColor="#9575CD", skeletonBackgroundColor="#AB47BC")),
    atomic_tangerine=ThemeInput(name="Atomic Tangerine", icon="🟠", order=38, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FF9800", backgroundColor="#FFF3E0", secondaryBackgroundColor="#FFCCBC", textColor="#E65100", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FFAB91", skeletonBackgroundColor="#FFCC80")),
    dark_chocolate=ThemeInput(name="Dark Chocolate", icon="🍫", order=39, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#A1887F", backgroundColor="#3E2723", secondaryBackgroundColor="#4E342E", textColor="#D7CCC8", widgetBackgroundColor="#5D4037", widgetBorderColor="#BCAAA4", skeletonBackgroundColor="#795548")),
    concrete=ThemeInput(name="Concrete", icon="🏗️", order=40, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#607D8B", backgroundColor="#F5F5F5", secondaryBackgroundColor="#E0E0E0", textColor="#263238", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#B0BEC5", skeletonBackgroundColor="#CFD8DC")),
    chalkboard=ThemeInput(name="Chalkboard", icon="✍️", order=41, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#8BC34A", backgroundColor="#212121", secondaryBackgroundColor="#303030", textColor="#CFD8DC", widgetBackgroundColor="#424242", widgetBorderColor="#E0E0E0", skeletonBackgroundColor="#757575")),
    paper_white=ThemeInput(name="Paper White", icon="📄", order=42, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#9E9E9E", backgroundColor="#FFFFFF", secondaryBackgroundColor="#FAFAFA", textColor="#212121", widgetBackgroundColor="#F5F5F5", widgetBorderColor="#E0E0E0", skeletonBackgroundColor="#BDBDBD")),
    ink_black=ThemeInput(name="Ink Black", icon="🖊️", order=43, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#B0BEC5", backgroundColor="#000000", secondaryBackgroundColor="#111111", textColor="#FAFAFA", widgetBackgroundColor="#212121", widgetBorderColor="#333333", skeletonBackgroundColor="#424242")),
    beige_canvas=ThemeInput(name="Beige Canvas", icon="🖼️", order=44, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#A1887F", backgroundColor="#F5F5DC", secondaryBackgroundColor="#EFEFEF", textColor="#5D4037", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#D7CCC8", skeletonBackgroundColor="#EFEBE9")),
    graphite=ThemeInput(name="Graphite", icon="⚫", order=45, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#757575", backgroundColor="#1A1A1A", secondaryBackgroundColor="#262626", textColor="#E0E0E0", widgetBackgroundColor="#333333", widgetBorderColor="#424242", skeletonBackgroundColor="#616161")),
    skyline=ThemeInput(name="Skyline", icon="🏢", order=46, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#26A69A", backgroundColor="#F5F5F5", secondaryBackgroundColor="#E0F2F1", textColor="#37474F", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#80CBC4", skeletonBackgroundColor="#B2DFDB")),
    warehouse=ThemeInput(name="Warehouse", icon="🏭", order=47, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FFB74D", backgroundColor="#F0F0F0", secondaryBackgroundColor="#E0E0E0", textColor="#5D4037", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FFD54F", skeletonBackgroundColor="#FFECB3")),
    night_shift=ThemeInput(name="Night Shift", icon="🌙", order=48, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#90CAF9", backgroundColor="#101010", secondaryBackgroundColor="#212121", textColor="#E0F7FA", widgetBackgroundColor="#333333", widgetBorderColor="#64B5F6", skeletonBackgroundColor="#424242")),
    clean_room=ThemeInput(name="Clean Room", icon="🧼", order=49, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#4DB6AC", backgroundColor="#FFFFFF", secondaryBackgroundColor="#F5F5F5", textColor="#004D40", widgetBackgroundColor="#FAFAFA", widgetBorderColor="#80CBC4", skeletonBackgroundColor="#B2DFDB")),
    coffee_steam=ThemeInput(name="Coffee Steam", icon="☕", order=50, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#795548", backgroundColor="#FBE9E7", secondaryBackgroundColor="#EFEBE9", textColor="#3E2723", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#A1887F", skeletonBackgroundColor="#D7CCC8")),
    matcha_latte=ThemeInput(name="Matcha Latte", icon="🍵", order=51, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#689F38", backgroundColor="#F9FFF5", secondaryBackgroundColor="#DCEDC8", textColor="#33691E", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#A5D6A7", skeletonBackgroundColor="#C5E1A5")),
    berry_sorbet=ThemeInput(name="Berry Sorbet", icon="🍓", order=52, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#E91E63", backgroundColor="#FCE4EC", secondaryBackgroundColor="#F8BBD0", textColor="#AD1457", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#F48FB1", skeletonBackgroundColor="#F48FB1")),
    lemon_zest=ThemeInput(name="Lemon Zest", icon="🍋", order=53, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FFEB3B", backgroundColor="#FFFDE7", secondaryBackgroundColor="#FFF9C4", textColor="#F57F17", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FFEE58", skeletonBackgroundColor="#FFF176")),
    gingerbread=ThemeInput(name="Gingerbread", icon="🍪", order=54, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#BF360C", backgroundColor="#5D4037", secondaryBackgroundColor="#795548", textColor="#FFCCBC", widgetBackgroundColor="#8D6E63", widgetBorderColor="#FF8A65", skeletonBackgroundColor="#A1887F")),
    mint_chocolate=ThemeInput(name="Mint Chocolate", icon="🍫", order=55, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#66BB6A", backgroundColor="#263238", secondaryBackgroundColor="#37474F", textColor="#E0F2F1", widgetBackgroundColor="#455A64", widgetBorderColor="#80CBC4", skeletonBackgroundColor="#B2DFDB")),
    grape_soda=ThemeInput(name="Grape Soda", icon="🍇", order=56, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#7B1FA2", backgroundColor="#301A4B", secondaryBackgroundColor="#4A2F6F", textColor="#E1BEE7", widgetBackgroundColor="#6A3D9E", widgetBorderColor="#BA68C8", skeletonBackgroundColor="#CE93D8")),
    cherry_cola=ThemeInput(name="Cherry Cola", icon="🍒", order=57, themeInfo=ThemeInfo(base=ThemeBaseDark.base, primaryColor="#D32F2F", backgroundColor="#212121", secondaryBackgroundColor="#424242", textColor="#FFCDD2", widgetBackgroundColor="#616161", widgetBorderColor="#EF9A9A", skeletonBackgroundColor="#9E9E9E")),
    pumpkin_spice=ThemeInput(name="Pumpkin Spice", icon="🎃", order=58, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FF7043", backgroundColor="#FFF3E0", secondaryBackgroundColor="#FFCCBC", textColor="#E65100", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#FFAB91", skeletonBackgroundColor="#FFD54F")),
    ice_cream=ThemeInput(name="Ice Cream", icon="🍦", order=59, themeInfo=ThemeInfo(base=ThemeBaseLight.base, primaryColor="#FF8A80", backgroundColor="#FFFAFA", secondaryBackgroundColor="#F8BBD0", textColor="#4A148C", widgetBackgroundColor="#FFFFFF", widgetBorderColor="#E1BEE7", skeletonBackgroundColor="#FFE0B2")),
)


# --- Combine All Themes for Session State ---

init_theme_data = dict(
    system_default_theme=system_default_theme,
    garden_light=garden_light_theme,
    garden_dark=garden_dark_theme,
)
# Merge the 50 extra themes into the main dictionary for editor access
init_theme_data.update(extra_themes_data)


# --- Define Main Themes for the Quick Picker (Only the 3 Core ones) ---
# THIS DICTIONARY ONLY CONTAINS THE CORE THEMES
main_themes_for_picker = {
    'system_default_theme': system_default_theme,
    'garden_light': garden_light_theme,
    'garden_dark': garden_dark_theme,
}


# --- Application Logic ---

# 1. Initialize session state variables
if "theme_data" not in st.session_state:
    st.session_state["theme_data"] = init_theme_data
if "show_settings_dialog" not in st.session_state:
    st.session_state["show_settings_dialog"] = False

theme_data = st.session_state["theme_data"]


# 2. Theme Changer Initialization (Must run first to set the theme)
st_theme_changer(themes_data=theme_data, render_mode="init", default_init_theme_name="system_default_theme", key="theme_init")


# --- Settings Dialogue (st.dialog) Logic ---

def render_settings_dialog():
    """
    Renders the content of the st.dialog.
    """
    global theme_data # Access the global theme data

    st.header("App Settings")
    st.markdown("---")

    # --- Theme Picker (Only the Core Themes) ---
    st.subheader("🎨 Quick Theme Switch")
    st.markdown("Switch between the core Light and Dark themes.")
    
    # *** NOTICE: This uses the restricted 'main_themes_for_picker' dictionary (3 themes) ***
    st_theme_changer(
        themes_data=main_themes_for_picker, 
        render_mode="pills",
        rerun_whole_st=True, 
        key="dialog_theme_picker"
    )
    
    # --- Music Option (Placeholder) ---
    st.subheader("🎵 Music & Sound")
    st.info("Music option placeholder (No functionality yet)")
    
    st.markdown("---")

    # --- Theme Editor UI (The "Notepad" for all 53 themes) ---
    # This section contains the full "notepad" editor functionality
    with st.expander("🛠️ Custom Theme Maker (50+ Themes)", expanded=False):
        st.info("This are your extra themes. All 53 defined themes are here. Select a tab to edit and save its properties.")
        
        with st.container(border=False):
            # Sort themes by order for consistent tab display
            theme_keys = sorted(theme_data.keys(), key=lambda k: theme_data[k])
