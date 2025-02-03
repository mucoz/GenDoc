from config.logger import Logger
from os.path import dirname, abspath
from app_state import AppState


AppState.project_directory = dirname(dirname(abspath(__file__)))
Logger.setup_logging(AppState.project_directory)


from gui.window_main import MainWindow
from gui.window_splash import SplashWindow


logger = Logger.get_logger(__file__)


class Application:
    def __init__(self):
        pass

    def run(self):
        logger.info("Opening Splash screen...")
        splash_screen = SplashWindow(AppState.project_directory, on_load_complete_callback=self.show_main_window)
        splash_screen.display()

    def show_main_window(self):
        if not AppState.splash_screen_cancelled:
            logger.info("Opening Main window...")
            main_window = MainWindow()
            main_window.display()
        else:
            logger.info("User cancelled the loading screen.")
        self.finalize()

    def finalize(self):
        logger.info("Application finalizing...")
        AppState.splash_screen_cancelled = False
        AppState.error_occured = False
        AppState.config_parser = None
        AppState.mouse_listener = None
        AppState.keyboard_listener = None


if __name__ == "__main__":
    app = Application()
    app.run()
