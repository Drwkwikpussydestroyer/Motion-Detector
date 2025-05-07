from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
import threading
import time
import winsound
import cv2
import imutils

# === Global Flags ===
alarm_mode = False
alarm = False
alarm_counter = 0
off_timer_triggered = False
no_motion_timeout = 5
last_motion_time = time.time()

def find_camera_index():
    """Find the index of the first available external camera, then fallback to internal."""
    for index in range(1, 10):
        capture = cv2.VideoCapture(index)
        if capture.isOpened():
            capture.release()
            print(f"External camera found at index {index}")
            return index
    capture = cv2.VideoCapture(0)
    if capture.isOpened():
        capture.release()
        print("Internal camera found at index 0")
        return 0
    raise RuntimeError("No camera found!")

def offtimer():
    global off_timer_triggered
    print("No motion detected. Countdown started...")
    time.sleep(no_motion_timeout)
    if time.time() - last_motion_time >= no_motion_timeout:
        print("⏲️ No motion detected for 5 seconds. Turning off...")
        off_timer_triggered = True

def beepBoop():
    global alarm
    for _ in range(5):
        if not alarm:
            break
        print("🔔 Movement detected!")
        winsound.Beep(2500, 1000)
    alarm = False

def start_camera_loop():
    global alarm_mode, alarm_counter, alarm, off_timer_triggered, last_motion_time

    camera_index = find_camera_index()
    capture = cv2.VideoCapture(camera_index)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    _, start_frame = capture.read()
    start_frame = imutils.resize(start_frame, width=500)
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Failed to read from camera. Exiting...")
            break

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blurred = cv2.GaussianBlur(gray, (21, 21), 0)

        if alarm_mode:
            difference = cv2.absdiff(start_frame, gray_blurred)
            threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
            threshold = cv2.dilate(threshold, None, iterations=2)

            if threshold.sum() > 4:
                print("Motion detected")
                alarm_counter += 1
                last_motion_time = time.time()
                off_timer_triggered = False
            else:
                alarm_counter = max(0, alarm_counter - 1)

            cv2.imshow("Cam", threshold)

            if alarm_counter > 20:
                if not alarm:
                    alarm = True
                    threading.Thread(target=beepBoop).start()

            if time.time() - last_motion_time >= no_motion_timeout and not off_timer_triggered:
                threading.Thread(target=offtimer).start()
                off_timer_triggered = True
        else:
            cv2.imshow("Cam", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        if alarm_mode:
            start_frame = gray_blurred

    capture.release()
    cv2.destroyAllWindows()

class HomeGlow(MDApp):
    def build(self):
        screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = MDLabel(
            text="BUTTON TESTING",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 2, 0, 1),
            font_style="H4"
        )

        button = MDRectangleFlatButton(
            text="Toggle Alarm",
            pos_hint={"center_x": 0.5},
            on_release=self.toggle_alarm
        )

        layout.add_widget(self.label)
        layout.add_widget(button)
        screen.add_widget(layout)

        threading.Thread(target=start_camera_loop, daemon=True).start()
        return screen

    def toggle_alarm(self, instance):
        global alarm_mode

        if not alarm_mode:
            self.label.text = "Activating alarm in 10 seconds..."
            print("Activating alarm in 10 seconds...")

            def delayed_activation():
                time.sleep(10)
                global alarm_mode
                alarm_mode = True
                print("Alarm mode toggled: ON")
                self.label.text = "Alarm mode is ON"

            threading.Thread(target=delayed_activation).start()
        else:
            alarm_mode = False
            self.label.text = "Alarm mode is OFF"
            print("Alarm mode toggled: OFF")

HomeGlow().run()
