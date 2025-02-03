from hardware.screen_utilities import Screen
from hardware.monitor_utilities import Monitor
from core.app_state import AppState
from core.app_constants import AppConstants
from config.logger import Logger
import traceback
from utilities.utils import show_message


logger = Logger.get_logger(__file__)


class ScreenshotCollector:

    # def __init__(self, canvas_handler):
    #     self.canvas_handler = canvas_handler

    def start_collection(self):
        # previous_window_name = None
        # previous_monitor_handle = None
        previous_window = None
        counter = 1
        try:
            while AppState.is_recording:
                cursor_pos = Screen.get_cursor_position()
                window_hwnd = Screen.get_window_handle(cursor_pos)
                ancestor_handle = Screen.get_ancestor_handle(window_hwnd)
                window_name = Screen.get_window_text(ancestor_handle)

                if window_name != AppConstants.RECORDER_WINDOW_TITLE:
                    # detect if the window is desktop or any other window
                    if window_name == "Program Manager":
                        # monitor = Monitor()
                        hMonitor = Monitor.get_monitor_handle_under_cursor()
                        if previous_window != hMonitor and AppState.is_recording:
                            previous_window = hMonitor
                            # print(f"Current monitor handle : {hMonitor}")
                            ss = Monitor.capture_monitor(hMonitor)
                            # ss = Monitor.capture_monitor()
                            AppState.screen_shot = ss
                            AppState.current_window_name = "Desktop " + str(hMonitor)
                            print(AppState.current_window_name)
                            # self.canvas_handler.set_canvas_image(image=ss)
                            # ss.save(f"ss_{counter}.png")
                            counter += 1
                    else:
                        if previous_window != window_name and AppState.is_recording:

                            previous_window = window_name
                            # print(f"{window_name} ({ancestor_handle})")
                            ss = Screen.capture_window(ancestor_handle)
                            AppState.screen_shot = ss
                            AppState.current_window_name = window_name
                            print(AppState.current_window_name)
                            # self.canvas_handler.set_canvas_image(image=ss)
                            # ss.save(f"ss_{counter}.png")
                            counter += 1
        except Exception as e:
            logger.error(f"Error occurred: {e.args[0]}")
            error_messages = traceback.format_exc().splitlines()
            for err in error_messages:
                logger.error(err)