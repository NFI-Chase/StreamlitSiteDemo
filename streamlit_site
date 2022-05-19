import streamlit as st
import streamlit_book as stb
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html

st.set_page_config(page_title="Chase Site",layout="wide",initial_sidebar_state="expanded")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
with st.sidebar:
    choose = option_menu("Apps", ["About", "Photo Editing", "Project Planning", "Screen Interactions", "Contact"],
        icons=['house', 'camera fill', 'kanban', 'calculator','envelope'],
        menu_icon="terminal", default_index=0,orientation="vertical",
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "#77C9D4", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#A5A5AF"},
            "nav-link-selected": {"background-color": "#015249"}}
    )
