import cv2
import numpy as np
import threading
import time
import logging

# Configure logging
logger = logging.getLogger("camera")

class CameraDriver:
    def __init__(self, camera_indices=[0, 1, 2]):
        self.mock = False
        self.cameras = {}
        
        # Try to initialize cameras
        try:
            for idx in camera_indices:
                cap = cv2.VideoCapture(idx)
                if cap.isOpened():
                    self.cameras[idx] = cap
                    logger.info(f"Camera {idx} initialized successfully.")
                else:
                    logger.warning(f"Camera {idx} failed to open.")
        except Exception as e:
            logger.error(f"Error initializing cameras: {e}")
            self.mock = True

        if not self.cameras:
            logger.warning("No cameras found. Using mock camera feeds.")
            self.mock = True

    def get_frame(self, index):
        if self.mock or index not in self.cameras:
            return self.generate_mock_frame(index)
        
        try:
            ret, frame = self.cameras[index].read()
            if not ret:
                logger.warning(f"Failed to capture frame from camera {index}")
                return self.generate_mock_frame(index)
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                return self.generate_mock_frame(index)
            
            return buffer.tobytes()
        except Exception as e:
            logger.error(f"Error capturing frame {index}: {e}")
            return self.generate_mock_frame(index)

    def generate_mock_frame(self, index):
        # Create a dummy image using numpy
        width, height = 640, 480
        img = np.zeros((height, width, 3), np.uint8)
        
        # Dynamic content based on time
        t = time.time()
        
        # Color cycle background
        r = int((np.sin(t) + 1) * 127)
        g = int((np.cos(t) + 1) * 127)
        b = int((np.sin(t + 2) + 1) * 127)
        img[:] = (b//4, g//4, r//4)
        
        # Draw text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"MOCK CAM {index}", (50, 50), font, 1, (255, 255, 255), 2)
        cv2.putText(img, time.strftime("%H:%M:%S"), (50, 100), font, 1, (255, 255, 255), 2)
        
        # Encode
        ret, buffer = cv2.imencode('.jpg', img)
        return buffer.tobytes()

    def release(self):
        for cap in self.cameras.values():
            cap.release()
