
import cv2
import mediapipe as mp
import numpy as np
import time
from tensorflow.keras.preprocessing.sequence import pad_sequences

"""Encoding of different Points of interest for mediapipe"""

NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32

MASKING = np.zeros((10,))
MASKING[:] = -20



class Preprocessor:

    def __init__(self, urls):
        self.urls = urls

    def unify_imgsize(self, frame, desired_width, desired_height):
        """Check the frames size and puts it into unified size by resizing/scaling/padding the image.
        Takes the image, desired_width and desired_height as input"""

        h,w, c = frame.shape

        if round(w/h, 2) < round(desired_width/desired_height, 2):

            new_width = int(desired_width/desired_height * h)
            frame = cv2.copyMakeBorder(frame, 0, 0, 0, new_width-w, cv2.BORDER_CONSTANT)

        elif round(w/h, 2) > round(desired_width/desired_height, 2):

            new_height = int(desired_height/desired_width * w)
            frame = cv2.copyMakeBorder(frame, 0, new_height-h, 0, 0, cv2.BORDER_CONSTANT)

        return cv2.resize(frame,(desired_width, desired_height), interpolation = cv2.INTER_CUBIC)



    def video_preprocess(self, videofile, frames=False, coords=False, showvideo=False,fps_desired=10, resize_width=480, resize_height=640):
        """Extracts the frames and coordinates of points of interest/joints from the dance video and returns
        a list of frames of the video and an np.array of coordinates with the joints."""

        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(videofile)

        #Initiating list to extract coordinates
        poi_coords = []

        #Initiating list to extract frames
        frames_lst = []

        vid_fps = cap.get(cv2.CAP_PROP_FPS)

        ## Setup mediapipe instance
        with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():

                if showvideo:
                    cv2.waitKey(1)

                ret, frame = cap.read()

                #Ends loop when video ends // avoids error message
                if ret == False:
                    cap.release()
                    cv2.destroyAllWindows()
                    break


                frames_lst.append(self.unify_imgsize(frame, resize_width,resize_height))

                #Implement resizing of frame https://theailearner.com/2018/11/15/changing-video-resolution-using-opencv-python/
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                interim = []
                try:
                    landmarks = results.pose_landmarks.landmark

                    for id, lm in enumerate(landmarks):
                        interim.append((lm.x, lm.y, lm.z))
                    poi_coords.append(interim)
                except:
                    pass

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                        )

                if showvideo:
                    cv2.imshow('Mediapipe Feed', image)

        new_fps = int(round(vid_fps/fps_desired))

        frames_lst = frames_lst[::new_fps]
        poi_coords = poi_coords[::new_fps]

        if frames and coords:
            return frames_lst, poi_coords

        elif frames == True and not coords:
            return frames_lst

        elif not frames and coords:
            return poi_coords

        else:
            return None



    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between(self, a,b,c):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::

                >>> angle_between((1, 0, 0), (0, 1, 0))
                1.5707963267948966
                >>> angle_between((1, 0, 0), (1, 0, 0))
                0.0
                >>> angle_between((1, 0, 0), (-1, 0, 0))
                3.141592653589793
        """
        a, b, c = np.array(a), np.array(b), np.array(c)

        v1_u = self.unit_vector(a-b)
        v2_u = self.unit_vector(c-b)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


    def angles(self, data):
        """Takes coordinates from video_preprocess function and outputs the data for the different angles"""
        return np.array([self.angle_between(data[LEFT_WRIST], data[LEFT_ELBOW], data[LEFT_SHOULDER]),\
        self.angle_between(data[LEFT_HIP], data[LEFT_SHOULDER], data[LEFT_ELBOW]),\
        self.angle_between(data[LEFT_SHOULDER], data[LEFT_HIP], data[LEFT_KNEE]),\
        self.angle_between(data[LEFT_HIP], data[LEFT_KNEE], data[LEFT_ANKLE]),\
        self.angle_between(data[LEFT_KNEE], data[LEFT_ANKLE], data[LEFT_FOOT_INDEX]),\
        self.angle_between(data[RIGHT_WRIST], data[RIGHT_ELBOW], data[RIGHT_SHOULDER]),\
        self.angle_between(data[RIGHT_HIP], data[RIGHT_SHOULDER], data[RIGHT_ELBOW]),\
        self.angle_between(data[RIGHT_SHOULDER], data[RIGHT_HIP], data[RIGHT_KNEE]),\
        self.angle_between(data[RIGHT_HIP], data[RIGHT_KNEE], data[RIGHT_ANKLE]),\
        self.angle_between(data[RIGHT_KNEE], data[RIGHT_ANKLE], data[RIGHT_FOOT_INDEX])])

    def extract_X_y_angles(self, y_val=0):
        """Extracting X & ys for a list of paths to video files. Set y_val to the correct y_val for the video"""

        X = []
        y = []
        pad_length = 0

        for ind, i in enumerate(self.urls):
            start = time.time()
            coords = self.video_preprocess(i, coords=True)

            jiggle_angles = []
            for i in coords:
                jiggle_angles.append(self.angles(i))

            X.append(np.array(jiggle_angles))
            y.append(y_val)
            print(f'Finished processing {ind+1} out of {len(self.urls)} in {round(time.time()-start, 2)} seconds.')

            if len(jiggle_angles) > pad_length:
                pad_length = len(jiggle_angles)

        return np.array(X), np.array(y), pad_length

    def create_X_y(self, Xs, ys, maxlenframes):
        """Takes a list of Xs, list of ys and maxlenframes from extract_angles
        function and creates X_padded and y, both which are concatenated from true and false dataset."""

        X_pad = pad_sequences(np.concatenate(Xs, axis=0), padding='post', maxlen=maxlenframes ,dtype='float64',value=MASKING)
        y = np.concatenate(ys, axis=0)

        return X_pad, y




if __name__ == '__main__':

    preproc = Preprocessor(['raw_data/jiggle.mp4'])
    print(preproc.extract_X_y_angles(1))
