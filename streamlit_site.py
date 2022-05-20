import streamlit as st
import streamlit_book as stb
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image, ImageSequence
import numpy as np
import cv2
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px
import io
import imageio
import base64,os
from io import BytesIO
from amzqr import amzqr

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
def remake_qrcode(qr_img):
        crop_size = 27
        new_img = qr_img.crop((crop_size, crop_size, qr_img.size[0] - crop_size, qr_img.size[1] - crop_size)) 
        return new_img
def load_qrcode_to_base64(qrLoad, format):
    buf = BytesIO()
    if format == 'jpg':
        crop_size = 27
        qrLoad = qrLoad.crop((crop_size, crop_size, qrLoad.size[0] - crop_size, qrLoad.size[1] - crop_size)) 
        qrLoad.save(buf, format = 'JPG')
        base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
        return base64_str
    elif format == 'gif':
        info = qrLoad.info
        sequence = [remake_qrcode(f.copy()) for f in ImageSequence.Iterator(qrLoad)]
        sequence[0].save(buf, format='GIF', save_all=True,append_images=sequence[1:], disposal=2,quality=100, **info)
        # base64_str =  f'base64://{base64.b64encode(buf.getvalue()).decode()}'
        url_data = base64.b64encode(buf.getvalue()).decode("utf-8")
        return url_data, buf.getvalue()
with st.sidebar:
    choose = option_menu("Apps", ["Photo Editor", "Project Planning", "QR Generator", "About", "Contact"],
        icons=[ 'camera fill', 'kanban', 'calculator','info-square','envelope'],
        menu_icon="terminal", default_index=0,orientation="vertical",
        styles={"container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "#77C9D4", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#A5A5AF"},
            "nav-link-selected": {"background-color": "#015249"}}
    )
    footer='<div class="footer">Developed with <b style="color:red";> ❤ </b> by Michael Strydom </br> Sponsor the Creator </br> <a href="https://paypal.me/michaelericstrydom" target="_blank">Michael Strydom</a></div>'
    st.markdown(footer,unsafe_allow_html=True)
logo = Image.open(r'resources/addYourImage.png')
profile = Image.open(r'resources/addYourImage.png')
if choose == "Photo Editor":
    st.markdown('<p class="fontPageHeadings">Photo Editor</p>', unsafe_allow_html=True)
    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    option = st.selectbox('Edit Type',('','Sketch 1', 'Sketch 2', 'Sketch 3', 'Grey', 'Invert', 'Cartoon', 'Cartoon Grey', 'PencilSketch Color', 'PencilSketch Gray','Stylized Image'))
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
            elif option == 'Invert':
                converted_img = np.array(image.convert('RGB'))
                grey_img=cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
                invert_img=cv2.bitwise_not(grey_img)
                st.image(invert_img,caption=f"Invert",width=500)
            elif option == 'Sketch 3':
                converted_img = np.array(image.convert('RGB'))
                grey_img=cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
                invert_img=cv2.bitwise_not(grey_img)
                blur_img=cv2.GaussianBlur(invert_img, (111,111),0)
                invblur_img=cv2.bitwise_not(blur_img)
                sketch_img=cv2.divide(grey_img,invblur_img, scale=256.0)
                st.image(sketch_img,caption=f"Sketch Image",width=500)
            # elif option == 'Cartoon':
            #     imageArray = np.array(image)
            #     custom_cartonized_image = cartoonize_image(imageArray)
            #     st.image(custom_cartonized_image,caption=f"Cartoonized Image",width=500)
            # elif option == 'Cartoon Grey':
            #     imageArray = np.array(image)
            #     custom_cartonized_image_gray = cartoonize_image(imageArray, True)
            #     st.image(custom_cartonized_image_gray,caption=f"Cartoonized Image Gray",width=500)
            # elif option == 'PencilSketch Color': 
            #     imageArray = np.array(image)
            #     sketch_gray, sketch_color = cv2.pencilSketch(imageArray, sigma_s=30, sigma_r=0.1, shade_factor=0.1)
            #     st.image(sketch_color,caption=f"Pencil Sketch Color",width=500)
            # elif option == 'PencilSketch Gray': 
            #     imageArray = np.array(image) 
            #     sketch_gray, sketch_color = cv2.pencilSketch(imageArray, sigma_s=30, sigma_r=0.1, shade_factor=0.1)
            #     st.image(sketch_gray,caption=f"Pencil Sketch Gray",width=500)
            # elif option == 'Stylized Image':
            #     imageArray = np.array(image)
            #     stylizated_image = cv2.stylization(imageArray, sigma_s=60, sigma_r=0.07)
            #     st.image(stylizated_image,caption=f"Stylized",width=500)
elif choose == "Project Planning":
    st.markdown('<p class="fontPageHeadings">Upload your project plan file and generate Gantt chart</p>', unsafe_allow_html=True)
    st.markdown('<p class="title3">Step 1: Download the project plan template</p>', unsafe_allow_html=True)
    image = Image.open(r'resources/templatePicture.png')
    st.image(image,  caption='Example of how the file should be completed')
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    df=pd.read_csv(r'resources/projectTemplate.csv')
    csv = convert_df(df)
    st.download_button(label="Download Template", data=csv, file_name='Project_Template.csv', mime='text/csv',)
    #Add a file uploader to allow users to upload their project plan file
    st.markdown('<p class="title3">Step 2: Upload your project plan</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Fill out the project plan template and upload your file here. After you upload the file, you can edit your project plan within the app.", type=['csv'], key="2")
    if uploaded_file is not None:
        Tasks=pd.read_csv(uploaded_file)
        Tasks['Start'] = Tasks['Start'].astype('datetime64')
        Tasks['Finish'] = Tasks['Finish'].astype('datetime64')
        grid_response = AgGrid(Tasks, editable=True, height=300, width='100%',)
        updated = grid_response['data']
        df = pd.DataFrame(updated) 
        if st.button('Generate Gantt Chart'): 
            fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color='Completion Pct', hover_name="Task Description")
            fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       
            fig.update_layout(title='Project Plan Gantt Chart',
                            hoverlabel_bgcolor='#DAEEED',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                            bargap=0.2, height=600, xaxis_title="", yaxis_title="",                   
                            title_x=0.5,                    #Make title centered                     
                            xaxis=dict(tickfont_size=15, tickangle = 270, rangeslider_visible=True,
                                    side ="top",            #Place the tick labels on the top of the chart
                                    showgrid = True, zeroline = True, showline = True, showticklabels = True,
                                    tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                    )
                        )
            fig.update_xaxes(tickangle=0, tickfont=dict(family='Rockwell', color='blue', size=15))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<p class="title3">Step 3 : Export Interactive Gantt chart to HTML</p>', unsafe_allow_html=True) #Allow users to export the Plotly chart to HTML
            buffer = io.StringIO()
            fig.write_html(buffer, include_plotlyjs='cdn')
            html_bytes = buffer.getvalue().encode()
            st.download_button(label='Export to HTML', data=html_bytes, file_name=uploaded_file.name + '.html', mime='text/html' ) 
        else:
            st.write('---')
elif choose == "QR Generator":
    st.markdown('<p class="fontPageHeadings">QR Code Generator</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("",accept_multiple_files=True, type=['jpg','png','jpeg'])
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        gif_qr_size=st.text_input(label='Please Enter the size of Image (default: 100):', key="qrSize")
        gif_transition_duration=st.text_input(label='GIF transition duration (default: 0.30):', key="gifTrasitionDuration")
    with col2:
        qr_type = st.selectbox('QR Code Type',('','Automation Color', 'Automation BW', 'Plain QR'))
        qr_version = st.selectbox('QR Code Version',(1,2,3,4,5,6))
        qr_destination_link=st.text_input(label='QR Data:', key="qrDestinationLink")
    images = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image = image.resize((250,250))
        images.append(image)
    if images:
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            #do GIF  
            st.markdown('<p class="title3">GIF Result</p>', unsafe_allow_html=True)  
            output = io.BytesIO()
            imageio.mimwrite(output, images, "gif", duration=0.30)
            data_url = base64.b64encode(output.getvalue()).decode("utf-8")
            imageio.mimsave('gifResult.gif', images, duration=0.30)
            st.markdown(f'</br> <img src="data:image/gif;base64,{data_url}" alt="Output GIF">',unsafe_allow_html=True,)
            st.download_button(label='Download GIF', data=output, file_name='gifResult.gif', mime='image/gif' )
        with col2:
            #do QR
            saved_qr_name = 'tempQR.gif'
            st.markdown('<p class="title3">QR Code Result</p>', unsafe_allow_html=True)
            if qr_type == 'Automation Color' and qr_destination_link and qr_version:
                version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,level='H',picture="gifResult.gif", colorized=True,contrast=1.0,brightness=1.0,save_name=saved_qr_name)
                qrLoad = Image.open(saved_qr_name)
                data_url, data = load_qrcode_to_base64(qrLoad, 'gif')
                st.markdown(f'</br> <img src="data:image/gif;base64,{data_url}" alt="Output QR">',unsafe_allow_html=True,)
                st.download_button(label='Download QR Code', data=data, file_name='qrCodeResult.gif', mime='image/gif' )
            elif qr_type == 'Automation BW' and qr_destination_link and qr_version:
                version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,level='H',picture="gifResult.gif", colorized=False,contrast=1.0,brightness=1.0,save_name=saved_qr_name)
            elif qr_type == 'Plain QR'and qr_destination_link:
                version, level, qr_name = amzqr.run(words=qr_destination_link,save_name=saved_qr_name,)
            os.remove('gifResult.gif')
            qrLoad.close()
            os.remove(saved_qr_name)
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