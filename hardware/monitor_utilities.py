import ctypes
from ctypes import wintypes
import win32gui
import win32con
import win32ui
from PIL import Image
import mss
import pyautogui


# Define the RECT structure to get monitor boundaries
class RECT(ctypes.Structure):
    _fields_ = [("left", wintypes.LONG),
                ("top", wintypes.LONG),
                ("right", wintypes.LONG),
                ("bottom", wintypes.LONG)]


class MonitorInfo(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", wintypes.DWORD),
    ]


class Monitor:
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    @staticmethod
    def get_monitor_info(hMonitor):
        # Define the monitor info structure
        monitor_info = MonitorInfo()
        monitor_info.cbSize = ctypes.sizeof(MonitorInfo)
        if Monitor.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
            return monitor_info
        return None

    # @staticmethod
    # def capture_monitor():
    #     with mss.mss() as sct:
    #         # Step 1: Get the monitor handle under the cursor
    #         monitor_handle = Monitor.get_monitor_handle_under_cursor()
    #
    #         # Step 2: Map the monitor handle to the appropriate bounding box
    #         for monitor in sct.monitors:
    #             # Use the bounding box to determine if it's the same monitor
    #             left, top, width, height = monitor["left"], monitor["top"], monitor["width"], monitor["height"]
    #
    #             # Use ctypes to match this bounding box with the monitor handle
    #             monitor_info = MonitorInfo()
    #             monitor_info.cbSize = ctypes.sizeof(MonitorInfo)
    #             hMonitor = wintypes.HMONITOR(monitor_handle)
    #             if Monitor.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
    #                 if (monitor_info.rcMonitor.left == left and
    #                         monitor_info.rcMonitor.top == top and
    #                         monitor_info.rcMonitor.right == width and
    #                         monitor_info.rcMonitor.bottom == height):
    #                     print(f"Cursor is on monitor with handle {monitor_handle}: {monitor}")
    #
    #                     # Step 3: Capture the monitor using `mss`
    #                     screenshot = sct.grab(monitor)
    #
    #                     # Convert the screenshot to a PIL Image
    #                     img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
    #                     return img

    @staticmethod
    def capture_monitor(hMonitor):
        # Define a MONITORINFO structure
        # class MonitorInfo(ctypes.Structure):
        #     _fields_ = [
        #         ("cbSize", ctypes.c_ulong),
        #         ("rcMonitor", ctypes.wintypes.RECT),
        #         ("rcWork", ctypes.wintypes.RECT),
        #         ("dwFlags", ctypes.c_ulong)
        #     ]

        # Initialize MONITORINFO
        monitor_info = MonitorInfo()
        monitor_info.cbSize = ctypes.sizeof(MonitorInfo)

        # Get monitor information
        if Monitor.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):

            # Monitor dimensions
            left = monitor_info.rcMonitor.left
            top = monitor_info.rcMonitor.top
            width = monitor_info.rcMonitor.right - monitor_info.rcMonitor.left
            height = monitor_info.rcMonitor.bottom - monitor_info.rcMonitor.top

            print(f"Monitor dimensions: {width}x{height} at ({left}, {top})")

            # Get device contexts
            hdc_screen = win32gui.GetDC(0)  # Device context for the entire screen
            hdc_memory = win32ui.CreateDCFromHandle(hdc_screen)  # Create compatible DC
            hdc_compatible = hdc_memory.CreateCompatibleDC()

            # Create a compatible bitmap
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(hdc_memory, width, height)
            hdc_compatible.SelectObject(bitmap)

            # BitBlt to copy monitor content to the bitmap
            hdc_compatible.BitBlt(
                (0, 0), (width, height),
                hdc_memory,
                (left, top),
                win32con.SRCCOPY
            )

            # Extract bitmap data
            bmp_info = bitmap.GetInfo()
            bmp_data = bitmap.GetBitmapBits(True)

            # Release resources
            hdc_memory.DeleteDC()
            hdc_compatible.DeleteDC()
            win32gui.ReleaseDC(0, hdc_screen)
            win32gui.DeleteObject(bitmap.GetHandle())

            # Convert the bitmap data to an image
            image = Image.frombuffer(
                "RGB",
                (bmp_info["bmWidth"], bmp_info["bmHeight"]),
                bmp_data,
                "raw",
                "BGRX",
                0,
                1
            )
            return image

    @staticmethod
    def _monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitor_info = MonitorInfo()
        monitor_info.cbSize = ctypes.sizeof(MonitorInfo)
        if Monitor.user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
            # Get the cursor position
            cursor_pos = wintypes.POINT()
            Monitor.user32.GetCursorPos(ctypes.byref(cursor_pos))

            # Check if the cursor is inside this monitor's bounds
            if (monitor_info.rcMonitor.left <= cursor_pos.x <= monitor_info.rcMonitor.right and
                monitor_info.rcMonitor.top <= cursor_pos.y <= monitor_info.rcMonitor.bottom):
                ctypes.cast(dwData, ctypes.POINTER(wintypes.HMONITOR))[0] = hMonitor

        return True  # Continue enumeration

    @staticmethod
    def get_monitor_handle_under_cursor():
        # Create a ctypes variable to store the monitor handle
        monitor_handle = wintypes.HMONITOR()

        # Enumerate all monitors
        MonitorEnumProc = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HMONITOR,
            wintypes.HDC,
            ctypes.POINTER(wintypes.RECT),
            wintypes.LPARAM,
        )
        callback = MonitorEnumProc(Monitor._monitor_enum_proc)

        if not Monitor.user32.EnumDisplayMonitors(0, 0, callback, ctypes.byref(monitor_handle)):
            raise RuntimeError("EnumDisplayMonitors failed")

        return monitor_handle.value
