import argparse
import cv2
from constants import FRAME_SIZE
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from videotx import VideoTx
import numpy as np
from multiprocessing import Queue


def CVProcess(q: Queue):
    cvs = CVServer(VidSource())
    tx = VideoTx()
    while True:
        res = cvs.compute()
        q.put(res[0])
        if VideoTx is not None:
            cvs.drawFrame(*res)
            tx.sendFrame(cvs.frame)


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
            self.cam.framerate = 32
            self.cam.rotation = 180
            self.rawCapture = PiRGBArray(self.cam, size=FRAME_SIZE)
            time.sleep(2)

    def nextFrame(self):
        if self.file is not None:
            ret, frame = self.cap.read()
            return ret, cv2.resize(frame, self.size)
        else:
            image = np.empty((FRAME_SIZE[0] * FRAME_SIZE[1] * 3,), dtype=np.uint8)
            self.cam.capture(image, 'bgr')
            return True, image.reshape((FRAME_SIZE[1], FRAME_SIZE[0], 3))


class CVServer:
    def __init__(self, source):
        self.source = source
        self.frame = None
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.detector = cv2.FaceDetectorYN.create("yunet.onnx", "", source.size, 0.9, 0.3, 5000)
        self.tmp = cv2.TickMeter()
        self.tmf = cv2.TickMeter()

    def compute(self):
        people = None
        ret, self.frame = self.source.nextFrame()
        if ret:
            self.tmf.start()
            faces = self.detector.detect(self.frame)[1]
            self.tmf.stop()
            if faces is not None:
                faces = faces[:, 0:4].astype(np.uint32)
            else:
                self.tmp.start()
                people = self.hog.detectMultiScale(self.frame, winStride=(8, 8), scale=1.10)[0]
                self.tmp.stop()
                if not isinstance(people, np.ndarray):
                    people = None
            return CVServer.chooseTarget(faces, people), faces, people
        else:
            print("Could not get new frame")
            return None, None, None

    @staticmethod
    def chooseTarget(faces, people):
        return CVServer.biggestBox(faces) if faces is not None \
            else CVServer.biggestBox(people) if people is not None \
            else None

    @staticmethod
    def biggestBox(boxes):
        idx = np.argmax(np.array([[w * h] for (x, y, w, h) in boxes]))
        return boxes[idx]

    @staticmethod
    def drawRect(frame, rect, thick, color):
        cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), color, thick)

    def drawFrame(self, target, faces, people, thick=2):
        if target is not None:
            CVServer.drawRect(self.frame, target, thick, (0, 0, 255))
        if faces is not None:
            for face in faces:
                CVServer.drawRect(self.frame, face, thick, (0, 255, 0))
        if people is not None:
            for person in people:
                CVServer.drawRect(self.frame, person, thick, (255, 0, 0))
        cv2.putText(self.frame,
                    'Pdet: {:.2f} - Fdet: {:.2f}'.format(self.tmp.getAvgTimeSec(), self.tmf.getAvgTimeSec()),
                    (1, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def main(args):
    # init video source
    source = VidSource(args["file"])
    # start CV server
    cvs = CVServer(source)
    tx = VideoTx()

    while True:
        # Draw results on the input image
        cvs.drawFrame(*cvs.compute())
        tx.sendFrame(cvs.frame)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", type=str, help="test video path")
    main(vars(ap.parse_args()))
