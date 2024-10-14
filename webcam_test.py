import cv2
import os
from datetime import datetime


def get_highest_resolution(cap):
    resolutions = [
        (1920, 1080),  # Full HD
        (1280, 720),  # HD
        (1024, 768),  # XGA
        (800, 600),  # SVGA
    ]

    for width, height in resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if actual_width >= width and actual_height >= height:
            return actual_width, actual_height

    return actual_width, actual_height  # Return the last supported resolution


def capture_photos():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Get the highest supported resolution
    width, height = get_highest_resolution(cap)
    print(f"Camera set to resolution: {width}x{height}")

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
            filename = (
                f"{output_dir}/photo_{width}x{height}_{timestamp}_{photo_count}.jpg"
            )
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
