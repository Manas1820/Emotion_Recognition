import cv2
import numpy as np
from keras.models import load_model
model=load_model('model_5-49-0.62.hdf5')
mask=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotion=['angry','disgust','fear','happy','sad','surprise','neutral']
videoCap=cv2.VideoCapture(0)
while True:
    res,frame=videoCap.read()
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face=mask.detectMultiScale(gray,scaleFactor=1.1)
    for (x, y, w, h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        box=frame[y:y+h,x:x+w]
        box=cv2.resize(box,(48,48))
        box=cv2.cvtColor(box,cv2.COLOR_BGR2GRAY)
        box=box.astype('float32')/255
        box=np.asarray(box)
        box=box.reshape(1, 1,box.shape[0],box.shape[1])
        cv2.putText(frame,emotion[np.argmax(model.predict(box))]
                    ,(x,y),cv2.FONT_HERSHEY_COMPLEX,1
                    ,(0,255,0),1,cv2.LINE_AA)
    cv2.imshow('Video',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
videoCap.release()
cv2.destroyAllWindows()