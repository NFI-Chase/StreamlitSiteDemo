import streamlit as st
import streamlit_book as stb
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html

st.set_page_config(page_title="Streamlit Demo Site",layout="wide",initial_sidebar_state="expanded")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
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
if choose == "Contact":
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Bradley Hand'; color: #015249;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
        Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
        Email=st.text_input(label='Please Enter Email') #Collect user feedback
        Message=st.text_input(label='Please Enter Your Message') #Collect user feedback
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')
footer="""<style>
a:link , a:visited{
color: #015249;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0E1117;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with <b style="color:red";> ❤ </b> by Michael Strydom</p> <p> Sponsor the Creator  <a style='display: block; text-align: center;' href="https://paypal.me/michaelericstrydom" target="_blank">Michael Strydom</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)