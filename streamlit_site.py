import streamlit as st
import streamlit_book as stb
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image

st.set_page_config(page_title="Streamlit Demo Site",layout="wide",initial_sidebar_state="expanded")
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
local_css("resources/style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

with st.sidebar:
    choose = option_menu("Apps", ["Photo Editing", "Project Planning", "Screen Interactions", "About", "Contact"],
        icons=[ 'camera fill', 'kanban', 'calculator','info-square','envelope'],
        menu_icon="terminal", default_index=0,orientation="vertical",
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "#77C9D4", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#A5A5AF"},
            "nav-link-selected": {"background-color": "#015249"}}
    )
logo = Image.open(r'resources/addYourImage.png')
profile = Image.open(r'resources/addYourImage.png')
if choose == "About":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown('<p class="fontPageHeadings">About the Creator</p>', unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=200 )
    
    st.markdown('<p>Michael Strydom is a Integration Specialist, architect and coding enthusiast.</p>', unsafe_allow_html=True) 
    st.markdown('<p>✔ From South Africa.</br> ✔ Age : How old do you want me to be.</br> ✔ Married to the most beautiful woman alive</br> ✔ Studied at University of Johannesburg</br> ✔ Graduated in BSc. Informatics and Computer Science with Endorsed Mathematics</p>', unsafe_allow_html=True)   
    st.image(profile, width=300 )
elif choose == "Contact":
    st.markdown('<p class="fontPageHeadings">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name')
        Email=st.text_input(label='Please Enter Email')
        Message=st.text_input(label='Please Enter Your Message')
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.markdown('<p>Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!</p>', unsafe_allow_html=True)
    
footer='<div class="footer">Developed with <b style="color:red";> ❤ </b> by Michael Strydom </br> Sponsor the Creator </br> <a href="https://paypal.me/michaelericstrydom" target="_blank">Michael Strydom</a></div>'
st.markdown(footer,unsafe_allow_html=True)