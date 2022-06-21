import argparse
import threading
import cv2
from constants import FRAME_SIZE, ARGS
from picamera import PiCamera
import time
from videotx import VideoTx
import numpy as np
from multiprocessing import Queue, Process
from threading import Thread
import psutil


class VidSource:
    def __init__(self, file=None, size=FRAME_SIZE):
        self.file = file
        if self.file is not None:
            self.cap = cv2.VideoCapture(file)
            orig_size = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            ratio = min(size[1], orig_size[1]) / orig_size[1]
            self.size = tuple(round(d * ratio) for d in orig_size)
        else:
            self.size = size
            self.cam = PiCamera()
            self.cam.resolution = FRAME_SIZE
            self.cam.rotation = 180
            time.sleep(2)

    def nextFrame(self):
        if self.file is not None:
            ret, frame = self.cap.read()
            return ret, cv2.resize(frame, self.size)
        else:
            image = np.empty((FRAME_SIZE[0], FRAME_SIZE[1], 3), dtype=np.uint8)
            self.cam.capture(image, 'bgr', use_video_port=True)
            return True, image.reshape((FRAME_SIZE[1], FRAME_SIZE[0], 3))


class CameraHandler:
    def __init__(self):
        self.outq = Queue()
        self.inq = Queue()
        self.tx = VideoTx() if ARGS["debug"] else None
        self.source = VidSource(ARGS["file"])
        self.p = Process(target=CVWorker, args=(self.inq, self.outq))
        self.t = Thread(target=self.try_put_continuous)
        self.isRunning = False

    def start(self):
        self.isRunning = True
        if not self.p.is_alive():
            self.p.start()
        if not self.t.is_alive():
            self.t.start()

    def stop(self):
        self.isRunning = False

    def try_put_continuous(self):
        t = threading.currentThread()
        while True:
            while not self.isRunning:
                time.sleep(0.2)
            ret, frame = self.source.nextFrame()
            if ret:
                if self.inq.qsize() < 1:
                    self.inq.put(frame)
                else:
                    print("Not given")
            else:
                print("Could not get new frame from camera")
            time.sleep(0.5)

    def try_get(self):
        if not self.outq.empty():
            frame, res = self.outq.get_nowait()
            if ARGS["debug"]:
                self.tx.sendFrame(frame)
            return True, res
        else:
            print("No new frames in outq")
            return False, None


def CVWorker(inq: Queue, outq):
    tm = cv2.TickMeter()
    fdet = cv2.FaceDetectorYN.create("resources/yunet.onnx", "", FRAME_SIZE, 0.9, 0.3, 5000)
    print(hex(id(fdet)))
    pdet = cv2.HOGDescriptor()
    pdet.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    while True:
        frame = inq.get()
        #print("Working on ", psutil.Process().cpu_num())
        tm.start()
        res = compute(frame, fdet, pdet)
        tm.stop()
        drawFrame(frame, tm, *res)
        outq.put((frame, res[0]))


def compute(frame, fdet, pdet):
    faces = fdet.detect(frame)[1]
    if faces is not None:
        faces = faces[:, 0:4].astype(np.uint32)
        return biggestBox(faces), faces, None
    else:
        people = None
        return biggestBox(people), None, people


def biggestBox(boxes):
    if boxes is not None:
        idx = np.argmax(np.array([[w * h] for (x, y, w, h) in boxes]))
        return boxes[idx]
    else:
        return None


def drawRect(frame, rect, thick, color):
    cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), color, thick)


def drawFrame(frame, tm, target, faces, people):
    thick = 2
    if target is not None:
        drawRect(frame, target, thick, (0, 0, 255))
    if faces is not None:
        for face in faces:
            drawRect(frame, face, thick, (0, 255, 0))
    if people is not None:
        for person in people:
            drawRect(frame, person, thick, (255, 0, 0))
    cv2.putText(frame, 'Fdet: {:.2f}'.format(tm.getAvgTimeSec()), (1, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def main():
    # start CV scheduler
    cvs = CameraHandler()
    cvs.start()

    while True:
        start = time.time()
        if cvs.try_get() is not None:
            print("Time = ", time.time()-start)
        time.sleep(0.2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", type=str, help="test video path")
    ap.add_argument("-d", "--debug", action=argparse.BooleanOptionalAction)
    args = vars(ap.parse_args())
    main()
