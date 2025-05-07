from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
import smtplib
import threading
import winsound
import cv2
import imutils
import time

class HomeGlow(MDApp):
    def build(self):
        label = MDLabel(text="Hello, HomeGlow! lorem ipsum oshdog;i soiugoes;dguisdogushidgiygiapyogiakjsdgoiasygpsdaiyghaskghsagisgl;ksh", halign="center", theme_text_color="Custom", text_color=(0, 1, 0, 1), font_style="H1")
        return  label
HomeGlow().run()


def totoy():
    import time
    x = int(input("how many minutes?"))                #10 + 1
    y = x * 60 + 1
    
    for i in range(y):
        y -= 1 
        time.sleep(1)
        print(y)

def tite():
    import time
    x_time = 5 + 1

    for i in range(x_time):
        x_time -= 1
        time.sleep(1)
    print("turning off")



# === Timer Control ===
no_motion_timeout = 5  # seconds
last_motion_time = time.time()

# === Flags ===
alarm = False
alarm_mode = False
alarm_counter = 0
off_timer_triggered = False

# === Motion Timeout Function ===
def offtimer():
    global off_timer_triggered
    print("No motion detected. Countdown started...")
    time.sleep(no_motion_timeout)
    # Only trigger if still no movement since countdown began
    if time.time() - last_motion_time >= no_motion_timeout:
        print("⏲️ No motion detected for 5 seconds. Turning off...")
        off_timer_triggered = True

# === Alarm Sound ===
def beepBoop():
    global alarm
    for _ in range(5):
        if not alarm:
            break
        print("🔔 Movement detected!")
        winsound.Beep(2500, 1000)
    alarm = False


#def send_email_notification(to_email, subject, message):
 #   from_email = "ikoygwapo31@gmail.com"
  #  password = ""

   # msg = f"Subject: {subject}\n\n{message}"
    #server = smtplib.SMTP('smtp.gmail.com', 587)
#    server.starttls()
 #   server.login(from_email, password)
  #  server.sendmail(from_email, to_email, msg)
   # server.quit()

#send_email_notification("user@example.com", "Alert", "You were notified!")


# === Camera Setup ===
capture = cv2.VideoCapture()
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# === Get First Frame ===
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
        difference = cv2.absdiff(start_frame, gray_blurred)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)

        if threshold.sum() > 4:  # motion detected
            alarm_counter += 1
            last_motion_time = time.time()
            off_timer_triggered = False  # reset
        else:
            alarm_counter = max(0, alarm_counter - 1)

        cv2.imshow("Cam", threshold)

        # Trigger alarm
        if alarm_counter > 20:
            if not alarm:
                alarm = True
                threading.Thread(target=beepBoop).start()

        # Start offtimer if enough time passed since last movement and not already triggered
        if time.time() - last_motion_time >= no_motion_timeout and not off_timer_triggered:
            threading.Thread(target=offtimer).start()
            off_timer_triggered = True
                
    else:
        cv2.imshow("Cam", frame)

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
        print("Alarm mode toggled:", "ON" if alarm_mode else "OFF")
    if key_pressed == ord("q"):
        break

    if alarm_mode:
        start_frame = gray_blurred

capture.release()
cv2.destroyAllWindows()























