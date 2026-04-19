import cv2
import numpy as np

class ImageEngine:
    """
    Handles all image processing operations.
    Modular design allows for easy extension of algorithms.
    """
    
    @staticmethod
    def equalize_grayscale(image_np):
        """Applies Histogram Equalization to a grayscale image."""
        if len(image_np.shape) == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        return cv2.equalizeHist(image_np)

    @staticmethod
    def equalize_color(image_np):
        """
        Applies Histogram Equalization to a color image.
        Converts to YCrCb to equalize only the Luminance (Y) channel.
        This prevents hue shifts and color distortion.
        """
        # Convert BGR to YCrCb (OpenCV uses BGR by default, but we'll handle RGB from PIL)
        img_y_cr_cb = cv2.cvtColor(image_np, cv2.COLOR_RGB2YCrCb)
        
        # Split channels
        y, cr, cb = cv2.split(img_y_cr_cb)
        
        # Equalize the Y channel
        y_eq = cv2.equalizeHist(y)
        
        # Merge back
        img_eq_y_cr_cb = cv2.merge([y_eq, cr, cb])
        
        # Convert back to RGB
        return cv2.cvtColor(img_eq_y_cr_cb, cv2.COLOR_YCrCb2RGB)

    @staticmethod
    def get_histogram_data(image_np):
        """Calculates histogram data for visualization."""
        if len(image_np.shape) == 2:
            hist = cv2.calcHist([image_np], [0], None, [256], [0, 256])
            return {'Gray': hist}
        else:
            # Color channels
            channels = ('R', 'G', 'B')
            hists = {}
            for i, col in enumerate(channels):
                hists[col] = cv2.calcHist([image_np], [i], None, [256], [0, 256])
            return hists
