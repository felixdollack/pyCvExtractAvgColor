import argparse
import cv2
import numpy as np
import matplotlib as mpl
from matplotlib import pylab as plt
import pandas as pd


def get_video_fps(file):
    """Open a video file and return the true sampling frequency.
    """
    cap = cv2.VideoCapture(file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def add_interval(ax, xdata, ydata, caps="  "):
    line = ax.add_line(mpl.lines.Line2D(xdata, ydata))
    anno_args = {
        'ha': 'center',
        'va': 'center',
        'size': 24,
        'color': line.get_color()
    }
    a0 = ax.annotate(caps[0], xy=(xdata[0], ydata[0]), **anno_args)
    a1 = ax.annotate(caps[1], xy=(xdata[1], ydata[1]), **anno_args)
    return (line,(a0,a1))


if __name__ == "__main__":
    """Take a video file as input, extract the audio and save it as wav file.
    Next, reload the audio data and save a table with trigger data [0~1].
    If separate output folders for the wav file and the trigger file are
    provided the respecting files will be saved there.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str, required=True,
                    help="Input video file")
    ap.add_argument("-at", "--audiotrigger", type=str, required=True,
                    help="Audio trigger file")
    ap.add_argument("-vt", "--videotrigger", type=str, required=True,
                    help="Video trigger file")
    args = vars(ap.parse_args())

    df_audio = pd.read_csv(args['audiotrigger'])
    df_video = pd.read_csv(args['videotrigger'])
    video_fps = get_video_fps(args['video'])
    fs_audio = int(round(1/(df_audio.time[2]-df_audio.time[1])))

    fig, ax = plt.subplots(1, 1, figsize=[8,4])
    ax.plot(df_audio.time, df_audio.trigger * 200, label='Audio')
    ax.plot((1/video_fps)*df_video.index, df_video.r, label='Video')
    ax.set_title('Extracted Trigger')
    ax.set_xlim([68, 69.5])
    ax.set_ylim([-1, 215])
    plt.legend()
    plt.savefig('trigger_comparison_audio_video.png')
    plt.close()

    pos_trigger = np.argwhere(df_audio.trigger.values>0).flatten()
    start_idx = np.argwhere(np.diff(pos_trigger) > 1).flatten()
    dt1 = (pos_trigger[start_idx[0]+1] - pos_trigger[start_idx[0]])/fs_audio
    dt2 = (pos_trigger[start_idx[1]+1] - pos_trigger[start_idx[1]])/fs_audio

    fig, ax = plt.subplots(1, 1, figsize=[8,4])
    ax.plot(df_audio.time, df_audio.trigger * 200, label='Audio')
    ax.plot((1/video_fps)*df_video.index, df_video.r, label='Video')
    add_interval(ax, (df_audio.time[pos_trigger[start_idx[0]]],
                      df_audio.time[pos_trigger[start_idx[0]+1]]), (100, 100), "()")
    add_interval(ax, (df_audio.time[pos_trigger[start_idx[1]]],
                      df_audio.time[pos_trigger[start_idx[1]+1]]), (100, 100), "()")
    ax.set_title('Duration between initial 3 trigger signals')
    ax.set_xlim([68.44, 68.66])
    ax.set_ylim([-1, 215])
    ax.text(68.505, 110, f'{dt1:.3f}s')
    ax.text(68.59, 110, f'{dt2:.3f}s')
    plt.legend()
    plt.savefig('trigger_triplet_initial_distance_audio.png')
    plt.close()
