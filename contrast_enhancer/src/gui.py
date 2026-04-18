import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import numpy as np
from .engine import ImageEngine
from .visualizer import Visualizer

class ContrastEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PixelPerfect | Contrast Enhancement Studio")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f0f2f5")
        
        # State
        self.original_image = None
        self.processed_image = None
        self.mode = tk.StringVar(value="Color") # "Grayscale" or "Color"
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom Colors
        self.bg_color = "#f0f2f5"
        self.accent_color = "#1a73e8"
        self.sidebar_color = "#ffffff"
        
        style.configure("TFrame", background=self.bg_color)
        style.configure("Sidebar.TFrame", background=self.sidebar_color)
        
        style.configure("Action.TButton", 
                        foreground="white", 
                        background=self.accent_color, 
                        font=("Segoe UI", 10, "bold"),
                        padding=10)
        style.map("Action.TButton", background=[('active', '#1557b0')])

    def create_widgets(self):
        # --- Sidebar ---
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="CONTROLS", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#5f6368").pack(pady=(30, 20))
        
        # Mode Selection
        mode_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        mode_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(mode_frame, text="Enhancement Mode:", bg=self.sidebar_color, 
                 font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        modes = [("Color Enhancement", "Color"), ("Grayscale / BW", "Grayscale")]
        for text, val in modes:
            ttk.Radiobutton(mode_frame, text=text, variable=self.mode, value=val).pack(fill=tk.X, pady=2)

        # Buttons
        self.btn_upload = ttk.Button(self.sidebar, text="📁 Upload Image", 
                                     command=self.load_image, style="Action.TButton")
        self.btn_upload.pack(fill=tk.X, padx=20, pady=(30, 5))
        
        self.btn_apply = ttk.Button(self.sidebar, text="✨ Apply Equalization", 
                                    command=self.process_image, style="Action.TButton")
        self.btn_apply.pack(fill=tk.X, padx=20, pady=10)
        
        self.btn_reset = ttk.Button(self.sidebar, text="🔄 Reset / Clear", 
                                    command=self.reset_app)
        self.btn_reset.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, padx=20, pady=20)

        self.btn_help = ttk.Button(self.sidebar, text="📘 View Concepts", 
                                    command=self.show_concepts)
        self.btn_help.pack(fill=tk.X, padx=20, pady=5)

        # Info Section
        info_label = tk.Label(self.sidebar, text="Supports: JPG, PNG, WEBP\nUses: Global Histogram Equalization", 
                            bg=self.sidebar_color, fg="#9aa0a6", font=("Segoe UI", 8), justify=tk.LEFT)
        info_label.pack(side=tk.BOTTOM, pady=20)

        # --- Main Viewport ---
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header = tk.Label(self.main_container, text="Side-by-Side Comparison", 
                              font=("Segoe UI", 16, "bold"), bg=self.bg_color, fg="#202124")
        self.header.pack(pady=(0, 20), anchor=tk.W)

        # 2x2 Grid for Images and Histograms
        self.grid_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.grid_frame.pack(fill=tk.BOTH, expand=True)

        self.original_panel = self.create_image_panel(self.grid_frame, "Original", 0, 0)
        self.processed_panel = self.create_image_panel(self.grid_frame, "Enhanced Result", 0, 1)
        self.orig_hist_panel = self.create_image_panel(self.grid_frame, "Original Histogram", 1, 0)
        self.proc_hist_panel = self.create_image_panel(self.grid_frame, "Enhanced Histogram", 1, 1)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready. Please upload an image to start.")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, 
                                   relief=tk.SUNKEN, anchor=tk.W, bg="#ffffff", padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_image_panel(self, parent, title, r, c):
        outer = tk.Frame(parent, bg="white", highlightbackground="#dadce0", highlightthickness=1)
        outer.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
        parent.grid_columnconfigure(c, weight=1)
        parent.grid_rowconfigure(r, weight=1)
        
        tk.Label(outer, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#5f6368").pack(pady=5)
        
        display = tk.Label(outer, bg="white", text="No Preview")
        display.pack(fill=tk.BOTH, expand=True)
        return display

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        )
        if not file_path:
            return
            
        try:
            self.original_image = Image.open(file_path).convert("RGB")
            self.update_preview(self.original_panel, self.original_image)
            
            # Generate initial histogram
            image_np = np.array(self.original_image)
            hist_data = ImageEngine.get_histogram_data(image_np)
            hist_plot = Visualizer.create_histogram_plot(hist_data, "Original Histogram")
            self.update_preview(self.orig_hist_panel, hist_plot)
            
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            # Clear previous results
            self.processed_panel.config(image='', text="Pending Processing...")
            self.proc_hist_panel.config(image='', text="Pending Processing...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def process_image(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first.")
            return
            
        self.status_var.set("Processing... Please wait.")
        self.root.update_idletasks()
        
        try:
            img_np = np.array(self.original_image)
            
            if self.mode.get() == "Grayscale":
                processed_np = ImageEngine.equalize_grayscale(img_np)
            else:
                processed_np = ImageEngine.equalize_color(img_np)
                
            self.processed_image = Image.fromarray(processed_np)
            self.update_preview(self.processed_panel, self.processed_image)
            
            # Update New Histograms
            hist_data = ImageEngine.get_histogram_data(processed_np)
            hist_plot = Visualizer.create_histogram_plot(hist_data, "Enhanced Histogram")
            self.update_preview(self.proc_hist_panel, hist_plot)
            
            self.status_var.set(f"Success! Equalization applied using {self.mode.get()} mode.")
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))
            self.status_var.set("Error during processing.")

    def update_preview(self, panel, pil_img):
        # Resize for display while maintaining aspect ratio
        width = panel.winfo_width()
        height = panel.winfo_height()
        
        # Default safety size if window not fully rendered
        if width < 10: width, height = 400, 300
        
        pil_img.thumbnail((width, height), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img)
        panel.config(image=tk_img, text="")
        panel.image = tk_img # Keep reference

    def reset_app(self):
        self.original_image = None
        self.processed_image = None
        for panel in [self.original_panel, self.processed_panel, self.orig_hist_panel, self.proc_hist_panel]:
            panel.config(image='', text="No Preview")
        self.status_var.set("Application Reset.")

    def show_concepts(self):
        # Create a modern top-level window
        help_win = tk.Toplevel(self.root)
        help_win.title("How it Works | Simple Guide")
        help_win.geometry("700x750")
        help_win.configure(bg="#ffffff")
        
        # --- Scrollable Container ---
        canvas = tk.Canvas(help_win, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(help_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse Wheel Support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        help_win.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Simple Content ---
        
        # 1. Header
        header_frame = tk.Frame(scrollable_frame, bg="#1a73e8")
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="HOW IT WORKS", font=("Segoe UI", 24, "bold"), 
                 bg="#1a73e8", fg="white", pady=40).pack()

        # 2. Simple Concept: Contrast
        self.add_section(scrollable_frame, "📈 1. Improving Contrast", 
                        "The 'Elastic Band' Analogy",
                        "Think of an image's brightness like a bunched-up elastic band. "
                        "When an image is dull, all the pixels are stuck in the middle. "
                        "Our tool takes both ends of that band and stretches them out! "
                        "By spreading the darks and lights evenly, the hidden details suddenly become visible.")

        # 3. Simple Concept: Color
        self.add_section(scrollable_frame, "🌈 2. Fixing Color Images", 
                        "The 'Coloring Book' Analogy",
                        "Imagine a picture where one person does the shading (pencil) and another does the colors (crayons). "
                        "If we tried to fix the whole thing at once, the colors would get messed up and look fake. "
                        "\n\nInstead, we do this:\n"
                        "- We separate the shading from the colors.\n"
                        "- We ONLY fix the shading to make it clearer.\n"
                        "- We put the original colors back on top.\n"
                        "This way, the image looks bright and sharp, but the colors stay natural.")

        # 4. Reading the Graphs
        self.add_section(scrollable_frame, "📊 3. Reading the Histograms", 
                        "What do those lines mean?",
                        "The graphs at the bottom show you how many dark vs light pixels are in the image:\n"
                        "- A big 'hump' in the middle means the image is flat and grey.\n"
                        "- A flat, wide line means the image has a great balance of darks, lights, and everything in between.")

        # Footer
        tk.Label(scrollable_frame, text="Simple, Powerful, Pixel Perfect.", 
                 bg="white", font=("Segoe UI", 10, "italic"), fg="#1a73e8", pady=40).pack()

    def add_section(self, parent, title, subtitle, body):
        f = tk.Frame(parent, bg="#f8f9fa", padx=30, pady=20, highlightbackground="#dadce0", highlightthickness=1)
        f.pack(fill=tk.X, padx=40, pady=15)
        
        tk.Label(f, text=title, font=("Segoe UI", 16, "bold"), bg="#f8f9fa", fg="#202124").pack(anchor=tk.W)
        tk.Label(f, text=subtitle, font=("Segoe UI", 11, "bold"), bg="#f8f9fa", fg="#1a73e8").pack(anchor=tk.W, pady=(2, 5))
        
        lbl = tk.Label(f, text=body, font=("Segoe UI", 10), bg="#f8f9fa", fg="#3c4043", justify=tk.LEFT)
        lbl.pack(anchor=tk.W, fill=tk.X, pady=10)
        f.bind("<Configure>", lambda e: lbl.configure(wraplength=e.width - 20))
