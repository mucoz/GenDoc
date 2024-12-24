import time
import tkinter as tk
import tkinter.ttk as ttk
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from app_constants import AppConstants
from app_state import AppState
from logger import Logger as log
from time import sleep
from kthread import KThread


class SplashWindow:
    def __init__(self, config_parser, on_load_complete_callback=None):
        self.config_parser = config_parser
        self.on_load_complete_callback = on_load_complete_callback
        self.window = tk.Tk()
        self.window.title(AppConstants.SPLASH_WINDOW_TITLE + " " +
                          self.config_parser.read("CONSTANTS", "ENV") + " " +
                          self.config_parser.read("CONSTANTS", "VERSION")
                          )
        self.adjust_window(AppConstants.SPLASH_WINDOW_WIDTH, AppConstants.SPLASH_WINDOW_HEIGHT)
        self.data_loading_thread = None
        self.create_elements()
        self.drag_start_x = None
        self.drag_start_y = None
        self.window.bind("<ButtonPress-1>", self._start_moving_window)
        self.window.bind("<ButtonRelease-1>", self._stop_moving_window)
        self.window.bind("<B1-Motion>", self._on_window_move)
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.window.bind("<Configure>", self._resize_image)
        self.data_thread = None
        self.start_data_loading()

    def start_data_loading(self):
        # Start data loading in a background thread
        self.data_loading_thread = KThread(target=self.load_data, daemon=True)
        self.data_loading_thread.start()

    def load_data(self):
        try:
            log.info("Starting data loading...")

            for i in range(5):
                print(f"Dataset {i + 1} loading...")
                self.label_info["text"] = f"Dataset {i + 1} loading..."
                self.label_info["width"] = 10 * (i + 1)
                time.sleep(1)

            if not AppState.splash_screen_cancelled:
                log.info("Data loaded successfully.")
                self.window.after(0, self.on_load_complete)  # Notify main thread
        except Exception as e:
            log.error(f"Error loading data: {e}")

    # def update_progress(self, value):
    #     self.progressbar['value'] = value

    def on_load_complete(self):
        # Close the splash screen and trigger the main window
        self._on_closing()
        if self.on_load_complete_callback:
            self.on_load_complete_callback()

    def cancel_splash_screen(self):
        log.info("Splash screen canceled by user.")
        AppState.splash_screen_cancelled = True
        self._on_closing()
        exit(0)  # Exit the application

    def adjust_window(self, width, height):
        self.window.resizable(False, False)
        self.window.minsize(width, height)
        self.window.overrideredirect(True)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (width / 2))
        y_cordinate = int((screen_height / 2) - (height / 2))
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x_cordinate, y_cordinate))

    def create_elements(self):
        # canvas for background image
        self.bg_image_path = "assets/img/splash.png"  # Replace with your image path
        self.canvas = tk.Canvas(self.window, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        # Load the image initially
        self.original_image = Image.open(self.bg_image_path)
        self._update_image(self.window.winfo_width(), self.window.winfo_height())
        # button for closing the window
        button_close = tk.Button(self.window, text=' X ', font=("Arial", 12), command=self.cancel_splash_screen, fg='white', bg='red', cursor='hand2')
        button_close.place(relx=0.98, rely=0.02, anchor='ne')

        # self.label_header = tk.Label(self.window, text="Generate Documents", font=("Arial", 24))
        # self.label_header.place(relx=0.8, rely=0.4, anchor="ne")

        self.label_info = tk.Label(self.window, text="Loading...", font=("Arial", 12, "bold"), fg="white", bg="green")
        self.label_info.pack(side=tk.LEFT, padx=1, pady=1, expand=True)
        # self.progressbar = ttk.Progressbar(self.window, orient='horizontal', length=180, mode='determinate')
        # self.progressbar.pack(side=tk.LEFT, padx=1, pady=1, expand=True)

    def _update_image(self, width, height):
        # Resize the image to fit the current window size
        resized_image = self.original_image.resize((width, height))
        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Add the image to the canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def _resize_image(self, event):
        # Update the image when the window is resized
        if event.widget == self.window:
            self._update_image(event.width, event.height)

    def display(self):
        self.window.mainloop()

    def _start_moving_window(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _stop_moving_window(self, event):
        self.drag_start_x = None
        self.drag_start_y = None

    def _on_window_move(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        win_x = self.window.winfo_x()
        win_y = self.window.winfo_y()
        x = win_x + dx
        y = win_y + dy
        self.window.geometry(f"+{x}+{y}")

    def _on_closing(self):
        log.info("Closing Splash screen...")
        self.window.destroy()
