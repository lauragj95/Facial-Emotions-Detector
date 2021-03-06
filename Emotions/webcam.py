"""
Maybe add all frames from the webcam in a buffer (queue) and
read them all one by one.
"""
import pickle

import cv2
import numpy as np

from frames import FrameHandler



def get_webcam_video(width, height):
    vc = cv2.VideoCapture(0)
    vc.set(3, width)
    vc.set(4, height)
    print(vc.isOpened())

    while True:
        ret, frame = vc.read()

        if not ret:
            return

        yield frame


emotions = ["happy","neutral","sadness"]
#emotions = ['anger', 'contempt', 'disgust', 'fear',
               # 'happy', 'neutral', 'sadness', 'surprise']

with open('models/trained_svm_model', 'rb') as f:
        model = pickle.load(f)
        
print('kek')

for frame in get_webcam_video(350, 350):
    handler = FrameHandler(frame)
    handler.draw_landmarks()
    faces = np.array([handler.get_vectorized_landmarks()])
    if faces[0] is not None:
        prediction = model.predict(faces)
        print(model.predict_proba(faces))
        if len(prediction) > 0:
            text = emotions[prediction[0]]
            cv2.putText(handler.frame, text, (40, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        thickness=2)

    cv2.imshow('image', handler.frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
    cv2

cv2.destroyAllWindows()
