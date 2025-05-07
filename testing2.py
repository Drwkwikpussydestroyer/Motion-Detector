import threading
import winsound
import cv2
import imutils
 

def offtimer():
    import time
    x_time = 5 + 1

    for i in range(x_time):
        x_time -= 1
        time.sleep(1)
    print("turning off")

# Video Capture: use 0 for internal, 1 for external camera
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
        print("movement detected")
        winsound.Beep(2500, 1000)
    alarm = False
 
# Get the initial frame and preprocess it
_, start_frame = capture.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
 
while True:
    ret, frame = capture.read()
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (21, 21), 0)
 
    if alarm_mode:
        # Compute difference between current frame and reference frame
        difference = cv2.absdiff(start_frame, gray_blurred)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)
 
        if threshold.sum() > 4:  # Adjust sensitivity if needed
            alarm_counter += 1
        else:
            alarm_counter = max(0, alarm_counter - 1)
 
        cv2.imshow("Cam", threshold)
 
        # Alarm trigger
        if alarm_counter > 20:
            if not alarm:
                alarm = True
                threading.Thread(target=beepBoop).start()


    else:
        cv2.imshow("Cam", frame)
 
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
        print("Alarm mode toggled:", "ON" if alarm_mode else "OFF")
    if key_pressed == ord("q"):
        break
 
    # Update start_frame only in alarm mode
    if alarm_mode:
        start_frame = gray_blurred
 
capture.release()
cv2.destroyAllWindows()


