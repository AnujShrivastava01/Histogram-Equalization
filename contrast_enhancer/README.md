# PixelPerfect | Image Contrast Enhancer

A production-quality tool for enhancing image contrast using **Global Histogram Equalization**. This project demonstrates clean architecture, robust image processing using OpenCV, and a modern GUI built with Tkinter and Matplotlib.

## 🚀 Key Features
- **Dual Processing Modes**:
    - **Grayscale**: Classic HE for monochromatic images.
    - **Color (YCrCb)**: Advanced HE that equalizes the Luminance (Y) channel to prevent color distortion and hue shifts.
- **Side-by-Side Comparison**: Real-time visualization of processing results.
- **Histogram Analysis**: Dynamic Matplotlib plots showing intensity distribution before and after enhancement.
- **Modern UI**: Clean, sidebar-based layout with responsive design and status feedback.

## 🛠️ Architecture
The project follows a modular design for high maintainability:
- `engine.py`: Encapsulates all OpenCV-based mathematical operations.
- `gui.py`: Manages the view layer, event loops, and user interactions.
- `visualizer.py`: Bridges the gap between raw data and visual plots.

## 📂 Installation & Usage
1. **Requirements**: Python 3.8+
2. **Setup**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run**:
   ```bash
   python main.py
   ```

## 🧠 Why YCrCb for Color?
Standard Histogram Equalization applied to RGB channels independently often results in severe color artifacts. By converting to the **YCrCb** color space, we isolate the brightness (Y) from the color information (Cr/Cb). Equalizing only the Y channel enhances contrast while keeping the colors natural and preserved.
