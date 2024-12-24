from configurator import Configurator
from logger import Logger as log
from window_main import MainWindow
from window_splash import SplashWindow
from listener_keyboard import KeyboardListener
from listener_mouse import MouseListener
from app_state import AppState


class Application:
    def __init__(self):
        log.info("Initializing configurator...")
        self.config_parser = Configurator()
        if not self.config_parser.verified():
            return
        log.info("Initializing keyboard listener...")
        self.keyboard_listener = KeyboardListener()
        log.info("Initializing mouse listener...")
        self.mouse_listener = MouseListener()

    def run(self):
        log.info("Opening Splash screen...")
        splash_screen = SplashWindow(self.config_parser, on_load_complete_callback=self.show_main_window)
        splash_screen.display()

    def show_main_window(self):
        if not AppState.splash_screen_cancelled:
            log.info("Opening Main window...")
            main_window = MainWindow(self.config_parser,
                                     self.keyboard_listener,
                                     self.mouse_listener)
            main_window.display()
        else:
            log.info("User cancelled the loading screen.")
        self.finalize()

    def finalize(self):
        pass


if __name__ == "__main__":
    app = Application()
    app.run()
