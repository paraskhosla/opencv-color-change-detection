import unittest
import cv2
import numpy as np
from Yellow_color_detection_using_OpenCV import detect_yellow_color  # The module name

class TestColorDetection(unittest.TestCase):

    def setUp(self):
        # Create synthetic images for testing
        self.yellow_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.yellow_image[:] = [0, 255, 255]  # BGR for yellow

        self.non_yellow_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.non_yellow_image[:] = [255, 0, 0]  # BGR for blue

        self.mixed_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.circle(self.mixed_image, (50, 50), 30, (0, 255, 255), -1)  # Draw a yellow circle

    def test_detect_yellow_in_yellow_image(self):
        # Test yellow detection in an all-yellow image
        result = detect_yellow_color(self.yellow_image.copy())
        hsv_result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_result, np.array([20, 100, 100]), np.array([30, 255, 255]))
        self.assertTrue(np.sum(mask) > 0, "Failed to detect yellow in an all-yellow image")

    def test_no_yellow_in_non_yellow_image(self):
        # Test yellow detection in a non-yellow image
        result = detect_yellow_color(self.non_yellow_image.copy())
        hsv_result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_result, np.array([20, 100, 100]), np.array([30, 255, 255]))
        self.assertTrue(np.sum(mask) == 0, "Incorrectly detected yellow in a non-yellow image")

    def test_detect_yellow_in_mixed_image(self):
        # Test yellow detection in a mixed image
        result = detect_yellow_color(self.mixed_image.copy())
        hsv_result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_result, np.array([20, 100, 100]), np.array([30, 255, 255]))
        self.assertTrue(np.sum(mask) > 0, "Failed to detect yellow in a mixed image")

    def test_camera_opening(self):
        # Test if the camera opens correctly
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        self.assertTrue(ret, "Failed to open camera and read a frame")

if __name__ == '__main__':
    unittest.main()
