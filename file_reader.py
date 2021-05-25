from os import listdir
from os.path import isfile, join
from icecream import ic

from models.item import Item

class FileReader:

    def __init__(
        self,
        path: str,
        file_name: str
    ):
        self.path = path
        self.file_name = file_name
    
    @staticmethod
    def get_file_names(path: str):
        #ic(path)
        file_names = [f for f in listdir(path) if isfile(join(path, f))]
        return file_names

    def print_lines(self):
        file = open(f"{self.path}/{self.file_name}", "r")
        for line in file:
            print(line)
        file.close()

    def parse_instance_data(self) -> dict:
        file = open(f"{self.path}/{self.file_name}", "r")
        n, capacity = file.readline().split()
        #ic((n, capacity))
        item_list = list()
        for i in range(int(n)):
            value, weight = file.readline().split()
            new_item = Item(weight=float(weight), value=float(value))
            item_list.append(new_item)
        return dict(
            n=int(n),
            capacity=float(capacity),
            item_list=item_list
        )
    
    def parse_solution_data(self) -> float:
        file = open(f"{self.path}/{self.file_name}", "r")
        optimum = float(file.readline())
        #ic(optimum)
        return optimum