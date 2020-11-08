import argparse
import cv2
import numpy as np
import os
import pandas as pd
import soundfile as sf



def get_video_fps(file):
    """Open a video file and return the true sampling frequency.
    """
    cap = cv2.VideoCapture(file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def extract_audio_from(file, out_dir=''):
    """Call ffmpeg on the command line with the video file as input.
    The output will be a wav file with the same name as the input file.
    If a output path is given, the resulting wav file will be saved there.
    This function will return the filepath of the output file.
    """
    output_filename = f'{os.path.join(out_dir, file[:-4])}.wav'
    os.system(f'ffmpeg -i {file} {output_filename}')
    return output_filename


if __name__ == "__main__":
    """Take a video file as input, extract the audio and save it as wav file.
    Next, reload the audio data and save a table with trigger data [0~1].
    If separate output folders for the wav file and the trigger file are
    provided the respecting files will be saved there.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str, required=True,
                    help="Input video file")
    ap.add_argument("-ao", "--audioout", type=str, required=False, default='',
                    help="Output path for audio file")
    ap.add_argument("-o", "--out", type=str, required=False, default='',
                    help="Output path for audio trigger file")
    args = vars(ap.parse_args())

    video_fps = get_video_fps(args['video'])
    args["input"] = extract_audio_from(args['video'], args['audioout'])

    data, fs_audio = sf.read(args["input"])  # load trigger file
    if (data.shape[1] > 1):
        # extract trigger on- and offset from signal
        proc = np.abs(np.diff(np.abs(data[:, 1])))
        thres = proc.mean() + 10*proc.std()
        idx = np.argwhere(proc > thres).flatten()
        didx = np.diff(idx)
        z = np.argwhere(didx > 100).flatten()
        final_idx_pairs = np.concatenate(([idx[0]], idx[z+1]))

        # make new trigger vectors with 0 and 1
        trigger = np.zeros((len(data), ))
        for onset, offset in zip(final_idx_pairs[::2], final_idx_pairs[1::2]):
            trigger[onset:offset+1] = 1

        time = np.linspace(0, (len(data)-1)/fs_audio, len(data))
        df1 = pd.DataFrame(time, columns=['time'])
        df2 = pd.DataFrame(trigger.astype('int'), columns=['trigger'])
        df = df1.join(df2)
        print('Saving...(might take some time)')
        df.to_csv(os.path.join(args['out'], f'{args['video'][:-4]}.csv'), index=False)
        print('Done.')
    else:
        print('No trigger found in right channel. File is single channel!')
