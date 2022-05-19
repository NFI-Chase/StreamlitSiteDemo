import streamlit as st
import streamlit_book as stb
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import cv2

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
def clear_form():
    st.session_state["customerFeedbackName"] = ""
    st.session_state["customerFeedbackEmail"] = ""
    st.session_state["customerFeedbackMessage"] = ""
@st.cache
def sketch_img(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #applying median filter
    img_gray = cv2.medianBlur(img_gray,5)  
    #detecting the images
    edges = cv2.Laplacian(img_gray,cv2.CV_8U,ksize =5)  
    #threhold for images
    ret, thresholded = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV) 
    return thresholded
#cartoonize the images
@st.cache
def cartoonize_image(img, gray_mode = False):
    thresholded = sketch_img(img)
    #applying bilateral fliter wid big numbers to get cartoonnized
    filtered= cv2.bilateralFilter(img,10,250,250)
    cartoonized = cv2.bitwise_and(filtered, filtered, mask=thresholded)
    if gray_mode:
        return cv2.cvtColor(cartoonized, cv2.COLOR_BGR2GRAY)
    return cartoonized

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
    footer='<div class="footer">Developed with <b style="color:red";> ❤ </b> by Michael Strydom </br> Sponsor the Creator </br> <a href="https://paypal.me/michaelericstrydom" target="_blank">Michael Strydom</a></div>'
    st.markdown(footer,unsafe_allow_html=True)
logo = Image.open(r'resources/addYourImage.png')
profile = Image.open(r'resources/addYourImage.png')
if choose == "Photo Editing":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Bradley Hand'; color: #015249;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)
        
    with col2:               # To display brand logo
        st.image(logo,  width=200)
        
    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    option = st.selectbox('Edit Type',('','Sketch 1', 'Sketch 2', 'Grey', 'Cartoon', 'Cartoon Grey', 'PencilSketch Color', 'PencilSketch Gray','Stylized Image'))
    if uploaded_file is not None and option != '':
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=500)  
        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
            if option == 'Sketch 1':
                imageArray = np.array(image)
                custom_sketch_image = sketch_img(imageArray)
                st.image(custom_sketch_image,caption=f"Sketch Image",width=500)
            elif option == 'Sketch 2':
                converted_img = np.array(image.convert('RGB')) 
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                inv_gray = 255 - gray_scale
                blur_image = cv2.GaussianBlur(inv_gray, (125,125), 0, 0)
                sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                st.image(sketch, width=500)
            elif option == 'Grey':
                converted_img = np.array(image.convert('RGB'))
                grey_img=cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
                st.image(grey_img,caption=f"Grey",width=500)
            elif option == 'Cartoon':
                imageArray = np.array(image)
                custom_cartonized_image = cartoonize_image(imageArray)
                st.image(custom_cartonized_image,caption=f"Cartoonized Image",width=500)
            elif option == 'Cartoon Grey':
                imageArray = np.array(image)
                custom_cartonized_image_gray = cartoonize_image(imageArray, True)
                st.image(custom_cartonized_image_gray,caption=f"Cartoonized Image Gray",width=500)
            elif option == 'PencilSketch Color': 
                imageArray = np.array(image)
                sketch_gray, sketch_color = cv2.pencilSketch(imageArray, sigma_s=30, sigma_r=0.1, shade_factor=0.1)
                st.image(sketch_color,caption=f"Pencil Sketch Color",width=500)
            elif option == 'PencilSketch Gray': 
                imageArray = np.array(image) 
                sketch_gray, sketch_color = cv2.pencilSketch(imageArray, sigma_s=30, sigma_r=0.1, shade_factor=0.1)
                st.image(sketch_gray,caption=f"Pencil Sketch Gray",width=500)
            elif option == 'Stylized Image':
                imageArray = np.array(image)
                stylizated_image = cv2.stylization(imageArray, sigma_s=60, sigma_r=0.07)
                st.image(stylizated_image,caption=f"Stylized",width=500)
elif choose == "About":
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
        Name=st.text_input(label='Please Enter Your Name', key="customerFeedbackName")
        Email=st.text_input(label='Please Enter Email', key="customerFeedbackEmail")
        Message=st.text_input(label='Please Enter Your Message', key="customerFeedbackMessage")
        col1, col2 = st.columns([1,1])
        with col1:
            cleared = st.form_submit_button(label='Clear', on_click=clear_form)
        with col2:
            submitted = st.form_submit_button('Submit')
        if submitted:
            st.info('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')
            st.balloons()
        if cleared:
            st.info('Form Cleared')
# footer='<div class="footer">Developed with <b style="color:red";> ❤ </b> by Michael Strydom </br> Sponsor the Creator </br> <a href="https://paypal.me/michaelericstrydom" target="_blank">Michael Strydom</a></div>'
# st.markdown(footer,unsafe_allow_html=True)