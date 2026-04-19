import streamlit as st
from PIL import Image
import numpy as np
import os
from src.engine import ImageEngine
from src.visualizer import Visualizer

# --- Page Config ---
st.set_page_config(
    page_title="PixelPerfect | Image Enhancement Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f5;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1a73e8;
        color: white;
        font-weight: bold;
    }
    .stRadio > div {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #202124;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("CONTROLS")
    st.write("---")
    
    st.subheader("Enhancement Mode")
    mode = st.radio(
        "Choose Mode:",
        ("Color Enhancement", "Grayscale / BW"),
        help="Color mode preserves natural hues while Grayscale converts to B&W."
    )
    
    st.write("---")
    uploaded_file = st.file_uploader("📁 Upload Image", type=["jpg", "jpeg", "png", "webp"])
    
    st.write("---")
    if st.button("🔄 Reset Application"):
        st.rerun()

    st.sidebar.markdown("""
    <div style='position: fixed; bottom: 20px;'>
        <p style='color: #9aa0a6; font-size: 0.8em;'>
        Supports: JPG, PNG, WEBP<br>
        Uses: Global Histogram Equalization
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Content ---
st.title("✨ PixelPerfect | Contrast Enhancement Studio")
st.markdown("### Side-by-Side Comparison")

if uploaded_file is not None:
    try:
        # Load and display original
        original_image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(original_image)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original")
            st.image(original_image, use_container_width=True)
            
            # Original Histogram
            hist_data = ImageEngine.get_histogram_data(img_np)
            hist_plot = Visualizer.create_histogram_plot(hist_data, "Original Histogram")
            st.image(hist_plot, use_container_width=True)

        with col2:
            st.subheader("Enhanced Result")
            
            # Process image
            with st.spinner("Processing..."):
                if mode == "Grayscale / BW":
                    processed_np = ImageEngine.equalize_grayscale(img_np)
                    # Convert single channel back to RGB for streamlit display if needed, 
                    # but st.image handles grayscale
                else:
                    processed_np = ImageEngine.equalize_color(img_np)
                
                processed_image = Image.fromarray(processed_np)
                st.image(processed_image, use_container_width=True)
                
                # Enhanced Histogram
                proc_hist_data = ImageEngine.get_histogram_data(processed_np)
                proc_hist_plot = Visualizer.create_histogram_plot(proc_hist_data, "Enhanced Histogram")
                st.image(proc_hist_plot, use_container_width=True)

        # --- Concept Guide ---
        st.write("---")
        with st.expander("📘 How it Works | Simple Guide"):
            st.markdown("""
            ### 📈 1. Improving Contrast
            **The 'Elastic Band' Analogy**
            Think of an image's brightness like a bunched-up elastic band. When an image is dull, all the pixels are stuck in the middle. Our tool takes both ends of that band and stretches them out! By spreading the darks and lights evenly, the hidden details suddenly become visible.

            ### 🌈 2. Fixing Color Images
            **The 'Coloring Book' Analogy**
            Imagine a picture where one person does the shading (pencil) and another does the colors (crayons). If we tried to fix the whole thing at once, the colors would get messed up and look fake.
            
            Instead, we do this:
            - We separate the shading from the colors.
            - We **ONLY** fix the shading to make it clearer.
            - We put the original colors back on top.
            This way, the image looks bright and sharp, but the colors stay natural.

            ### 📊 3. Reading the Graphs
            **What do those lines mean?**
            The graphs show you how many dark vs light pixels are in the image:
            - A big 'hump' in the middle means the image is flat and grey.
            - A flat, wide line means the image has a great balance of darks, lights, and everything in between.
            """)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Ready. Please upload an image from the sidebar to start.")
    
    # Placeholder layout
    col1, col2 = st.columns(2)
    with col1:
        st.info("Original View Pending...")
    with col2:
        st.info("Enhanced View Pending...")
