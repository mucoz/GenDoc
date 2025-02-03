import os.path
import time
import tkinter as tk
from PIL import Image, ImageTk
import traceback
from core.app_constants import AppConstants
from core.app_state import AppState
from core.app_exceptions import *
from utilities.kthread import KThread
from utilities.utils import show_message
from config.logger import Logger
from config.language_manager import LanguageManager
from hardware.listener_keyboard import KeyboardListener
from hardware.listener_mouse import MouseListener
from config.configurator import Configurator
from database.db_session import DatabaseSession
from database.db_models import DatabaseModels


logger = Logger.get_logger(__file__)


class SplashWindow:
    def __init__(self, project_directory, on_load_complete_callback=None):
        self.project_directory = project_directory
        self.on_load_complete_callback = on_load_complete_callback
        self.window = tk.Tk()
        self.window.title(AppConstants.SPLASH_WINDOW_TITLE)
        self.adjust_window(AppConstants.SPLASH_WINDOW_WIDTH, AppConstants.SPLASH_WINDOW_HEIGHT)
        self.create_elements()
        self.bind_events()
        self.drag_start_x = None
        self.drag_start_y = None
        self.data_loading_thread = None
        self.start_data_loading()

    def start_data_loading(self):
        # Start data loading in a background thread
        self.data_loading_thread = KThread(target=self.load_data, daemon=True)
        self.data_loading_thread.start()

    def load_data(self):
        try:

            self.messages = {
                "1": "Initializing configurator...",
                "2": "Initializing keyboard listener...",
                "3": "Initializing mouse listener...",
                "4": "Initializing DB Session...",
                "5": "Initializing language package..."
            }

            logger.info(self.messages["1"])
            self.label_info["text"] = self.messages["1"]
            AppState.config_parser = Configurator()
            if not AppState.config_parser.verified():
                raise ConfigNotVerifiedException("Configuration verification failed.")

            logger.info(self.messages["2"])
            self.label_info["text"] = self.messages["2"]
            AppState.keyboard_listener = KeyboardListener()

            logger.info(self.messages["3"])
            self.label_info["text"] = self.messages["3"]
            AppState.mouse_listener = MouseListener()

            logger.info(self.messages["4"])
            self.label_info["text"] = self.messages["4"]
            db_path = os.path.join(self.project_directory, "test.db")
            AppState.db_session = DatabaseSession(db_path)
            db_engine = AppState.db_session.get_engine()
            db_models = DatabaseModels()
            db_models.generate_models(db_engine)

            # TODO : read the language from the db and provide it to language manager
            logger.info(self.messages["5"])
            self.label_info["text"] = self.messages["5"]
            AppState.language_manager = LanguageManager()
            AppState.language_manager.set_language("en")

            if not AppState.splash_screen_cancelled:
                logger.info("Data loaded successfully.")
                self.window.after(0, self.on_load_complete)  # Notify main thread
        except Exception as e:
            logger.error(f"Error occurred: {e.args[0]}")
            error_messages = traceback.format_exc().splitlines()
            for err in error_messages:
                logger.error(err)
            show_message("Error", e.args[0], 16)
            AppState.error_occured = True
            self.cancel_splash_screen()

    def on_load_complete(self):
        # Close the splash screen and trigger the main window
        self._on_closing()
        if self.on_load_complete_callback:
            self.on_load_complete_callback()

    def cancel_splash_screen(self):
        if AppState.error_occured:
            logger.info("Error occurred while loading the application.")
        else:
            logger.info("Splash screen canceled by user.")
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
        self.bg_image_path = "../assets/img/splash.png"  # Replace with your image path
        self.canvas = tk.Canvas(self.window, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        # Load the image initially
        self.original_image = Image.open(self.bg_image_path)
        self._update_image(self.window.winfo_width(), self.window.winfo_height())
        # button for closing the window
        button_close = tk.Button(self.window, text=' X ', font=("Arial", 12), command=self.cancel_splash_screen, fg='white', bg='red', cursor='hand2')
        button_close.place(relx=0.98, rely=0.02, anchor='ne')
        # label for showing the loading messages
        self.label_info = tk.Label(self.window, text="Loading...", font=("Arial", 12, "bold"), fg="black", bg="white")
        self.label_info.pack(side=tk.LEFT, padx=1, pady=1, fill=tk.X, expand=True)

    def bind_events(self):
        self.window.bind("<ButtonPress-1>", self._start_moving_window)
        self.window.bind("<ButtonRelease-1>", self._stop_moving_window)
        self.window.bind("<B1-Motion>", self._on_window_move)
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.window.bind("<Configure>", self._resize_image)

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
        logger.info("Closing Splash screen...")
        self.window.destroy()
