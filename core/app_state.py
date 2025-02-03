from typing import List
# from aux_classes import File


class AppState:
    # directory_files: List[File] = []
    project_directory: str = None
    error_occured: bool = False
    splash_screen_cancelled: bool = False
    config_parser: object = None
    keyboard_listener: object = None
    mouse_listener: object = None
    db_session: object = None
    language_manager: object = None

    is_recording = False
    screen_shot = None
    current_window_name = None
    last_captured_window_name = None

    captured_images = []


