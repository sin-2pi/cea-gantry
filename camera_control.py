import cv2
import time

class CameraControl:
    @staticmethod
    def take_snapshot():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        
        frame_count = 0
        target_frame_count = 100

        while frame_count < target_frame_count:
            ret, frame = cap.read()
            frame_count += 1

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_name = f"captured_image_{timestamp}.jpg"
        cv2.imwrite(file_name, frame)

        cap.release()
        cv2.destroyAllWindows()