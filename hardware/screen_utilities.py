import mss
import win32gui
import win32con
import win32api
import win32ui
from PIL import Image
import ctypes
from ctypes import wintypes, windll
from hardware.monitor_utilities import Monitor


class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]


class Screen:

    @staticmethod
    def get_cursor_position():
        return win32api.GetCursorPos()

    @staticmethod
    def get_window_handle(cursor_pos):
        return win32gui.WindowFromPoint(cursor_pos)

    @staticmethod
    def get_ancestor_handle(hwnd):
        GA_ROOT = 2
        return windll.user32.GetAncestor(hwnd, GA_ROOT)

    @staticmethod
    def get_window_text(hwnd):
        return win32gui.GetWindowText(hwnd)

    # @staticmethod
    # def capture_window(hwnd):
    #     window_dc = win32gui.GetWindowDC(hwnd)
    #     dc_obj = win32ui.CreateDCFromHandle(window_dc)
    #     compatible_dc = dc_obj.CreateCompatibleDC()
    #     left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    #     width = right - left
    #     height = bottom - top
    #
    #     # Create a bitmap object
    #     bitmap = win32ui.CreateBitmap()
    #     bitmap.CreateCompatibleBitmap(dc_obj, width, height)
    #     compatible_dc.SelectObject(bitmap)
    #
    #     # Copy the window's DC into the compatible DC
    #     compatible_dc.BitBlt((0, 0), (width, height), dc_obj, (0, 0), win32con.SRCCOPY)
    #
    #     # Extract the bitmap data
    #     bmp_info = bitmap.GetInfo()
    #     bmp_data = bitmap.GetBitmapBits(True)
    #
    #     # Clean up
    #     dc_obj.DeleteDC()
    #     # Create an image using Pillow
    #     image = Image.frombuffer("RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]), bmp_data, "raw", "BGRX", 0, 1, )
    #     return image

    @staticmethod
    def capture_window(hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        with mss.mss() as sct:
            screenshot = sct.grab({
                "top": top,
                "left": left,
                "width": width,
                "height": height
            })
            img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            return img

    @staticmethod
    def get_taskbar_height():
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        work_area = RECT()
        SPI_GETWORKAREA = 0x0030
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0)
        taskbar_height = screen_height - work_area.bottom
        return taskbar_height

# previous_window_name = None
# previous_monitor_handle = None
# counter = 1
# while True:
#     cursor_pos = Screen.get_cursor_position()
#     window_hwnd = Screen.get_window_handle(cursor_pos)
#     ancestor_handle = Screen.get_ancestor_handle(window_hwnd)
#     window_name = Screen.get_window_text(ancestor_handle)
#
#     # detect if the window is desktop or any other window
#     if window_name == "Program Manager":
#         # monitor = Monitor()
#         hMonitor = Monitor.get_monitor_handle_under_cursor()
#         if previous_monitor_handle != hMonitor:
#             previous_monitor_handle = hMonitor
#             print(f"Current monitor handle : {hMonitor}")
#             ss = Monitor.capture_monitor(hMonitor)
#             ss.save(f"ss_{counter}.png")
#             counter += 1
#     else:
#         if previous_window_name != window_name:
#
#             previous_window_name = window_name
#             print(f"{window_name} ({ancestor_handle})")
#             ss = Screen.capture_window(ancestor_handle)
#             ss.save(f"ss_{counter}.png")
#             counter += 1
