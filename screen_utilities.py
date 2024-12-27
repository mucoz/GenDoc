import win32gui
import win32con
import win32api
import win32ui
from ctypes import windll
from PIL import Image


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

    @staticmethod
    def capture_window(hwnd):
        window_dc = win32gui.GetWindowDC(hwnd)
        dc_obj = win32ui.CreateDCFromHandle(window_dc)
        compatible_dc = dc_obj.CreateCompatibleDC()
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # Create a bitmap object
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dc_obj, width, height)
        compatible_dc.SelectObject(bitmap)

        # Copy the window's DC into the compatible DC
        compatible_dc.BitBlt((0, 0), (width, height), dc_obj, (0, 0), win32con.SRCCOPY)

        # Extract the bitmap data
        bmp_info = bitmap.GetInfo()
        bmp_data = bitmap.GetBitmapBits(True)

        # Clean up
        dc_obj.DeleteDC()
        # Create an image using Pillow
        image = Image.frombuffer("RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]), bmp_data, "raw", "BGRX", 0, 1, )
        return image

# TODO : iki ekranın ayrılması lazım

previous_window_name = None
counter = 1
while True:
    cursor_pos = Screen.get_cursor_position()
    window_hwnd = Screen.get_window_handle(cursor_pos)
    ancestor_handle = Screen.get_ancestor_handle(window_hwnd)
    window_name = Screen.get_window_text(ancestor_handle)

    if previous_window_name != window_name:
        previous_window_name = window_name
        print(f"{window_name} ({ancestor_handle})")
        ss = Screen.capture_window(ancestor_handle)
        ss.save(f"ss_{counter}.png")
        counter += 1