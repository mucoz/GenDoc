import inspect


class InvalidLanguageError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Labels:
    # window_main.py controlls
    controls = [" Controls ", " Kontroller "]
    saved_docs = [" Saved Documents ", " Kaydedilen Belgeler "]
    files = [" Files ", " Dosyalar "]
    info =  [" Info ", " Durum "]
    new_doc = [" New Doc", " Yeni Belge"]
    settings = [" Settings", " Ayarlar"]
    start_recording = ["Start Recording", "Kaydı Başlat"]
    stop_recording = ["Stop Recording", "Kaydı Durdur"]
    refresh = [" Refresh", " Yenile"]
    directory = ["Directory", "Klasör"]
    select = [" Select", " Seç"]
    message_error_file_open = ["Error opening file", "Dosyayı açarken hata"]
    message_error_file_not_found = ["File not found:", "Dosya bulunamadı:"]
    message_warning_choose_dir = ["Choose a valid directory!", "Geçerli bir dizin seçin!"]
    message_warning_invalid_dir = ["Invalid directory!", "Geçersiz dizin!"]


    caption_error = ["Error", "Hata"]
    caption_warning = ["Warning", "Uyarı"]


class LanguageUtilities:
    @staticmethod
    def print_label_functions():
        variables = [name for name, value in vars(Labels).items() if not callable(value) and not name.startswith("__")]
        pro_tag = "\t@property\n\t"
        for item in variables:
            block = pro_tag + "def " + item.strip() + "(self):" + "\n\t\t" + "return Labels." + item.strip() + "[self.language_index]"
            block += "\n"
            print(block)


class LanguageManager:

    def set_language(self, language="en"):
        if language == "en":
            self.language_index = 0
        elif language == "tr":
            self.language_index = 1
        else:
            raise InvalidLanguageError("Select a valid language : EN, TR")

    @property
    def controls(self):
        return Labels.controls[self.language_index]

    @property
    def saved_docs(self):
        return Labels.saved_docs[self.language_index]

    @property
    def files(self):
        return Labels.files[self.language_index]

    @property
    def info(self):
        return Labels.info[self.language_index]

    @property
    def new_doc(self):
        return Labels.new_doc[self.language_index]

    @property
    def settings(self):
        return Labels.settings[self.language_index]

    @property
    def start_recording(self):
        return Labels.start_recording[self.language_index]

    @property
    def stop_recording(self):
        return Labels.stop_recording[self.language_index]

    @property
    def refresh(self):
        return Labels.refresh[self.language_index]

    @property
    def directory(self):
        return Labels.directory[self.language_index]

    @property
    def select(self):
        return Labels.select[self.language_index]

    @property
    def message_error_file_open(self):
        return Labels.message_error_file_open[self.language_index]

    @property
    def message_error_file_not_found(self):
        return Labels.message_error_file_not_found[self.language_index]

    @property
    def message_warning_choose_dir(self):
        return Labels.message_warning_choose_dir[self.language_index]

    @property
    def message_warning_invalid_dir(self):
        return Labels.message_warning_invalid_dir[self.language_index]

    @property
    def caption_error(self):
        return Labels.caption_error[self.language_index]

    @property
    def caption_warning(self):
        return Labels.caption_warning[self.language_index]


    # TODO : complete rest of the words