class File:
    def __init__(self, file_name: str, date_modified: str, file_format: str, file_size: int):
        self.file_name = file_name
        self.date_modified = date_modified
        self.file_format = file_format
        self.file_size = file_size

    def __repr__(self):
        return (f"File(file_name='{self.file_name}', "
                f"date_modified='{self.date_modified}', file_format='{self.file_format}', "
                f"file_size={self.file_size})")

