import datetime
import numpy as np
import cv2

cap = cv2.VideoCapture("test1.mp4")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    start = datetime.datetime.now()
    boxes, weights = hog.detectMultiScale(frame, winStride=(16, 16), useMeanshiftGrouping=False)
    bB = len(boxes)
    aB = len(boxes)
    print(bB, aB)
    print("[INFO] detection took: {}s".format(
        (datetime.datetime.now() - start).total_seconds()))

    if len(boxes) != 0:
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
       break


# initialize the camera and grab a reference to the raw camera capture
cap = cv.VideoCapture("test1.mp4")

detector = cv.FaceDetectorYN.create(
    "yunet.onnx",
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)
scale = 0.5

tm = cv.TickMeter()


def visualize(input, faces, fps, thickness=2):
    if faces[1] is not None:
        for idx, face in enumerate(faces[1]):
            print('Face {}, top-left coordinates: ({:.0f}, {:.0f}), box width: {:.0f}, box height {:.0f}, score: {:.2f}'.format(idx, face[0], face[1], face[2], face[3], face[-1]))
            coords = face[:-1].astype(np.int32)
            cv.rectangle(input, (coords[0], coords[1]), (coords[0]+coords[2], coords[1]+coords[3]), (0, 255, 0), thickness)
            cv.circle(input, (coords[4], coords[5]), 2, (255, 0, 0), thickness)
            cv.circle(input, (coords[6], coords[7]), 2, (0, 0, 255), thickness)
            cv.circle(input, (coords[8], coords[9]), 2, (0, 255, 0), thickness)
            cv.circle(input, (coords[10], coords[11]), 2, (255, 0, 255), thickness)
            cv.circle(input, (coords[12], coords[13]), 2, (0, 255, 255), thickness)
    cv.putText(input, 'FPS: {:.2f}'.format(fps), (1, 16), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        img1Width = int(frame.shape[1] * scale)
        img1Height = int(frame.shape[0] * scale)
        frame = cv.resize(frame, (img1Width, img1Height))
        tm.start()

        detector.setInputSize((img1Width, img1Height))
        faces = detector.detect(frame)

        tm.stop()

        #assert faces[1] is not None, 'Cannot find a face'
        # Draw results on the input image
        visualize(frame, faces, tm.getFPS())
        # Save results if save is true

        # Visualize results in a new window
        cv.imshow("image1", frame)

    # Break the loop
    else:
        break

    # Press Q on keyboard to  exit
    if cv.waitKey(25) & 0xFF == ord('q'):
        break