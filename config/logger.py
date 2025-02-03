import datetime
import os
from logging.config import dictConfig
import logging


class Logger:
    # Class-level variable to store the project root directory
    PROJECT_ROOT = None

    @staticmethod
    def setup_logging(project_directory):
        """
        Configures logging with the specified project root directory.
        """
        Logger.PROJECT_ROOT = os.path.abspath(project_directory)  # Store the project root directory globally

        log_dir = os.path.join(project_directory, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        current_time = datetime.datetime.now()

        # Define logging configuration
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                },
                "detailed": {
                    "format": "%(asctime)s - %(name)s [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "filename": os.path.join(log_dir, f"Log_{current_time.strftime('%Y_%m_%d')}.log"),
                    "formatter": "detailed",
                    "level": "DEBUG",
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "root": {
                "handlers": ["file", "console"],
                "level": "DEBUG",
            },
        }

        # Apply logging configuration
        dictConfig(log_config)

    @staticmethod
    def get_logger(file):
        """
        Returns a logger with a name based on the file's location in the project.
        """
        if Logger.PROJECT_ROOT is None:
            raise ValueError("Project root is not set. Call setup_logging first.")

        # Ensure file paths are absolute for consistent behavior
        file = os.path.abspath(file)

        # Get the relative path of the file within the project directory
        relative_path = os.path.relpath(file, Logger.PROJECT_ROOT)

        # Use the full relative path as the logger name, replacing OS-specific separators with "/"
        logger_name = relative_path.replace(os.sep, "/")

        # Return logger with the constructed name
        return logging.getLogger(logger_name)
