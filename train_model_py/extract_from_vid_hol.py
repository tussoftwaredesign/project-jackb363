import cv2
import os
import util
import mediapipe as mp
import numpy as np
import math

# path to dataset and file list
root_dir = 'C:/Users/Jack/Documents/MediaPipe_SmallDataset'
root_dir_files = os.listdir(root_dir)

mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities


# function to extract numpy arrays from video frames
def extract_np_arr(section_root_dir):
    # mediapipe is used to extract keypoints from the video
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        # iterates over the categories in dataset
        for folder in section_root_dir:
            # gets all videos in a category
            vid_list = util.get_files(os.path.join(root_dir, folder))
            # iterates over each video in category
            for vid in vid_list:
                # creates dirs for each set of .npy files
                vid_dir = os.path.join(root_dir, folder, str(vid_list.index(vid)))
                if not os.path.exists(vid_dir):
                    os.mkdir(vid_dir)

                if not os.listdir(vid_dir):
                    # loads current vid to videocapture
                    cap = cv2.VideoCapture(os.path.join(root_dir, folder, vid))
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # get video width
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # get video height

                    # checks to see if a video is portrait, discarding if it is
                    if height < width:
                        frames_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        # iterates over each frame in a video
                        for frame_num in range(frames_length):
                            # Read feed
                            ret, frame = cap.read()
                            try:
                                # Make detections
                                image, results = util.mediapipe_detection(frame, holistic)
                                # get keypoints and save to .npy
                                keypoints = util.extract_keypoints_holistic(results)
                                # saves data keypoints to .npy file
                                npy_path = os.path.join(root_dir, folder,
                                                        str(vid_list.index(vid)), str(frame_num))
                                np.save(npy_path, keypoints)
                            except Exception as e:
                                break
                    else:
                        os.rmdir(vid_dir)
                    cap.release()
                    cv2.destroyAllWindows()
                print('category: ', folder)


if __name__ == '__main__':
    extract_np_arr(root_dir_files)

