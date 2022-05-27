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
import time
import random
from streamlit_quill import st_quill
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
from streamlit_folium import st_folium
import folium
from stmol import showmol
import py3Dmol
from streamlit_cropper import st_cropper
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
def clear_contact_form():
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
    choose = option_menu("Apps", ["Home","Photo Editor", "Image Crop","Text Editor","Maps","3D Modeling", "Project Planning", "QR Generator", "About", "Contact", "Additional", "Admin"],
        icons=[ 'house','camera fill','crop','pen','map','badge-3d', 'kanban', 'calculator','info-square','envelope','cloud-plus','box-arrow-in-right'],
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
if choose == "Home":
    st.markdown('<p class="fontPageHeadings">Home</p>', unsafe_allow_html=True)
    url = "https://www.youtube.com/watch?v=0ESc1bh3eIg"
    col1, col2, col3 = st.columns( [0.5, 0.5,0.5])
    with col1:
        st.write("")
    with col2:
        st.video(url,start_time=1080)
    with col3:
        st.write("")  
    def init(post_init=False):
        if not post_init:
            st.session_state.opponent = 'Human'
            st.session_state.win = {'X': 0, 'O': 0}
        st.session_state.board = np.full((3, 3), '.', dtype=str)
        st.session_state.player = 'X'
        st.session_state.warning = False
        st.session_state.winner = None
        st.session_state.over = False


    def check_available_moves(extra=False) -> list:
        raw_moves = [row for col in st.session_state.board.tolist() for row in col]
        num_moves = [i for i, spot in enumerate(raw_moves) if spot == '.']
        if extra:
            return [(i // 3, i % 3) for i in num_moves]
        return num_moves


    def check_rows(board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return None


    def check_diagonals(board):
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            return board[0][0]
        if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
            return board[0][len(board) - 1]
        return None


    def check_state():
        if st.session_state.winner:
            st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")
        if st.session_state.warning and not st.session_state.over:
            st.warning('⚠️ This move already exist')
        if st.session_state.winner and not st.session_state.over:
            st.session_state.over = True
            st.session_state.win[st.session_state.winner] = (
                st.session_state.win.get(st.session_state.winner, 0) + 1
            )
        elif not check_available_moves() and not st.session_state.winner:
            st.info(f'It\'s a tie 📍')
            st.session_state.over = True


    def check_win(board):
        for new_board in [board, np.transpose(board)]:
            result = check_rows(new_board)
            if result:
                return result
        return check_diagonals(board)


    def computer_player():
        moves = check_available_moves(extra=True)
        if moves:
            i, j = random.choice(moves)
            handle_click(i, j)


    def handle_click(i, j):
        if (i, j) not in check_available_moves(extra=True):
            st.session_state.warning = True
        elif not st.session_state.winner:
            st.session_state.warning = False
            st.session_state.board[i, j] = st.session_state.player
            st.session_state.player = "O" if st.session_state.player == "X" else "X"
            winner = check_win(st.session_state.board)
            if winner != ".":
                st.session_state.winner = winner

    def main():
        st.write(
            """
            # ❎🅾️ Tic Tac Toe
            """
        )
        if "board" not in st.session_state:
            init()
        reset, score, player, settings = st.columns([0.5, 0.6, 1, 1])
        reset.button('New game', on_click=init, args=(True,))

        with settings.expander('Settings'):
            st.write('**Warning**: changing this setting will restart your game')
            st.selectbox(
                'Set opponent',
                ['Human', 'Computer'],
                key='opponent',
                on_change=init,
                args=(True,),
            )

        for i, row in enumerate(st.session_state.board):
            cols = st.columns([5, 1, 1, 1, 5])
            for j, field in enumerate(row):
                cols[j + 1].button(
                    field,
                    key=f"{i}-{j}",
                    on_click=handle_click
                    if st.session_state.player == 'X'
                    or st.session_state.opponent == 'Human'
                    else computer_player(),
                    args=(i, j),
                )

        check_state()

        score.button(f'❌{st.session_state.win["X"]} 🆚 {st.session_state.win["O"]}⭕')
        player.button(
            f'{"❌" if st.session_state.player == "X" else "⭕"}\'s turn'
            if not st.session_state.winner
            else f'🏁 Game finished'
        )
    if __name__ == '__main__':
        main()  
elif choose == "Photo Editor":
    st.markdown('<p class="fontPageHeadings">Photo Editor</p>', unsafe_allow_html=True)
    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    option = st.selectbox('Edit Type',('','Sketch 1', 'Sketch 2', 'Sketch 3', 'Grey', 'Invert'))
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
elif choose == "Image Crop":
    st.markdown('<p class="fontPageHeadings">Image Crop</p>', unsafe_allow_html=True)
    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict[aspect_choice]
    if img_file:
        img = Image.open(img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend
        cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)
        # Manipulate cropped image at will
        st.write("Preview")
        _ = cropped_img.thumbnail((250,250))
        st.image(cropped_img,width=500)
elif choose == "Text Editor":
    st.markdown('<p class="fontPageHeadings">Text Editor</p>', unsafe_allow_html=True)
    st.markdown('<p class="title3">Quill Editor</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    c2.subheader("Parameters")
    with c1:
        content = st_quill(
            placeholder="Write your text here",
            html=c2.checkbox("Return HTML", False),
            readonly=c2.checkbox("Read only", False),
            key="quill",
        )
        if content:
            st.subheader("Content")
            st.text(content)
    st.markdown('<p class="title3">Ace Editor</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    c2.subheader("Parameters")
    with c1:
        content = st_ace(placeholder=c2.text_input("Editor placeholder", value="Write your code here"),
            language=c2.selectbox("Language mode", options=LANGUAGES, index=121),theme=c2.selectbox("Theme", options=THEMES, index=35),
            keybinding=c2.selectbox("Keybinding mode", options=KEYBINDINGS, index=3),font_size=c2.slider("Font size", 5, 24, 14),
            tab_size=c2.slider("Tab size", 1, 8, 4),show_gutter=c2.checkbox("Show gutter", value=True),
            show_print_margin=c2.checkbox("Show print margin", value=False),wrap=c2.checkbox("Wrap enabled", value=False),
            auto_update=c2.checkbox("Auto update", value=False),readonly=c2.checkbox("Read-only", value=False),
            min_lines=45,key="ace",
        )
        if content:
            st.subheader("Content")
            st.text(content)
elif choose == "Maps":
    st.markdown('<p class="fontPageHeadings">Maps</p>', unsafe_allow_html=True)
    m = folium.Map(location=[52.379189, 4.899431], zoom_start=16)
    folium.Marker([52.379189, 4.899431], popup="Amsterdam Centraal", tooltip="Amsterdam Centraal").add_to(m)
    st_data = st_folium(m, width = 1000)
elif choose == "3D Modeling":
    st.markdown('<p class="fontPageHeadings">3D Modeling</p>', unsafe_allow_html=True)
    st.sidebar.title('Show Proteins')
    prot_str='1A2C,1BML,1D5M,1D5X,1D5Z,1D6E,1DEE,1E9F,1FC2,1FCC,1G4U,1GZS,1HE1,1HEZ,1HQR,1HXY,1IBX,1JBU,1JWM,1JWS'
    prot_list=prot_str.split(',')
    bcolor = st.sidebar.color_picker('Pick A Color', '#FFFFFF')
    protein=st.sidebar.selectbox('select protein',prot_list)
    style = st.sidebar.selectbox('style',['line','cross','stick','sphere','cartoon','clicksphere'])
    xyzview = py3Dmol.view(query='pdb:'+protein)
    xyzview.setStyle({style:{'color':'spectrum'}})
    xyzview.setBackgroundColor(bcolor)
    showmol(xyzview, height = 500,width=800)
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
            fig.update_xaxes(tickangle=0, tickfont=dict(family='Rockwell', color='#77C9D4', size=13))
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
        gif_qr_size=st.number_input(label='Please Enter the size of Image (default: 100):', key="qrSize",value=100, min_value=100, max_value=500, step=50)
        gif_transition_duration=st.number_input(label='GIF transition duration (default: 0.30):', key="gifTrasitionDuration",value=0.30, min_value=0.10, max_value=3.5, step=0.20)
    with col2:
        qr_type = st.selectbox('QR Code Type',('','Automation Color', 'Automation BW', 'Plain QR'))
        qr_version = st.selectbox('QR Code Version (Size)',(1,2,3,4,5,6,7,8,9,10))
        qr_destination_link=st.text_input(label='QR Data:', key="qrDestinationLink",max_chars=100)
    if gif_qr_size == '':
        gif_qr_size = 100
    if gif_transition_duration == '':
        gif_transition_duration = 0.30
    images = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image = image.resize((gif_qr_size,gif_qr_size))
        images.append(image)
    if images:
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            #do GIF  
            st.markdown('<p class="title3">GIF Result</p>', unsafe_allow_html=True)  
            output = io.BytesIO()
            imageio.mimwrite(output, images, "gif", duration=gif_transition_duration)
            data_url = base64.b64encode(output.getvalue()).decode("utf-8")
            imageio.mimsave('gifResult.gif', images, duration=gif_transition_duration)
            st.markdown(f'</br> <img src="data:image/gif;base64,{data_url}" alt="Output GIF">',unsafe_allow_html=True,)
            st.download_button(label='Download GIF', data=output, file_name='gifResult.gif', mime='image/gif' )
        with col2:
            #do QR
            if qr_type != '' and qr_version != '' and qr_destination_link != '':
                saved_qr_name = 'tempQR.gif'
                st.markdown('<p class="title3">QR Code Result</p>', unsafe_allow_html=True)
                if qr_type == 'Automation Color' and qr_destination_link and qr_version:
                    version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,level='H',picture="gifResult.gif", colorized=True,contrast=1.0,brightness=1.0,save_name=saved_qr_name)
                    qrLoad = Image.open(saved_qr_name)
                    data_url, data = load_qrcode_to_base64(qrLoad, 'gif')
                    st.markdown(f'</br> <img src="data:image/gif;base64,{data_url}" alt="Output QR">',unsafe_allow_html=True,)
                    st.download_button(label='Download QR Code', data=data, file_name='qrCodeResult.gif', mime='image/gif' )
                    if qrLoad : qrLoad.close()
                elif qr_type == 'Automation BW' and qr_destination_link and qr_version:
                    version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,level='H',picture="gifResult.gif", colorized=False,contrast=1.0,brightness=1.0,save_name=saved_qr_name)
                elif qr_type == 'Plain QR'and qr_destination_link:
                    version, level, qr_name = amzqr.run(words=qr_destination_link,save_name=saved_qr_name,)
                os.remove('gifResult.gif')
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
        Name=st.text_input(label='Please Enter Your Name', key="customerFeedbackName",max_chars=100)
        Email=st.text_input(label='Please Enter Email', key="customerFeedbackEmail",max_chars=100)
        Message=st.text_input(label='Please Enter Your Message', key="customerFeedbackMessage",max_chars=200)
        col1, col2 = st.columns([1,1])
        with col1:
            cleared = st.form_submit_button(label='Clear', on_click=clear_contact_form)
        with col2:
            submitted = st.form_submit_button('Submit')
        if submitted:
            st.info('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')
            st.balloons()
        if cleared:
            st.info('Form Cleared')
elif choose == "Additional":
    st.markdown('<p class="fontPageHeadings">Additional Projects</p>', unsafe_allow_html=True)
    link='Code Gallery [link](https://streamlit.io/gallery)'
    st.markdown(link,unsafe_allow_html=True)
    link='Bug Report [link](https://share.streamlit.io/streamlit/example-app-bug-report/main) Github [link](https://github.com/streamlit/example-app-bug-report)'
    st.markdown(link,unsafe_allow_html=True)
    code = '''# Bug Report
        import google_auth_httplib2
        import httplib2
        import pandas as pd
        import streamlit as st
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import HttpRequest

        SCOPE = "https://www.googleapis.com/auth/spreadsheets"
        SPREADSHEET_ID = "1QlPTiVvfRM82snGN6LELpNkOwVI1_Mp9J9xeJe-QoaA"
        SHEET_NAME = "Database"
        GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"


        @st.experimental_singleton()
        def connect_to_gsheet():
            # Create a connection object.
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=[SCOPE],
            )

            # Create a new Http() object for every request
            def build_request(http, *args, **kwargs):
                new_http = google_auth_httplib2.AuthorizedHttp(
                    credentials, http=httplib2.Http()
                )
                return HttpRequest(new_http, *args, **kwargs)

            authorized_http = google_auth_httplib2.AuthorizedHttp(
                credentials, http=httplib2.Http()
            )
            service = build(
                "sheets",
                "v4",
                requestBuilder=build_request,
                http=authorized_http,
            )
            gsheet_connector = service.spreadsheets()
            return gsheet_connector


        def get_data(gsheet_connector) -> pd.DataFrame:
            values = (
                gsheet_connector.values()
                .get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"{SHEET_NAME}!A:E",
                )
                .execute()
            )

            df = pd.DataFrame(values["values"])
            df.columns = df.iloc[0]
            df = df[1:]
            return df


        def add_row_to_gsheet(gsheet_connector, row) -> None:
            gsheet_connector.values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=f"{SHEET_NAME}!A:E",
                body=dict(values=row),
                valueInputOption="USER_ENTERED",
            ).execute()


        st.set_page_config(page_title="Bug report", page_icon="🐞", layout="centered")

        st.title("🐞 Bug report!")

        gsheet_connector = connect_to_gsheet()

        st.sidebar.write(
            f"This app shows how a Streamlit app can interact easily with a [Google Sheet]({GSHEET_URL}) to read or store data."
        )

        st.sidebar.write(
            f"[Read more](https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet) about connecting your Streamlit app to Google Sheets."
        )

        form = st.form(key="annotation")

        with form:
            cols = st.columns((1, 1))
            author = cols[0].text_input("Report author:")
            bug_type = cols[1].selectbox(
                "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
            )
            comment = st.text_area("Comment:")
            cols = st.columns(2)
            date = cols[0].date_input("Bug date occurrence:")
            bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
            submitted = st.form_submit_button(label="Submit")


        if submitted:
            add_row_to_gsheet(
                gsheet_connector,
                [[author, bug_type, comment, str(date), bug_severity]],
            )
            st.success("Thanks! Your bug was recorded.")
            st.balloons()

        expander = st.expander("See all records")
        with expander:
            st.write(f"Open original [Google Sheet]({GSHEET_URL})")
            st.dataframe(get_data(gsheet_connector))'''   
    st.code(code, language='python')
    link='NYC Uber Ridesharing Data [link](https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main) Github [link](https://github.com/streamlit/demo-uber-nyc-pickups)'
    st.markdown(link,unsafe_allow_html=True)
    code = '''# -*- coding: utf-8 -*-
        # Copyright 2018-2022 Streamlit Inc.
        #
        # Licensed under the Apache License, Version 2.0 (the "License");
        # you may not use this file except in compliance with the License.
        # You may obtain a copy of the License at
        #
        #    http://www.apache.org/licenses/LICENSE-2.0
        #
        # Unless required by applicable law or agreed to in writing, software
        # distributed under the License is distributed on an "AS IS" BASIS,
        # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        # See the License for the specific language governing permissions and
        # limitations under the License.

        """An example of showing geographic data."""

        import streamlit as st
        import pandas as pd
        import numpy as np
        import altair as alt
        import pydeck as pdk

        # SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
        st.set_page_config(layout="wide", page_title="NYC Ridesharing Demo", page_icon=":taxi:")

        # LOAD DATA ONCE
        @st.experimental_singleton
        def load_data():
            data = pd.read_csv(
                "uber-raw-data-sep14.csv.gz",
                nrows=100000,  # approx. 10% of data
                names=[
                    "date/time",
                    "lat",
                    "lon",
                ],  # specify names directly since they don't change
                skiprows=1,  # don't read header since names specified directly
                usecols=[0, 1, 2],  # doesn't load last column, constant value "B02512"
                parse_dates=[
                    "date/time"
                ],  # set as datetime instead of converting after the fact
            )

            return data


        # FUNCTION FOR AIRPORT MAPS
        def map(data, lat, lon, zoom):
            st.write(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": lat,
                        "longitude": lon,
                        "zoom": zoom,
                        "pitch": 50,
                    },
                    layers=[
                        pdk.Layer(
                            "HexagonLayer",
                            data=data,
                            get_position=["lon", "lat"],
                            radius=100,
                            elevation_scale=4,
                            elevation_range=[0, 1000],
                            pickable=True,
                            extruded=True,
                        ),
                    ],
                )
            )


        # FILTER DATA FOR A SPECIFIC HOUR, CACHE
        @st.experimental_memo
        def filterdata(df, hour_selected):
            return df[df["date/time"].dt.hour == hour_selected]


        # CALCULATE MIDPOINT FOR GIVEN SET OF DATA
        @st.experimental_memo
        def mpoint(lat, lon):
            return (np.average(lat), np.average(lon))


        # FILTER DATA BY HOUR
        @st.experimental_memo
        def histdata(df, hr):
            filtered = data[
                (df["date/time"].dt.hour >= hr) & (df["date/time"].dt.hour < (hr + 1))
            ]

            hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]

            return pd.DataFrame({"minute": range(60), "pickups": hist})


        # STREAMLIT APP LAYOUT
        data = load_data()

        # LAYING OUT THE TOP SECTION OF THE APP
        row1_1, row1_2 = st.columns((2, 3))

        with row1_1:
            st.title("NYC Uber Ridesharing Data")
            hour_selected = st.slider("Select hour of pickup", 0, 23)

        with row1_2:
            st.write(
                """
            ##
            Examining how Uber pickups vary over time in New York City's and at its major regional airports.
            By sliding the slider on the left you can view different slices of time and explore different transportation trends.
            """
            )

        # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
        row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))

        # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
        la_guardia = [40.7900, -73.8700]
        jfk = [40.6650, -73.7821]
        newark = [40.7090, -74.1805]
        zoom_level = 12
        midpoint = mpoint(data["lat"], data["lon"])

        with row2_1:
            st.write(
                f"""**All New York City from {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
            )
            map(filterdata(data, hour_selected), midpoint[0], midpoint[1], 11)

        with row2_2:
            st.write("**La Guardia Airport**")
            map(filterdata(data, hour_selected), la_guardia[0], la_guardia[1], zoom_level)

        with row2_3:
            st.write("**JFK Airport**")
            map(filterdata(data, hour_selected), jfk[0], jfk[1], zoom_level)

        with row2_4:
            st.write("**Newark Airport**")
            map(filterdata(data, hour_selected), newark[0], newark[1], zoom_level)

        # CALCULATING DATA FOR THE HISTOGRAM
        chart_data = histdata(data, hour_selected)

        # LAYING OUT THE HISTOGRAM SECTION
        st.write(
            f"""**Breakdown of rides per minute between {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
        )

        st.altair_chart(
            alt.Chart(chart_data)
            .mark_area(
                interpolate="step-after",
            )
            .encode(
                x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
                y=alt.Y("pickups:Q"),
                tooltip=["minute", "pickups"],
            )
            .configure_mark(opacity=0.2, color="red"),
            use_container_width=True,
        )'''
    st.code(code, language='python')
    link='Diploma PDF Generator [link](https://share.streamlit.io/streamlit/example-app-pdf-report/main) Github [link](https://github.com/streamlit/example-app-pdf-report)'
    st.markdown(link,unsafe_allow_html=True)
    code = '''# Diploma PDF Generator
        import pdfkit
        from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
        from datetime import date
        import streamlit as st
        from streamlit.components.v1 import iframe

        st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
        st.title("🎓 Diploma PDF Generator")

        st.write(
            "This app shows you how you can use Streamlit to make a PDF generator app in just a few lines of code!"
        )

        left, right = st.columns(2)

        right.write("Here's the template we'll be using:")

        right.image("template.png", width=300)

        env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
        template = env.get_template("template.html")


        left.write("Fill in the data:")
        form = left.form("template_form")
        student = form.text_input("Student name")
        course = form.selectbox(
            "Choose course",
            ["Report Generation in Streamlit", "Advanced Cryptography"],
            index=0,
        )
        grade = form.slider("Grade", 1, 100, 60)
        submit = form.form_submit_button("Generate PDF")

        if submit:
            html = template.render(
                student=student,
                course=course,
                grade=f"{grade}/100",
                date=date.today().strftime("%B %d, %Y"),
            )

            pdf = pdfkit.from_string(html, False)
            st.balloons()

            right.success("🎉 Your diploma was generated!")
            # st.write(html, unsafe_allow_html=True)
            # st.write("")
            right.download_button(
                "⬇️ Download PDF",
                data=pdf,
                file_name="diploma.pdf",
                mime="application/octet-stream",
            )'''
    st.code(code, language='python')
    link='JAVA: New Programming Jargon [link](https://blog.codinghorror.com/new-programming-jargon/)'
    st.markdown(link,unsafe_allow_html=True)
    code = '''//Finding a position to insert the numeric element in the array
        import java.util.Arrays;
        public class GFG {
            public static void main(String[] args)
            {
                int[] arr = new int[] { 1, 3, 4, 5, 6 };
        
                // 2 has to be inserted
                int pos = Arrays.binarySearch(arr, 2);
                System.out.print("Element has to be inserted at: " + ~pos);
            }
        }'''
    st.code(code, language='Java')
    link='Image Carousel with Streamlit and Typescript(NodeJS) [link](https://github.com/DenizDogan92/Streamlit-Image-Carousel)'
    st.markdown(link,unsafe_allow_html=True)
elif choose == "Admin":
    def loginPage():
        users = {"test":"test"}
        st.markdown('<p class="fontPageHeadings">ADMIN Login:</p>', unsafe_allow_html=True)
        with st.form(key='login_form'):
            if "username" not in st.session_state:
                email = st.text_input("Username or e-mail",max_chars=100)
                password = st.text_input("Password", type="password",max_chars=100)
            submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if email.lower() in users and users[email.lower()] == password:
                st.success("👍 Succesfully logged in! :tada:")
                st.session_state.logged_in = True
                with st.spinner("Redirecting to application..."):
                        time.sleep(1)
                        st.experimental_rerun()
            else:
                st.error("👎 Unsuccessful Logon! 😔")
    if "logged_in" in st.session_state and st.session_state.logged_in == True:
        if st.button('Logout', key='adminLogout'):
            st.session_state.logged_in = False
            st.legacy_caching.clear_cache()
            st.experimental_rerun()
        def _tabs(tabs_data = {}, default_active_tab=0):
            tab_titles = list(tabs_data.keys())
            if not tab_titles:
                return None
            active_tab = st.radio("", tab_titles, index=default_active_tab)
            child = tab_titles.index(active_tab)+1
            st.markdown("""  
                <style type="text/css">
                div[role=radiogroup] > label > div:first-of-type {
                display: none
                }
                div[role=radiogroup] {
                    flex-direction: unset
                }
                div[role=radiogroup] label {             
                    border: 1px solid #black;
                    background: black;
                    padding: 4px 12px;
                    border-radius: 4px 4px 0 0;
                    position: relative;
                    top: 1px;
                    }
                div[role=radiogroup] label:nth-child(""" + str(child) + """) {    
                    background: #77C9D4 !important;
                    border-bottom: 1px solid transparent;
                }            
                </style>
            """,unsafe_allow_html=True)        
            return tabs_data[active_tab]

        def _show_video():
            st.title("Russia – Ukraine conflict / crisis Explained")
            st.video("https://www.youtube.com/watch?v=h2P9AmGcMdM")

        def _fake_df():
            N = 50
            rand = pd.DataFrame()
            rand['a'] = np.arange(N)
            rand['b'] = np.random.rand(N)
            rand['c'] = np.random.rand(N)    
            return rand

        def do_tabs():
            st.markdown("Welcome User")
            tab_content = _tabs({
                    "Tab html": "<h2> Hello Streamlit, <br/> what a cool tool! </h2>",
                    "Tab video": _show_video, 
                    "Tab df": _fake_df()
                })
            if callable(tab_content):
                tab_content()
            elif type(tab_content) == str:
                st.markdown(tab_content, unsafe_allow_html=True)
            else:
                st.write(tab_content)
        do_tabs()
    if "logged_in" not in st.session_state:
        loginPage()
    if "logged_in" in st.session_state and st.session_state.logged_in == False:
        loginPage() 

# footer='<div class="footer">Developed with <b style="color:red";> ❤ </b> by Michael Strydom </br> Sponsor the Creator </br> <a href="https://paypal.me/michaelericstrydom" target="_blank">Michael Strydom</a></div>'
# st.markdown(footer,unsafe_allow_html=True)