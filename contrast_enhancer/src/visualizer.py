import matplotlib.pyplot as plt
import io
from PIL import Image
import numpy as np

class Visualizer:
    """
    Handles generation of histogram plots as PIL images.
    """
    
    @staticmethod
    def create_histogram_plot(hists_dict, title="Histogram", size=(4, 3)):
        """
        Creates a matplotlib plot from histogram data and returns it as a PIL image.
        """
        plt.figure(figsize=size, dpi=100)
        plt.title(title)
        plt.xlabel("Intensity Value")
        plt.ylabel("Pixel Count")
        
        colors = {'R': 'red', 'G': 'green', 'B': 'blue', 'Gray': 'black'}
        
        for ch, hist in hists_dict.items():
            plt.plot(hist, color=colors.get(ch, 'black'), label=ch)
        
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save plot to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        
        return Image.open(buf)
