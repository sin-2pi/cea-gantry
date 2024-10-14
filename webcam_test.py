import cv2
import os
from datetime import datetime


def capture_photos():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a directory to store the photos
    output_dir = "webcam_photos"
    os.makedirs(output_dir, exist_ok=True)

    photo_count = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Display the resulting frame
        cv2.imshow("Webcam", frame)

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF

        # If 's' is pressed, save the photo
        if key == ord("s"):
            photo_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/photo_{timestamp}_{photo_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Photo saved: {filename}")

        # If 'q' is pressed, quit the program
        elif key == ord("q"):
            print("Quitting...")
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_photos()
