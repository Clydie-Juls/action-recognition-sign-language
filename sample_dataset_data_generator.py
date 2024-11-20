import cv2
import numpy as np
import os
import urllib.request
from pytube import YouTube
import ffmpeg
import json
import utils


# downloads video's via url if possible
def download_video(url, download_path):
    # Check if the URL is for a YouTube video
    if 'youtube.com' in url or 'youtu.be' in url:
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            file_name = stream.default_filename
            downloaded_video_path = os.path.join(download_path, file_name)
            stream.download(download_path)
            print(f"YouTube video downloaded: {downloaded_video_path}")
            return downloaded_video_path
        except Exception as e:
            print(f"Error downloading YouTube video: {e}")
            return None

    # Check if the URL points to an MP4 file
    elif url.endswith('.mp4'):
        try:
            file_name = url.split('/')[-1]
            downloaded_video_path = os.path.join(download_path, file_name)
            urllib.request.urlretrieve(url, downloaded_video_path)
            print(f"MP4 video downloaded: {downloaded_video_path}")
            return downloaded_video_path
        except Exception as e:
            print(f"Error downloading MP4 video: {e}")
            return None

    elif url.endswith('.swf'):
        try:
            file_name = os.path.basename(url)
            downloaded_video_path = os.path.join(download_path, file_name)
            ffmpeg.input(url).output(downloaded_video_path).run()
            print(f"SWF video converted to MP4: {downloaded_video_path}")
            return downloaded_video_path
        except Exception as e:
            print(f"Error converting SWF to MP4: {e}")
            return None
    else:
        return None


DATASET_PATH = os.path.join('dataset', "WLASL_v0.3.json")

# read JSON data
with open(DATASET_PATH, 'r') as data:
    dt = json.load(data)
    min = 90000000
    vid_locs = {}
    for i in range(3, 6):
        instance_ids = []
        instances_json = dt[i]['instances']
        for instance in instances_json:
            instance_ids.append([instance['video_id'], instance['url']])
            vid_locs[dt[i]['gloss']] = instance_ids

for gloss, ids in vid_locs.items():
    try:
        os.makedirs(os.path.join('images', gloss))
    except:
        pass

# Set mediapipe model
for gloss, instances in vid_locs.items():
    for instance in instances:
        VID_PATH = os.path.join('dataset', 'videos', f"{instance[0]}.mp4")
        cap = cv2.VideoCapture(VID_PATH)
        frame_cnt = 0
        print(id)
        if not cap.isOpened():
            url_vid_path = download_video(instance[1], os.path.join("downloaded_images"))
            if url_vid_path is not None:
                cap = cv2.VideoCapture(url_vid_path)

        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if length < utils.no_of_frames:
            continue
        with utils.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while cap.isOpened() and frame_cnt < utils.no_of_frames:

                # Read feed
                ret, frame = cap.read()
                if not ret:
                    print("Done")
                    break

                # Make detections
                image, results = utils.mediapipe_detection(frame, holistic)
                print(results)

                # Draw landmarks
                utils.draw_styled_landmarks(image, results)

                # Show to screen
                cv2.imshow('OpenCV Feed', image)

                keypoints = utils.extract_keypoints(results)
                try:
                    os.makedirs(os.path.join('images', gloss, str(instance[0])))
                except:
                    pass
                npy_path = os.path.join('images', gloss, str(instance[0]), str(frame_cnt))
                np.save(npy_path, keypoints)
                frame_cnt += 1
                # Break gracefully
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
cap.release()
cv2.destroyAllWindows()
