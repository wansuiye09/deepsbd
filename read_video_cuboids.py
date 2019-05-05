from clockshortenstream.process_video_pkg.frame_reader import FrameReader
from skimage.transform import resize
from config import frame_size,grad_n_frames_per_sample
import numpy as np
import cv2
from SIM_generator_class import SIMGenerator


simgen = SIMGenerator(grad_n_frames_per_sample)

def read_cuboid_from_video_cut_detection(video_path, frame_nums_list):
    fReader = FrameReader(pathToVideo=video_path)

    frames = []

    for frame_num in frame_nums_list:
        frame = fReader.getFrameAtFrameNumber(frame_num)
        frame_resized = resize(frame, frame_size)
        frames.append(frame_resized)

    fReader.closeFrameReader()

    cuboid = np.array(frames)
    cuboid = np.expand_dims(cuboid,axis=0)

    return cuboid



def get_frame_start_for_grad_cuboids(frame_candidate):
    frame_start = frame_candidate-grad_n_frames_per_sample/2

    return frame_start



def read_frame_cuboid_from_video_grad(video_path, frame_candidate):

    fReader = FrameReader(pathToVideo=video_path)
    frame_start = get_frame_start_for_grad_cuboids(frame_candidate)
    frames = fReader.getNumberOfFramesFromPosition(start_frame_id=frame_start,
                                                   num_frames=grad_n_frames_per_sample)
    for idx, frame in enumerate(frames):
        frames[idx] = cv2.resize(frame, frame_size)

    fReader.closeFrameReader()

    return frames


def get_SIM_for_grad_candidate(video_path,frame_candidate):

    grad_cuboid = read_frame_cuboid_from_video_grad(video_path,frame_candidate)
    sim = simgen.createFullSIM(grad_cuboid)
    sim = np.expand_dims(sim,axis=0)

    return sim