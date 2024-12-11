from pynput import mouse
from kthread import KThread
from threading import Timer


class MouseListener:
    def __init__(self):
        print("Mouse thread is set.")
        self.mouse_thread = None
        self.click_count = 0
        self.double_click_time = 0.25

    def _listen_mouse(self):
        with mouse.Listener(on_click=self._handle_click) as self.listener:
            self.listener.join()

    def _handle_click(self, x, y, button, pressed):
        if pressed:
            self.click_count += 1

            if self.click_count == 1:
                Timer(self.double_click_time, self._reset_click_count, [x, y, button]).start()
            elif self.click_count == 2:
                self._on_double_click(x, y, button)

    def _on_click(self, x, y, button, pressed):
        """Callback for mouse click events."""
        if pressed:
            if button == mouse.Button.left:
                print(f"Left button clicked at ({x}, {y})")
            elif button == mouse.Button.right:
                print(f"Right button clicked at ({x}, {y})")
        else:
            print(f"{button} released at ({x}, {y})")

    def _on_double_click(self, x, y, button):
        """Callback for mouse double-click events."""
        if button == mouse.Button.left:
            print(f"Double left click at ({x}, {y})")
        elif button == mouse.Button.right:
            print(f"Double right click at ({x}, {y})")

    def _reset_click_count(self, x, y, button):
        if self.click_count == 1:
            self._on_click(x, y, button, True)  # Handle single click
        self.click_count = 0

    def start(self):
        self.mouse_thread = KThread(target=self._listen_mouse)
        self.mouse_thread.start()
        print("Mouse thread started.")

    def is_alive(self):
        if self.mouse_thread:
            return self.mouse_thread.is_alive()
        return False

    def stop(self):
        self.listener.stop()
        self.mouse_thread.kill()
        print("Mouse stopped.")
