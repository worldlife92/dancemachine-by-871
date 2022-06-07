import streamlit as st
import cv2
import validators
import random
import streamlit.components.v1 as components
from dancemachine_by_871.gcp import storage_upload
import os.path
from google.oauth2 import service_account
from google.cloud import storage
import requests
import hydralit_components as hc
from streamlit_option_menu import option_menu

@st.cache
def load_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    return video_bytes


def main():
    st.title("Let’s Dance ヾ(⌐■_■)/♪♬")
    with st.sidebar:
        choice = option_menu("Main Menu", ["The Challenge", 'Video Upload', 'Live Recording'],
                             icons=['house', 'arrow-bar-up', 'record2'], menu_icon="cast", default_index=0)

    # menu = ["Challenge", "Video upload", "Live record", "LR", "Video URL", "About"]
    # choice = st.sidebar.selectbox("Menu", menu)
    video_name = ""

    if choice == "The Challenge":
        st.subheader("Dance Challenge of the Day 💃🏻 🕺🏽")
        video_bytes = load_video('dancemachine_by_871/data/dance1.mp4')
        st.video(video_bytes)

    elif choice == "Video Upload":
        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = storage.Client(credentials=credentials)

        # Streamlit page
        st.subheader("Video Upload")
        video_file = st.file_uploader("Upload video", type=['mp4'])
        temp_path = "dancemachine_by_871/temp"
        if video_file is not None:
            # To See Details
            video_name = video_file.name
            st.video(video_file)

            # Save video to temp file
            # if not os.path.exists(temp_path):
            #     os.makedirs(temp_path)
            # with open(f"{temp_path}/{video_file.name}", "wb") as f:
            #     f.write(video_file.getbuffer())
            #     st.success("File Saved")

            # Upload video to gcp
            if os.path.exists(f"{temp_path}/{video_file.name}"):
                storage_upload(client, video_file.name, temp_path, True)
                st.success(f" Successfully uploaded '{video_name}'!")

            # Rate me button
            if st.button("Rate Me!"):
                params = {"filename": video_name}
                with hc.HyLoader('Checking out your dance moves...', loader_name=hc.Loaders.pacman):
                    response = requests.get('http://127.0.0.1:8000/predict', params=params)
                    status = response.status_code
                    result = response.json()

                if status == 200:
                    if result["score"] <= 50:
                        st.markdown(f'<h1 style="color:#8b0000;font-size:24px;">'
                                    f'"{result["score"]}% | \"My grandmother dances better than that!! 💩\""</h1>',
                                    unsafe_allow_html=True)
                    elif result["score"] <= 75:
                        st.markdown(f'<h1 style="color:#FFFF00;font-size:24px;">'
                                    f'"{result["score"]}% | \"Not bad! keep trying\""</h1>',
                                    unsafe_allow_html=True)
                    else:
                        st.markdown(f'<h1 style="color:#00FF00;font-size:24px;">{"Perfect 🤩"}</h1>',
                                    unsafe_allow_html=True)
                else:
                    st.error(f"Error {status} in request, couldn't rate '{video_name}'!")


    elif choice == "Live Recording":
        st.title("Webcam Frames Live Record")
        # run = st.checkbox('Run')
        frame_window = st.image([])
        camera = cv2.VideoCapture(0)

        active_record = False
        end_rec = True
        # vid_cod = cv2.VideoWriter_fourcc(*'mp4v')
        # vid_cod = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        output = cv2.VideoWriter(os.path.join(os.path.dirname(__file__),"cam_video.mp4"), -1,20.0, (640, 480))

        record = st.button('Start recording', disabled=active_record)
        end =  st.button('End recording', disabled=end_rec)


        while camera.isOpened():
            ret, frame = camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_window.image(frame)

                active_record = True
                output.write(frame)
                end_rec = False

            if end:
                break


        camera.release()
        output.release()
        cv2.destroyAllWindows()

    elif choice == "LR":
        st.title("Webcam Frames Live Record  II")
        cap = cv2.VideoCapture(0)

        # Define the codec and create VideoWriter object
        # fourcc = cv2.cv.CV_FOURCC(*'DIVX')
        # out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
        out = cv2.VideoWriter('output.avi', -1, 20.0, (640, 480))

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 0)

                # write the flipped frame
                out.write(
                    "/Users/ammarwanli/code/wanliammar/dancemachine_by_871/dancemachine_by_871/data/cam_video.mp4")

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

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
