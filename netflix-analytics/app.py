import streamlit as st
from streamlit_option_menu import option_menu

# Custom CSS for Netflix theme
st.markdown("""
<style>
    .main {
        background-color: #000000;
        color: #ffffff;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #f40612;
        transform: scale(1.05);
    }
    .hero-section {
        text-align: center;
        padding: 50px 0;
        background: linear-gradient(135deg, #000000 0%, #e50914 100%);
        border-radius: 10px;
        margin-bottom: 30px;
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .hero-title {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 1.2em;
        margin-bottom: 30px;
        color: #cccccc;
    }
    .nav-bar {
        background-color: #000000;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .card {
        background-color: #141414;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(229, 9, 20, 0.2);
    }
    .metric-card {
        text-align: center;
        background-color: #e50914;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
    }
    .insight-card {
        background-color: #141414;
        border-left: 5px solid #e50914;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .insight-card:hover {
        background-color: #1a1a1a;
        transform: scale(1.02);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            max-width: 100%;
            padding: 0 10px;
        }
        .hero-title {
            font-size: 2em;
        }
        .hero-subtitle {
            font-size: 1.1em;
        }
        .stButton>button {
            padding: 8px 16px;
            font-size: 14px;
        }
        .metric-card {
            padding: 15px;
            margin: 5px;
        }
        .card {
            padding: 15px;
        }
        .insight-card {
            padding: 10px;
        }
    }

    @media (max-width: 480px) {
        .main {
            padding: 0 5px;
        }
        .hero-title {
            font-size: 1.5em;
        }
        .hero-subtitle {
            font-size: 1em;
        }
        .stButton>button {
            padding: 6px 12px;
            font-size: 12px;
        }
        .metric-card {
            padding: 10px;
            margin: 3px;
        }
        .card {
            padding: 10px;
        }
        .insight-card {
            padding: 8px;
        }
    }

    @media (min-width: 1200px) {
        .hero-title {
            font-size: 4em;
        }
        .hero-subtitle {
            font-size: 1.5em;
        }
        .stButton>button {
            padding: 12px 24px;
            font-size: 18px;
        }
        .metric-card {
            padding: 25px;
            margin: 15px;
        }
        .card {
            padding: 25px;
        }
        .insight-card {
            padding: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Navigation
# Check if buttons from home page triggered page change
if 'selected_page' in st.session_state:
    page_map = {"Home": 0, "Dashboard": 1, "Insights": 2, "About": 3}
    default_index = page_map.get(st.session_state.selected_page, 0)
    del st.session_state.selected_page  # Clear it after use
else:
    default_index = 0

selected = option_menu(
    menu_title=None,
    options=["Home", "Dashboard", "Insights", "About"],
    icons=["house", "bar-chart", "lightbulb", "info-circle"],
    menu_icon="cast",
    default_index=default_index,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000000"},
        "icon": {"color": "#e50914", "font-size": "25px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#e50914",
            "color": "#ffffff",
        },
        "nav-link-selected": {"background-color": "#e50914"},
    }
)

# Page routing
if selected == "Home":
    import pages.home as home
    home.show()
elif selected == "Dashboard":
    import pages.dashboard as dashboard
    dashboard.show()
elif selected == "Insights":
    import pages.insights as insights
    insights.show()
elif selected == "About":
    import pages.about as about
    about.show()
