import argparse
import cv2
from matplotlib import pylab as plt
import numpy as np
import pandas as pd
from pathlib import PurePath
from queue import Queue
import sys
from threading import Thread
import time
import tqdm


class FileVideoStream:
    def __init__(self, path, fps=1, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.fps = fps
        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return
            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                for _ in range(self.fps):
                    (grabbed, frame) = self.stream.read()
                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return
                # add the frame to the queue
                self.Q.put(frame)

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def plot_result(csv_path, fps, filestem):
    # save a result plot of the colors
    df = pd.read_csv(csv_path)
    t = np.linspace(0, len(df.r)/fps, len(df.r))
    plt.plot(t, df.r, 'r', label='red')
    plt.plot(t, df.g, 'g', label='green')
    plt.plot(t, df.b, 'b', label='blue')
    plt.xlabel('time [s]')
    plt.legend()
    plt.savefig(f'colors_plot_{filestem}.png')
    plt.close()


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str, required=True,
                    help="Path to input video file")
    ap.add_argument("-a", "--area", type=str, default="",
                    help="Area (x1, y1, x2, y2) of the ROI in the video")
    ap.add_argument("-s", "--speed", type=str, default="1",
                    help="Manual video frame search speed")
    args = vars(ap.parse_args())

    # initialize the bounding box coordinates
    if len(args.get('area')) < 7:
        initBB = None
    else:
        area = args.get('area').split(',')
        if len(area) != 4:
            print("area needs to be in form: x1,y1,x2,y2")
            sys.exit(-1)
        else:
            initBB = (int(area[0]), int(area[1]),
                      int(area[2]) - int(area[0]), int(area[3]) - int(area[1]))

    # check if we know the area, if not we need to show the video
    if isinstance(initBB, type(None)):
        setArea = False
    else:
        # if we know the area, we can process the video
        setArea = True

    fps = int(args.get('speed'))
    filestem = PurePath(args.get('video')).stem
    csv_path = f'colors_{filestem}.csv'

    # if a video path was not supplied, grab the reference to the web cam
    fvs = FileVideoStream(args["video"], fps).start()
    time.sleep(1.0)
    vfps = round(fvs.stream.get(cv2.CAP_PROP_FPS))
    num_frames = int(fvs.stream.get(cv2.CAP_PROP_FRAME_COUNT))

    if not setArea:
        # loop over frames from the video stream
        while not setArea:
            if fvs.more():
                frame = fvs.read()

            # check to the led area is known
            if initBB is not None:
                [x, y, w, h] = initBB
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 0), 2)

            # show the output frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # press 's' key, to "select" a bounding box
            if key == ord("s"):
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                                       showCrosshair=True)
                break

            # if the `q` key was pressed, break from the loop
            elif key == ord("q"):
                break

        print(f'Selected area: "{initBB[0]},{initBB[1]},\
                {initBB[0]+initBB[2]},{initBB[1]+initBB[3]}"')

        # close all windows
        cv2.destroyAllWindows()

    # know we knoe the area, so let's process the video for the trigger
    if not setArea:
        # stop video read thread
        fvs.stop()

    # (re)open the video stream from the beginning
    vs = cv2.VideoCapture(args["video"])
    time.sleep(1.0)

    s = time.time()
    with open(csv_path, "w") as out:
        out.write('b,g,r\n')

        for _ in tqdm.tqdm(range(num_frames)):
            ret, frame = vs.read()

            if ret:
                roi = frame[initBB[1]:(initBB[1]+initBB[3]),
                            initBB[0]:(initBB[0]+initBB[2]), :]
                avg_color = roi.mean(axis=0).mean(axis=0)
                out.write(f'{avg_color[0]},{avg_color[1]},{avg_color[2]}\n')

        e = time.time()

        print(f'started: {s}\nended  : {e}')

    # stop video read thread
    vs.release()

    plot_result(csv_path, vfps, filestem)
    print('Done\n')
