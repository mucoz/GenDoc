from pynput.keyboard import Listener
from kthread import KThread


class KeyboardListener:
    def __init__(self):
        print("Keybard thread is set.")
        self.keyboard_thread = None

    def _listen_keyboard(self):
        with Listener(on_press=self._on_press) as self.listener:
            self.listener.join()

    def _on_press(self, key):
        print(key)

    def start(self):
        self.keyboard_thread = KThread(target=self._listen_keyboard)
        self.keyboard_thread.start()
        print("Keyboard started.")

    def is_alive(self):
        if self.keyboard_thread:
            return self.keyboard_thread.is_alive()
        return False

    def stop(self):
        self.listener.stop()
        self.keyboard_thread.kill()
        print("Keyboard stopped.")
