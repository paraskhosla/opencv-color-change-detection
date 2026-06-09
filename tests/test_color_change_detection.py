import unittest
import cv2
import numpy as np
from Color_change_detection_using_ROI_with_predefined_color import detect_color_change  # Replace with the actual module name

class TestColorChangeDetection(unittest.TestCase):

    def setUp(self):
        # Create synthetic images for testing
        self.burgundy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.burgundy_image[:] = [60, 20, 220]  # BGR for a burgundy-like color

        self.non_burgundy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.non_burgundy_image[:] = [255, 0, 0]  # BGR for blue

    def test_detect_burgundy_in_burgundy_frame(self):
        # Test burgundy detection in a frame with burgundy color
        roi = self.burgundy_image.copy()
        color_change_detected, _ = detect_color_change(self.burgundy_image, roi)
        self.assertFalse(color_change_detected, "Incorrectly detected color change in a frame with burgundy color")

    def test_no_burgundy_in_non_burgundy_frame(self):
        # Test burgundy detection in a frame without burgundy color
        roi = self.non_burgundy_image.copy()
        color_change_detected, _ = detect_color_change(self.non_burgundy_image, roi)
        self.assertTrue(color_change_detected, "Failed to detect color change in a frame without burgundy color")

if __name__ == '__main__':
    unittest.main()
