from email.headerregistry import AddressHeader
import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd
import docx2txt
from PIL import Image


@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img


def main():
    st.title("Let’s Dance ヾ(⌐■_■)/♪♬")

    menu = ["Challenge", "Video upload", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Challenge":
        st.subheader("Dance challenge of the day 💃🏻 🕺🏽")
        video_file = open('dancemachine_by_871/data/dance1.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    elif choice == "Video upload":
        st.subheader("Video upload")
        video_file = st.file_uploader("Upload video", type=['mp4'])
        if video_file is not None:
            # To See Details
            file_details = {"Filename": video_file.name, "FileType": video_file.type, "FileSize": video_file.size}
            st.write(file_details)

            vid = load_image(video_file)
            st.image(vid, width=250, height=250)

    else:
        st.subheader("About")
        st.info("Built with Streamlit")
        st.info("Jesus Saves @JCharisTech")
        st.text("Jesse E.Agbe(JCharis)")


if __name__ == '__main__':
    main()
