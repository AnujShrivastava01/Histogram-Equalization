# Image Contrast Enhancement: Mathematical Concepts

This document explains the core algorithms used in the PixelPerfect Contrast Enhancer.

## 1. Histogram Equalization (Grayscale)
The goal of Histogram Equalization (HE) is to map the probability distribution of pixel intensities to a uniform distribution, thereby spreading out the contrast.

### The Algorithm:
1. **Intensity Probability**: Let $n_k$ be the number of pixels with intensity $r_k$. The probability of an intensity level occurring is:
   $$P(r_k) = \frac{n_k}{MN}$$
   *(Where $M \times N$ is the total number of pixels)*

2. **Cumulative Distribution Function (CDF)**: We calculate the cumulative probability for each intensity $k$:
   $$s_k = T(r_k) = (L-1) \sum_{j=0}^{k} P(r_j)$$
   *(Where $L=256$ for standard 8-bit images)*

3. **Transformation**: Each original pixel $r_k$ is replaced by its corresponding $s_k$ value, rounded to the nearest integer.

## 2. Color Enhancement (YCrCb Strategy)
Applying standard HE independently to Red, Green, and Blue channels causes **Hue Shift** (e.g., a blue sky might turn purple because the ratios between R, G, and B are lost).

### Our Improved Strategy:
Instead of RGB, we use the **YCrCb** color space:
- **Y**: Luminance (Brightness)
- **Cr**: Red-difference Chroma (Color)
- **Cb**: Blue-difference Chroma (Color)

**The Process:**
1. Convert image from **RGB → YCrCb**.
2. Apply Histogram Equalization ONLY to the **Y channel**.
3. Keep **Cr** and **Cb** channels exactly as they were (preserving original colors).
4. Convert back from **YCrCb → RGB**.

## 3. Why This Project Stands Out
* **Human-Centric Processing**: By only touching the Luminance ($Y$), we mimic how human eyes perceive brightness without distorting actual color data.
* **Global vs Local**: This app uses Global HE, which looks at the entire image to determine the best transformation, ensuring a stable and consistent look across the frame.
