import os
import subprocess
import platform
import time
import utils
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from app_constants import AppConstants
from typing import List
from aux_classes import File


class MainWindow:
    def __init__(self, config_parser, keyboard_listener, mouse_listener):
        self.config_parser = config_parser
        self.keyboard_listener = keyboard_listener
        self.mouse_listener = mouse_listener
        self.window = ttk.Window(themename="superhero")
        self.window.title(AppConstants.MAIN_WINDOW_TITLE + " " +
                          self.config_parser.read("CONSTANTS", "ENV") + " " +
                          self.config_parser.read("CONSTANTS", "VERSION"))
        self.adjust_window(AppConstants.MAIN_WINDOW_WIDTH, AppConstants.MAIN_WINDOW_HEIGHT)
        self.window.iconbitmap(self.config_parser.read("CONSTANTS", "APP_ICON"))
        self.create_elements()
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def adjust_window(self, width, height):
        self.window.resizable(True, True)
        self.window.minsize(width, height)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (width / 2))
        y_cordinate = int((screen_height / 2) - (height / 2))
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x_cordinate, y_cordinate))

    def create_elements(self):
        # configure window for frames
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=10)
        self.window.rowconfigure(3, weight=1)
        self.window.columnconfigure(0, weight=1)

        # frame for buttons
        self.frame_buttons = ttk.Labelframe(self.window, text='Controls', padding=2, borderwidth=1, relief="solid", bootstyle="info")
        self.frame_buttons.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)
        # frame for directory entry and choose folder button
        self.frame_directory = ttk.Labelframe(self.window, text='Saved Documents', padding=2, borderwidth=1, relief="solid", bootstyle="info")
        self.frame_directory.grid(row=1, column=0, sticky="nswe", padx=15, pady=5)
        self.frame_directory.columnconfigure(0, weight=1)  # Refresh button
        self.frame_directory.columnconfigure(1, weight=1)  # Directory label
        self.frame_directory.columnconfigure(2, weight=5)  # Entry will expand
        self.frame_directory.columnconfigure(3, weight=1)  # Button fixed width
        # self.frame_directory.columnconfigure(0, weight=1)
        # frame for list view
        self.frame_listbox = ttk.Labelframe(self.window, text='Files', padding=2, borderwidth=1, relief="solid", bootstyle="info")
        self.frame_listbox.grid(row=2, column=0, sticky="nswe", padx=15, pady=5)
        # frame for footer
        self.frame_footer = ttk.Labelframe(self.window, text='Info', padding=2, borderwidth=1, relief="solid", bootstyle="info")
        self.frame_footer.grid(row=3, column=0, sticky="nswe", padx=15, pady=5)

        # define styles for buttons -------------------------------------

        self.style = ttk.Style()
        self.style.configure("Large.TButton", padding=10, font=("Arial", 12, "bold"), relief="flat")
        self.style.configure("Medium.TButton", padding=5, font=("Verdana", 10), relief="raised")
        self.style.configure("Small.TButton", padding=5, font=("Helvetica", 8), relief="solid")

        # button frame -----------------------------------------------
        # record button
        # ttk.Style().configure("TButton", padding=6, font=("Arial", 12), relief="flat")
        self.icon_record = tk.PhotoImage(file='assets/img/add.png')
        self.button_record = ttk.Button(self.frame_buttons,
                                   text=' New Doc',
                                   image=self.icon_record,
                                   compound="left",
                                   style="Large.TButton"
                                   ) # command=self.keyboard_listener.start
        self.button_record.pack(side=LEFT, padx=15, pady=5, ipadx=5, ipady=5)
        # refresh button
        # self.icon_refresh = tk.PhotoImage(file='assets/img/refresh.png')
        # self.button_refresh = ttk.Button(self.frame_buttons,
        #                                  text=' Refresh',
        #                                  image=self.icon_refresh,
        #                                  compound="left",
        #                                  command=self.refresh_list)
        # self.button_refresh.pack(side=LEFT, padx=15, pady=5, ipady=5)
        # settings button
        self.icon_settings = tk.PhotoImage(file='assets/img/settings.png')
        self.button_settings = ttk.Button(self.frame_buttons,
                                          text=' Settings',
                                          image=self.icon_settings,
                                          compound='left',
                                          style="Large.TButton"
                                          )
        self.button_settings.pack(side=LEFT, padx=15, pady=15, ipadx=5, ipady=5)
        # start recording button
        self.button_start_recording = ttk.Button(self.frame_buttons,
                                                 text='Start Recording',
                                                 compound='left',
                                                 command=self.start_recording)
        self.button_start_recording.pack(side=LEFT, padx=15, pady=15, ipady=7)
        # stop recording button
        self.button_stop_recording = ttk.Button(self.frame_buttons,
                                                text='Stop Recording',
                                                compound='left',
                                                command=self.stop_recording)
        self.button_stop_recording.pack(side=LEFT, padx=15, pady=15, ipady=7)


        # directory frame ------------------------------------------------
        self.icon_refresh = tk.PhotoImage(file='assets/img/refresh.png')
        self.button_refresh = ttk.Button(self.frame_directory,
                                         text=' Refresh',
                                         image=self.icon_refresh,
                                         compound="left",
                                         # style="Small.TButton",
                                         bootstyle=ttk.OUTLINE,
                                         command=self.refresh_list)
        self.button_refresh.pack(side=LEFT, padx=15, pady=5, ipadx=2, ipady=2)
        # label for Directory
        self.label_directory = ttk.Label(self.frame_directory, text='Directory:')
        # self.label_directory.grid(row=0, column=0, sticky="we", padx=15, pady=10)
        self.label_directory.pack(side=LEFT, padx=5, pady=15)
        # Entry widget for directory path
        self.entry_directory = ttk.Entry(self.frame_directory, font=("Arial", 12), width=35)
        self.entry_directory.pack(side=LEFT, padx=15, pady=15, expand=True, fill=X)
        # Button to open the folder dialog
        self.icon_folder = tk.PhotoImage(file='assets/img/folder.png')
        self.button_choose_folder = ttk.Button(
            self.frame_directory,
            text=" Select",
            image=self.icon_folder,
            compound='left',
            # style="Small.TButton",
            bootstyle=ttk.OUTLINE,
            command=self.choose_folder
        )
        # self.button_choose_folder.grid(row=0, column=2, sticky="e", padx=15, pady=10)
        self.button_choose_folder.pack(side=RIGHT, padx=15, pady=15, ipadx=2, ipady=2)

        # listbox frame -------------------------------------
        coldata = [{"text": "File Name", "width": 350},
                   {"text": "Date Modified", "width": 120},
                   {"text": "File Format", "width": 100},
                   {"text": "File Size", "stretch": "True", "width": 100}]
        rowdata = []
        colors = self.window.style.colors
        self.listbox_files = Tableview(self.frame_listbox,
                                       coldata=coldata,
                                       rowdata=rowdata,
                                       paginated=True,
                                       pagesize=20,
                                       searchable=True,
                                       bootstyle=SUCCESS,
                                       stripecolor=(colors.dark, "white"))
        self.listbox_files.pack(fill=BOTH, expand=YES, padx=15, pady=10)
        # Bind double click event
        self.listbox_files.view.bind("<Double-1>", self.on_row_double_click)
        # footer frame ----------------------------------------------------
        self.label_info = ttk.Label(self.frame_footer, font=("Arial", 12), text='Ready.')
        self.label_info.pack(side=LEFT, padx=15, pady=5)

    def start_recording(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop_recording(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def on_row_double_click(self, event):
        # Get the row index where the user double-clicked
        selected = self.listbox_files.view.selection()
        records = []
        for iid in selected:
            record = self.listbox_files.iidmap.get(iid)
            records.append(record.values)
        if records:
            if records[0][0]:
                # Retrieve the corresponding file path
                folder_path = self.entry_directory.get()
                file_path = os.path.join(folder_path, records[0][0])
                # Call the method to open the file
                self.open_file(file_path)

    def open_file(self, file_path):
        """
        Opens the file with the default system application, without showing the command prompt window.
        """
        # Normalize file path to ensure there are no issues with path separators
        file_path = os.path.abspath(file_path)  # Get the absolute path
        file_path = os.path.normpath(file_path)  # Normalize path (handle backslashes correctly)

        if os.path.exists(file_path):
            try:
                os.startfile(file_path)
            except Exception as e:
                utils.show_message("Error", f"Error opening file {file_path}: {e}", 64)
        else:
            utils.show_message("Waning", f"File not found: {file_path}", 16)

    def refresh_list(self):
        path = self.entry_directory.get()
        if not path:
            utils.show_message("Warning", "Choose a valid directory!", 48)
            return
        if not os.path.isdir(path):
            utils.show_message("Warning", "Invalid directory!", 48)
            return
        files = self.collect_files_info(path)
        self.populate_tableview(files)

    def choose_folder(self):
        folder_path = filedialog.askdirectory()  # Open the folder dialog
        if folder_path:
            self.entry_directory.delete(0, tk.END)  # Clear the entry field
            self.entry_directory.insert(0, folder_path)  # Insert the selected folder
            files = self.collect_files_info(folder_path)
            self.populate_tableview(files)

    def collect_files_info(self, directory: str) -> List[File]:
        files_info = []
        try:
            # Get a list of files in the directory
            for entry in os.scandir(directory):
                if entry.is_file():
                    # Get file details
                    file_name = entry.name
                    file_path = entry.path
                    file_stat = os.stat(file_path)

                    # Extract metadata
                    date_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime))
                    file_format = os.path.splitext(file_name)[1][1:].upper()  # Get file extension without the dot
                    file_size = file_stat.st_size  # File size in bytes

                    # Create a File object
                    file_obj = File(file_name, date_modified, file_format, file_size)
                    files_info.append(file_obj)
        except Exception as e:
            utils.show_message("Error", f"Error occurred while accessing directory {directory}: {e}", 16)

        return files_info

    def populate_tableview(self, files: List[File]):
        # Clear existing rows in Tableview
        self.listbox_files.tablerows.clear()
        # Prepare rows for Tableview
        rowdata = [
            (file.file_name, file.date_modified, file.file_format, f"{file.file_size // 1024} KB")
            for file in files
        ]

        # Insert new rows into Tableview
        # Insert new rows at index 0
        self.listbox_files.insert_rows(0, rowdata=rowdata)
        self.listbox_files.load_table_data()
        # self.listbox_files.autofit_columns()
        self.listbox_files.autoalign_columns()

    def display(self):
        self.window.mainloop()

    def _on_closing(self):
        print("Stopping threads...")
        if self.keyboard_listener.is_alive():
            self.keyboard_listener.stop()
        if self.mouse_listener.is_alive():
            self.mouse_listener.stop()
        print("Threads stopped.")
        print("Exiting application.")
        # Destroy the tkinter window
        self.window.destroy()
