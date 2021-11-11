import cv2
import numpy as np
import math
from PIL import Image as im
from tqdm import tqdm
import pytube

max_samples = 1280

def download_video(video_id):
    link = 'http://www.youtube.com/watch?v=' + video_id
    print("Downloading", link)
    yt = pytube.YouTube(link)
    yt.streams.filter(progressive=True, file_extension='mp4')[0].download(filename="barcode.mp4")
    return True

def gen_image(total_samples, filename):
    total_samples = int(total_samples)
    path = 'barcode.mp4'
    video = cv2.VideoCapture(path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    vid_duration = math.floor(frame_count / fps)
    print("video duration:", vid_duration)
    print("total samples:", total_samples)
    sample_rate = vid_duration / total_samples * 1000
    print('sample rate:', sample_rate)

    height = math.floor(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out_image_arr = np.empty((height, total_samples, 3))

    success, image = video.read()
    for count in range(1, total_samples):
        frame = np.array(image)
        frame_averaged = np.mean(frame, axis=1)
        out_image_arr[:, count] = frame_averaged
        video.set(cv2.CAP_PROP_POS_MSEC, count * sample_rate)
        success, image = video.read()

    cv2.imwrite('static/img/' + filename, out_image_arr)

    return (total_samples, height)