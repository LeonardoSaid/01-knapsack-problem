from icecream import ic

class FileWriter:
    file = None
    file_name = None

    def __init__(
        self,
        file_name: str,
        mode: str = "write"
    ):
        self.file_name = file_name
        if mode == "append":
            self.file = open(f"{self.file_name}_output.txt", "a")
        else:
            self.file = open(f"{self.file_name}_output.txt", "w")

    @staticmethod
    def rewrite_file(file_to_read: str, file_to_write: str):
        read_file = open(file_to_read, "r")
        write_file = open(file_to_write, "w")
        for line in read_file:
            write_file.write(line)
        read_file.close()
        write_file.close()

    def write_line(self, line: str):
        self.file.write(line + "\n")

    def close_file(self):
        self.file.close()