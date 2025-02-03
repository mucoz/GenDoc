import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from config.logger import Logger
from core.app_constants import AppConstants
from core.app_state import AppState
from core.canvas_handler import CanvasHandler
from hardware.screen_utilities import Screen
from gui.magnetic_window import MagneticWindow
from gui.window_explorer import ExplorerWindow
from PIL import Image, ImageTk
from core.ss_collector import ScreenshotCollector
from utilities.kthread import KThread
from time import sleep


logger = Logger.get_logger(__file__)


# TODO : last captured window labels
# TODO : Sağ tıklanınca ve taskbar ın adı çıkmıyor. Bir yol bul. Mouse kordinatlarından task bar tespit edilebilir.
class RecorderWindow(MagneticWindow):
    def __init__(self, parent_window):
        self.parent_window = parent_window
        super().__init__()
        self.window = self
        self.window.attributes("-alpha", 0.9)
        self.window.title(AppConstants.RECORDER_WINDOW_TITLE)
        self.adjust_window(AppConstants.RECORDER_WINDOW_WIDTH,
                           AppConstants.RECORDER_WINDOW_HEIGHT)
        self.window.iconbitmap('../assets/img/ico_app.ico')
        self.create_elements()
        # self.bind_events()
        self.ss_collector_thread = None
        self.initialize_recording()

    def adjust_window(self, width, height):
        self.window.resizable(False, False)
        self.window.minsize(width, height)
        self.window.attributes("-topmost", True)
        self.window.overrideredirect(True)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        taskbar_offset = Screen.get_taskbar_height()
        x = screen_width - AppConstants.RECORDER_WINDOW_WIDTH
        y = screen_height - AppConstants.RECORDER_WINDOW_HEIGHT - taskbar_offset
        self.window.geometry(f"+{x}+{y}")

    def create_elements(self):

        self.small_font = ("Arial", 8)

        self.canvas = tk.Canvas(self.window, width=50, height=50, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.circle = self.canvas.create_oval(15, 15, 25, 25, fill="red", outline="", width=0)
        self.label = tk.Label(self.window, text="Recording...", font=self.small_font)
        self.label.place(x=30, y=10)

        self.style1 = ttk.Style()
        self.style1.configure("Small.TButton", padding=3, font=self.small_font, relief="solid")

        self.button_close = ttk.Button(self.window, text="Close", command=self.confirm_close, bootstyle="secondary", style="Small.TButton", width=5)
        self.button_close.place(relx=0.98, rely=0, anchor="ne", x=-5, y=10)

        self.button_complete = ttk.Button(self.window, text="Save&Finish", command=self.complete_recording, bootstyle="primary", style="Small.TButton", width=12)
        self.button_complete.place(relx=0.98, rely=0, anchor="ne", x=-60, y=10)

        self.label_info = ttk.Label(self.window, text="Press CTRL + SHIFT + Z to UNDO", font=self.small_font)
        self.label_info.place(relx=0.5, rely=0.2, anchor="center")

        # Create the canvas
        self.canvas_ss = tk.Canvas(self.window, width=AppConstants.RECORDER_CANVAS_WIDTH,
                                   height=AppConstants.RECORDER_CANVAS_HEIGHT, bg="white")
        self.canvas_ss.place(relx=0.5, rely=0.55, anchor="center")

        # Load the image
        image_path = "../assets/img/noimage.png"
        no_image = Image.open(image_path)

        self.canvas_handler = CanvasHandler(self.canvas_ss,
                                        canvas_width=AppConstants.RECORDER_CANVAS_WIDTH,
                                        canvas_height=AppConstants.RECORDER_CANVAS_HEIGHT)
        self.canvas_handler.set_canvas_image(image=no_image)


        self.label_current_window = ttk.Label(self.window, text="Current Window: Not Selected", font=self.small_font)
        self.label_current_window.place(relx=0.05, rely=0.88, anchor="w")

        self.label_last_captured = ttk.Label(self.window, text="Last Captured: None", font=("Helvetica", 8))
        self.label_last_captured.place(relx=0.05, rely=0.95, anchor="w")

        self.is_blinking = False
        self.start_blinking()

    def initialize_recording(self):
        AppState.captured_images = []
        AppState.is_recording = True
        self.ss_collector_thread = KThread(target=self.collect_ss)
        self.display_info_thread = KThread(target=self.display_info)
        self.ss_collector_thread.start()
        self.display_info_thread.start()

    def display_info(self):
        last_window_name = None
        while AppState.is_recording:
            if AppState.current_window_name != last_window_name:
                last_window_name = AppState.current_window_name
                self.canvas_handler.set_canvas_image(image=AppState.screen_shot)
                self.label_current_window["text"] = "Current Window: " + self.format_label_text(AppState.current_window_name)

    def format_label_text(self, text, max_length=35):
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    def collect_ss(self):
        self.ss_collector = ScreenshotCollector() # self.canvas_handler
        self.ss_collector.start_collection()

    # def bind_events(self):
    #     self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def start_blinking(self):
        if not self.is_blinking:
            self.is_blinking = True
            self.blink()

    def blink(self):
        """Blink the circle by toggling its visibility."""
        if not self.is_blinking or self.window is None:
            return

        # Toggle visibility
        current_fill = self.canvas.itemcget(self.circle, "fill")
        new_fill = "" if current_fill == "red" else "red"
        self.canvas.itemconfig(self.circle, fill=new_fill)

        # Schedule next blink
        if self.window:
            self.window.after(500, self.blink)  # Adjust the delay

    def stop_blinking(self):
        """Stop the blinking animation."""
        self.is_blinking = False
        if self.window:
            self.canvas.itemconfig(self.circle, fill="red")

    def confirm_close(self):
        """Show confirmation dialog before closing."""
        if self.window:
            response = messagebox.askyesno("Confirm Close", "Do you want to stop recording without saving?")
            if response:
                # reset restored pictures from AppState
                AppState.captured_images = []
                AppState.is_recording = False
                self.stop_blinking()
                self.window.destroy()
                self.window = None
                self.parent_window.enable_start_recording_button()

    def complete_recording(self):
        """Handle the completion of the recording."""
        if self.window:
            AppState.is_recording = False
            self.stop_blinking()
            self.window.destroy()
            self.window = None
            logger.info("Opening Explorer Window...")
            self.explorer_window = ExplorerWindow(self.parent_window)
            # TODO : condisyon eklenecek : eğer resim kaydedilmişse show explorer window
            # TODO : yoksa, ana windowu göster ve new record butonunu aktif et

    def window_exists(self):
        if self.window:
            return self.window.winfo_exists()
        return False

    # def _on_closing(self):
    #     if self.window:
    #         # self.ss_collector_thread.kill()
    #         AppState.is_recording = False
    #         self.stop_blinking()
    #         self.window.destroy()
    #         self.window = None
    #         self.parent_window.enable_start_recording_button()
