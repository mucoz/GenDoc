from configparser import ConfigParser
import os
from utilities.utils import show_message
from core.app_constants import AppConstants


class Configurator:
    def __init__(self):
        self.config = ConfigParser()

    def verified(self) -> bool:
        if not os.path.exists(AppConstants.CONFIG_FILE_NAME):
            show_message("Error", AppConstants.CONFIG_FILE_NAME + " file does not exist in project folder!", 16)
            return False
        self.config.read("Config.ini")
        return True

    def read(self, section, key):
        return self.config[section][key]
