# streamlit app for creating gifs from images
import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import os
import imageio
import base64
from PIL import Image
import numpy as np
from sqlalchemy.orm import sessionmaker
from moviepy.editor import *

from database import engine, Gif
save_loc = 'generated'

def open_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def main():
    st.title("Gif Creator")
    st.write("Upload images to create a gif")

    # select gif creation method
    gif_creation_method = st.selectbox("Select gif creation method", ["Images", "Video"])

    if gif_creation_method == "Images":
        uploaded_files = st.file_uploader("Upload Files", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, use_column_width=True)
        if st.button("Create Gif"):
            create_gif_from_images(uploaded_files)
    elif gif_creation_method == "Video":
        video_file = st.file_uploader("Upload Video", type=["mp4"])
        fps = st.number_input("Enter fps", min_value=1, max_value=100, value=10)
        start = st.number_input("Enter start time", min_value=0, max_value=100, value=0)
        end = st.number_input("Enter end time", min_value=0, max_value=100, value=10)
        if video_file is not None:
            video_bytes = video_file.read()
            st.video(video_bytes)
        if st.button("Create Gif"):
            create_gif_from_video(video_file, fps, start, end)

def increment_file_name(file_name):
    file_name, file_extension = os.path.splitext(file_name)
    file_name = file_name.split('_')
    if len(file_name) > 1 and file_name[-1].isdigit():
        file_name[-1] = str(int(file_name[-1]) + 1)
    else:
        file_name.append('1')
    file_name = '_'.join(file_name)
    return file_name + file_extension

def create_gif_from_images(uploaded_files):
    images = []
    for uploaded_file in uploaded_files:
        images.append(imageio.imread(uploaded_file))
    path = os.path.join(save_loc, increment_file_name('content.gif'))
    imageio.mimsave(path, images, duration=0.01)
    with open(path, 'rb') as f:
        data = f.read()
    st.markdown("### Gif")
    st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(data).decode()}" alt="cat gif" width="600">', unsafe_allow_html=True)   
    st.markdown(get_binary_file_downloader_html(path, 'Download Gif'), unsafe_allow_html=True)
    save_to_db(path)

def create_gif_from_video(video_file, fps, start, end):
    video = save_video(video_file)
    clip = VideoFileClip(video).subclip(start, end)
    path = os.path.join(save_loc, increment_file_name('content.gif'))
    clip.write_gif(path, fps=fps)
    with open(path, 'rb') as f:
        data = f.read() 
    st.markdown("### Gif")
    st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(data).decode()}" alt="cat gif" width="600">', unsafe_allow_html=True)
    st.markdown(get_binary_file_downloader_html(path, 'Download Gif'), unsafe_allow_html=True)


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:file/txt;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href

def save_video(video_file):
    with open(os.path.join(save_loc, video_file.name), 'wb') as f:
        f.write(video_file.getbuffer())
    return os.path.join(save_loc, video_file.name)

def save_to_db(path):
    session = open_db()
    gif = Gif(name=path.split('\\')[-1], path=path)
    session.add(gif)
    session.commit()




__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    
    main()




# streamlit run app.py
