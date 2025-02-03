import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from config.logger import Logger
from core.app_state import AppState
from core.app_constants import AppConstants
from core.canvas_handler import CanvasHandler
import sys
import os


logger = Logger.get_logger(__file__)


class ExplorerWindow:
    def __init__(self, parent_window, start_full_screen=True):
        self.parent_window = parent_window
        self.window = ttk.Toplevel(self.parent_window)
        self.window.title(AppConstants.EXPLORER_WINDOW_TITLE)
        if start_full_screen: self.window.state("zoomed")
        self.adjust_window(AppConstants.EXPLORER_WINDOW_WIDTH,
                           AppConstants.EXPLORER_WINDOW_HEIGHT)
        self.window.iconbitmap('../assets/img/ico_app.ico')
        self.create_elements()
        self.bind_events()

    def adjust_window(self, width, height):
        self.window.resizable(True, True)
        self.window.minsize(width, height)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (width / 2))
        y_cordinate = int((screen_height / 2) - (height / 2))
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x_cordinate, y_cordinate))

    def create_elements(self):
        # Configure columns for layout (10% - 80% - 10%)
        self.window.columnconfigure(0, weight=10)
        self.window.columnconfigure(1, weight=85)
        self.window.columnconfigure(2, weight=5)
        self.window.rowconfigure(0, weight=1)

        self.frame_buttons = ttk.LabelFrame(self.window, text=" Operations ", padding=2, borderwidth=1, relief="solid", bootstyle="info")
        self.frame_main_image = ttk.LabelFrame(self.window, text=" Display Image ", padding=2, borderwidth=1, relief="solid", bootstyle="info")
        self.frame_thumbnails = ttk.LabelFrame(self.window, text=" Images ", padding=2, borderwidth=1, relief="solid", bootstyle="info")

        self.frame_buttons.grid(row=0, column=0, sticky="nswe", padx=15, pady=5)
        self.frame_main_image.grid(row=0, column=1, sticky="nswe", pady=5)
        self.frame_thumbnails.grid(row=0, column=2, sticky="nswe", padx=15, pady=5)

        # -------------------- Section 1: Button Panel (10%) --------------------

        for i in range(5):
            btn = tk.Button(self.frame_buttons, text=f"Button {i + 1}", width=10)
            btn.pack(pady=5, fill="x", padx=5)

        # -------------------- Section 2: Image Display (80%) --------------------

        self.canvas = tk.Canvas(self.frame_main_image, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Load the default image when the canvas is created
        self.load_main_image("../assets/img/noimage.png")

        # Bind the canvas resize event to a new method
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.current_image_tk = None
        self.current_image = None  # Store original image
        self.rectangles = []  # Store drawn rectangles
        self.start_x, self.start_y = None, None  # Store mouse click positions

        # -------------------- Section 3: Scrollable Thumbnail Images (10%) --------------------

        # Create a Canvas for scrolling
        self.canvas_thumbnails = tk.Canvas(self.frame_thumbnails, bg="gray", width=100)
        self.scrollbar = tk.Scrollbar(self.frame_thumbnails, orient="vertical", command=self.canvas_thumbnails.yview)

        # Configure scrollbar and canvas
        self.canvas_thumbnails.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_thumbnails.pack(side="left", fill="both", expand=True, padx=20)

        # Create a frame inside the canvas to hold the thumbnails
        self.frame_thumbnails_inner = tk.Frame(self.canvas_thumbnails, bg="gray")
        self.canvas_thumbnails.create_window((0, 0), window=self.frame_thumbnails_inner, anchor="nw", tags="inner_frame")

        # Bind the inner frame's configure event to update the scroll region
        self.frame_thumbnails_inner.bind("<Configure>", self.on_frame_configure)
        # Bind mouse wheel for scrolling
        self.canvas_thumbnails.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Thumbnail images (Replace with actual paths)
        thumbnail_paths = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg"]
        parent_dir = os.path.dirname(os.path.dirname(sys.argv[0]))
        root_dir = os.path.join(parent_dir, "assets", "img", "test")
        self.thumbnail_paths = [os.path.join(root_dir, path) for path in thumbnail_paths]
        self.thumbnail_images = []
        # Add thumbnails to the inner frame
        for thumb_path in self.thumbnail_paths:
            img_thumb = Image.open(thumb_path)
            img_thumb = img_thumb.resize((100, 100), Image.Resampling.LANCZOS)
            img_thumb_tk = ImageTk.PhotoImage(img_thumb)
            self.thumbnail_images.append(img_thumb_tk)  # Prevent garbage collection
            btn_thumb = tk.Button(self.frame_thumbnails_inner, image=img_thumb_tk,
                                  command=lambda p=thumb_path: self.on_thumbnail_click(p))
            btn_thumb.pack(pady=5)
            lbl_name = ttk.Label(self.frame_thumbnails_inner, text=os.path.basename(thumb_path))
            lbl_name.pack()

        # Bind window resize event to adjust thumbnails
        self.window.bind("<Configure>", self.on_window_resize)
        # Flag to prevent infinite recursion
        self.is_resizing = False
        # set the first image of the list inside the canvas
        self.load_main_image(self.thumbnail_paths[0])

    def on_window_resize(self, event):
        """
        Adjust the thumbnails to stay centered when the window is resized.
        """
        # Check if the widgets still exist
        if not self.frame_thumbnails_inner.winfo_exists() or not self.canvas_thumbnails.winfo_exists():
            return  # Exit if the widgets no longer exist

        if self.is_resizing:
            return  # Prevent re-entering this method while it's already executing

        self.is_resizing = True  # Set the flag to True

        try:
            # Update the width of the inner frame to match the canvas width
            canvas_width = self.canvas_thumbnails.winfo_width()
            self.frame_thumbnails_inner.config(width=canvas_width)

            # Re-center the thumbnails
            self.frame_thumbnails_inner.update_idletasks()

            # Update the scroll region to encompass the inner frame
            self.canvas_thumbnails.configure(scrollregion=self.canvas_thumbnails.bbox("all"))

            # Ensure the inner frame is centered horizontally
            self.canvas_thumbnails.itemconfig("inner_frame", width=canvas_width)
        finally:
            self.is_resizing = False  # Reset the flag after execution

    # Scroll with mouse wheel
    def on_mouse_wheel(self, event):
        """Enable scrolling with mouse wheel."""
        if event.num == 4:  # Linux scroll up
            self.canvas_thumbnails.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas_thumbnails.yview_scroll(1, "units")
        else:  # Windows and macOS
            self.canvas_thumbnails.yview_scroll(-1 * (event.delta // 120), "units")

    def on_thumbnail_click(self, image_path):
        """Update the main image when a thumbnail is clicked."""
        self.load_main_image(image_path)

    # Enable scrolling
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas_thumbnails.configure(scrollregion=self.canvas_thumbnails.bbox("all"))

    def load_main_image(self, image_path):
        """Loads and displays an image in the canvas and keeps it centered."""
        # Load the image if a new path is provided
        if image_path is not None:
            self.current_image = Image.open(image_path)

        # Get the current canvas size
        self.window.update_idletasks()  # Ensures the window size is updated
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Resize the image to fit the canvas while maintaining aspect ratio
        img_width, img_height = self.current_image.size
        aspect_ratio = img_width / img_height

        if canvas_width / aspect_ratio <= canvas_height:
            new_width = canvas_width
            new_height = int(canvas_width / aspect_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * aspect_ratio)

        # Resize the image only if the canvas size has changed
        if new_width != img_width or new_height != img_height:
            self.current_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.current_image_tk = ImageTk.PhotoImage(self.current_image)

        # Clear previous image and place new one at center
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, anchor="center", image=self.current_image_tk)

    def on_canvas_resize(self, event):
        """Handle canvas resizing and adjust the image accordingly."""
        if hasattr(self, 'current_image') and self.current_image is not None:
            self.load_main_image(None)  # Pass None to avoid reloading the image

    def bind_events(self):
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        if self.window:
            # Unbind the resize event to prevent further calls
            self.window.unbind("<Configure>")
            self.window.destroy()
            self.window = None
            self.parent_window.enable_start_recording_button()