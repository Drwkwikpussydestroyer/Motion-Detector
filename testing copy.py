import cv2
import time

# Initialize video capture from the default webcam
video = cv2.VideoCapture(0)

# Allow the camera to warm up
time.sleep(2)

# Initialize the first frame for reference
first_frame = None

while True:
    # Read the current frame
    check, frame = video.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise and detail
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Set the first frame as reference
    if first_frame is None:
        first_frame = gray
        continue

    # Compute the absolute difference between the current frame and the reference frame
    delta_frame = cv2.absdiff(first_frame, gray)
    
    # Apply thresholding to highlight significant differences
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    
    # Dilate the thresholded image to fill in holes
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
    
    # Find contours on the thresholded image
    contours, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Ignore small contours to reduce false positives
        if cv2.contourArea(contour) < 300:
            continue
        
        # Get bounding box coordinates for the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # Draw a rectangle around the detected motion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # Display the resulting frames
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)
    
    key = cv2.waitKey(1)
    
    # Exit the loop when 'q' is pressed
    if key == ord('q'):
        break

# Release the video capture and close all windows
video.release()
cv2.destroyAllWindows()
