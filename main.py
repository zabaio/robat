import imutils
import datetime
import numpy as np
import cv2

# initialize the camera and grab a reference to the raw camera capture
cap = cv2.VideoCapture("test1.mp4")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        frame = imutils.resize(frame, width=min(500, frame.shape[1]))

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

    # Break the loop
    else:
        break

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()