import ctypes


def show_message(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)