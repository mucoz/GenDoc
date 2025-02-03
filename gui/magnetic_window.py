import ttkbootstrap as ttk
from hardware.screen_utilities import Screen


class MagneticWindow(ttk.Toplevel):
    def __init__(self, magnetic_threshold=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskbar_height = Screen.get_taskbar_height()
        self.magnetic_threshold = magnetic_threshold
        self.drag_start_x = None
        self.drag_start_y = None
        self.cursor_in_corner = False
        self.snapped_left = False
        self.snapped_right = False
        self.snapped_up = False
        self.snapped_down = False
        self.snapped_top_left = False
        self.snapped_top_right = False
        self.snapped_bottom_left = False
        self.snapped_bottom_right = False
        self.bind("<ButtonPress-1>", self._start_moving_window)
        self.bind("<ButtonRelease-1>", self._stop_moving_window)
        self.bind("<B1-Motion>", self._on_window_move)

    def _start_moving_window(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _stop_moving_window(self, event):
        self.drag_start_x = None
        self.drag_start_y = None

    def _on_window_move(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_width = self.winfo_width()
        win_height = self.winfo_height()
        win_x = self.winfo_x()
        win_y = self.winfo_y()
        x = win_x + dx
        y = win_y + dy
        if not self.cursor_in_corner:
            # left
            if abs(win_x) < self.magnetic_threshold and not self.snapped_left:
                self.geometry(f"+0+{win_y}")
                self.snapped_left = True
            if self.snapped_left and dx > self.magnetic_threshold:
                self.snapped_left = False
                self.geometry(f"+{win_x + dx}+{win_y}")
            if self.snapped_left:
                self.geometry(f"+{0}+{y}")
            # right
            if abs((screen_width - (
                    win_x + win_width))) < self.magnetic_threshold and not self.snapped_right:
                self.geometry(f"+{screen_width - win_width}+{win_y}")
                self.snapped_right = True
            if self.snapped_right and abs(dx) > self.magnetic_threshold:
                self.snapped_right = False
                self.geometry(f"+{win_x + dx}+{dy}")
            if self.snapped_right:
                self.geometry(f"+{screen_width - win_width}+{y}")
            # top
            if win_y < self.magnetic_threshold and not self.snapped_up:
                self.snapped_up = True
                self.geometry(f"+{win_x}+{0}")
            if self.snapped_up and dy > self.magnetic_threshold:
                self.snapped_up = False
                self.geometry(f"+{win_y + dy}+{win_y}")
            if self.snapped_up:
                self.geometry(f"+{x}+{0}")
            # down
            if abs((screen_height - (
                    win_y + win_height) - self.taskbar_height)) < self.magnetic_threshold and \
                    not self.snapped_down:
                self.geometry(f"+{win_x}+{screen_height - win_height - self.taskbar_height}")
                self.snapped_down = True
            if self.snapped_down and abs(dy) > self.magnetic_threshold:
                self.snapped_down = False
                self.geometry(f"+{win_x}+{win_y + dy}")
            if self.snapped_down:
                self.geometry(f"+{x}+{screen_height - self.taskbar_height - win_height}")
            # if not snapped :
            if not self.snapped_left and not self.snapped_right and not self.snapped_up and not self.snapped_down:
                self.geometry(f"+{x}+{y}")

        # top-left corner
        if abs(win_x) < self.magnetic_threshold and abs(win_y) < self.magnetic_threshold and \
                not self.snapped_top_left:
            self.geometry(f"+{0}+{0}")
            self.snapped_top_left = True
            self.cursor_in_corner = True
            self._disable_edges()
        if self.snapped_top_left and self.cursor_in_corner and dx > self.magnetic_threshold and \
                dy > self.magnetic_threshold:
            self.snapped_top_left = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{win_y + dy}")
        if self.snapped_top_left and self.cursor_in_corner and dx > self.magnetic_threshold:
            self.snapped_top_left = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{0}")
        if self.snapped_top_left and self.cursor_in_corner and dy > self.magnetic_threshold:
            self.snapped_top_left = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{0}+{win_y + dy}")
        # top-right corner
        if abs((screen_width - (win_x + win_width))) < self.magnetic_threshold and \
            win_y < self.magnetic_threshold and not self.snapped_top_right:
            self.geometry(f"+{screen_width - win_width}+{0}")
            self.snapped_top_right = True
            self.cursor_in_corner = True
            self._disable_edges()
        if self.snapped_top_right and self.cursor_in_corner and abs(dx) > self.magnetic_threshold and dy > self.magnetic_threshold:
            self.snapped_top_right = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{win_y + dy}")
        if self.snapped_top_right and self.cursor_in_corner and abs(dx) > self.magnetic_threshold:
            self.snapped_top_right = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{0}")
        if self.snapped_top_right and self.cursor_in_corner and dy > self.magnetic_threshold:
            self.snapped_top_right = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{screen_width - win_width}+{win_y + dy}")
        # bottom-right corner
        if (screen_width - (win_x + win_width)) < self.magnetic_threshold and \
                ((screen_height - self.taskbar_height) - (win_y + win_height)) < self.magnetic_threshold and \
            not self.snapped_bottom_right:
            self.geometry(f"+{screen_width - win_width}+{screen_height - self.taskbar_height - win_height}")
            self.snapped_bottom_right = True
            self.cursor_in_corner = True
            self._disable_edges()
        if self.snapped_bottom_right and self.cursor_in_corner and abs(dx) > self.magnetic_threshold and \
                abs(dy) > self.magnetic_threshold:
            self.snapped_bottom_right = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{win_y + dy}")
        if self.snapped_bottom_right and self.cursor_in_corner and abs(dx) > self.magnetic_threshold:
            self.snapped_bottom_right = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{screen_height - win_height}")
        if self.snapped_bottom_right and self.cursor_in_corner and abs(dy) > self.magnetic_threshold:
            self.snapped_bottom_right = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{screen_width - win_width}+{win_y + dy}")
        # bottom-left corner
        if abs(win_x) < self.magnetic_threshold and \
                ((screen_height - self.taskbar_height) - (win_y + win_height)) < self.magnetic_threshold and \
            not self.snapped_bottom_left:
            self.geometry(f"+{0}+{screen_height - self.taskbar_height - win_height}")
            self.snapped_bottom_left = True
            self.cursor_in_corner = True
            self._disable_edges()
        if self.snapped_bottom_left and self.cursor_in_corner and dx > self.magnetic_threshold and \
                abs(dy) > self.magnetic_threshold:
            self.snapped_bottom_left = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{win_y + dy}")
        if self.snapped_bottom_left and self.cursor_in_corner and abs(dy) > self.magnetic_threshold:
            self.snapped_bottom_left = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{0}+{win_y + dy}")
        if self.snapped_bottom_left and self.cursor_in_corner and dx > self.magnetic_threshold:
            self.snapped_bottom_left = False
            self.cursor_in_corner = False
            self._disable_edges()
            self.geometry(f"+{win_x + dx}+{(screen_height - self.taskbar_height - win_height)}")

    def _disable_edges(self):
        self.snapped_left = False
        self.snapped_right = False
        self.snapped_up = False
        self.snapped_down = False