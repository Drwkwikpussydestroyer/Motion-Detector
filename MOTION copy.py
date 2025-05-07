import threading
import winsound
import cv2
import imutils
 
 
#Video Capture swtich it to 1 when you want to use an extermal camera
capture = cv2.VideoCapture(0)
 
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
 
 
alarm = False
alarm_mode = False
alarm_counter = 0
 
def beepBoop():
    global alarm
    for _ in range(5):
        if not alarm:
            break
        print("WEDOWEODWEDOWEDO")
        winsound.Beep(2500,1000)
    alarm = False
 
 
_, start_frame= capture.read()
 
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2RGB)
start_frame = cv2.GaussianBlur(start_frame, (21,23), 0)
 
 
while True:
    ret,frame = capture.read()
    frame = imutils.resize(frame, width=500)
    if alarm_mode:
        frame_alarm = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_alarm = cv2.GaussianBlur(frame_alarm, (5,5), 0)
        difference = cv2.absdiff(frame, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_alarm
       
        if threshold.sum() > 300:
            alarm_counter +=1
        else:
            if alarm_counter > 0:
                alarm_counter -=1
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
        if alarm_counter> 20:
            if not alarm:
                alarm = True
                threading.Thread(target=beepBoop).start()
             
    key_pressed =  cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode =  False
        break
 
capture.release()
cv2.destroyAllWindows()