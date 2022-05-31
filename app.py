from email.headerregistry import AddressHeader
import streamlit as st
import cv2
import validators
import random
import streamlit.components.v1 as components


@st.cache
def load_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    return video_bytes


def main():
    st.title("Let’s Dance ヾ(⌐■_■)/♪♬")
    menu = ["Challenge", "Video upload", "Live record", "Video URL", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Challenge":
        st.subheader("Dance challenge of the day 💃🏻 🕺🏽")
        video_bytes = load_video('dancemachine_by_871/data/dance1.mp4')
        st.video(video_bytes)

    elif choice == "Video upload":
        st.subheader("Video Upload")
        video_file = st.file_uploader("Upload video", type=['mp4'])
        if video_file is not None:
            # To See Details
            file_details = {"Filename": video_file.name, "FileType": video_file.type, "FileSize": video_file.size}
            st.write(file_details)
            st.video(video_file)
            st.write(type(video_file))
            if st.button("Rate Me!"):
                mylist = ["Perfect", "Ok", "Terrible"]
                choice = random.choices(mylist)
                if choice[0] == "Perfect":
                    st.markdown(f'<h1 style="color:#00FF00;font-size:24px;">{"Perfect 🤩"}</h1>',
                                unsafe_allow_html=True)
                elif choice[0] == "Ok":
                    st.markdown(f'<h1 style="color:#FFFF00;font-size:24px;">{"It ok, keep trying 😕”"}</h1>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<h1 style="color:#8b0000;font-size:24px;">'
                                f'{"My grandmother dances better than that!! 💩"}</h1>',
                                unsafe_allow_html=True)

        else:
            st.write("wrong format!")

    elif choice == "Live record":
        st.title("Webcam Frames Live Record")
        run = st.checkbox('Run')
        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(0)

        while run:
            _, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
        else:
            st.write('Stopped')

    elif choice == "Video URL":
        st.title("Video URL")
        url = st.text_input(label='The URL link', type="default")
        if st.button("Load"):
            if validators.url(url):
                st.video(url)
            else:
                st.markdown(f'<h1 style="color:#8b0000;font-size:24px;">{"Invalid URL (✖╭╮✖)”"}</h1>',
                            unsafe_allow_html=True)

    else:
        st.subheader("About")
        components.html('''
        <div class="d-flex align-items-center my-" data-controller="ajax-form">
            <small><a target="blank" class="ml-2 btn text-underline" href="https://github.com/worldlife92/dancemachine_by_871">Github Repository</a></small>
          </div>
        <div class="d-flex align-items-center my-1" data-controller="ajax-form">
            <small><a target="blank" class="ml-2 btn text-underline" href="https://trello.com/invite/b/ZWB295OI/8395bd05d3cafe2b30cade4b350d6de7/dance-tutor">Project Dashboard</a></small>
        </div>
        ''')


if __name__ == '__main__':
    main()
