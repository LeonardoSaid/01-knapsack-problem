import random
from copy import deepcopy

from file_writer import FileWriter
from models.solution import Solution
from utils.general import General

class SimulatedAnnealing:

    def __init__(
        self,
        solution: Solution,
        item_list: list,
        distance: int,
        output_filename: str
    ):
        self.solution = solution
        self.item_list = item_list
        self.distance = distance
        self.output_filename = output_filename
        # writing output variables
        self.output_file = FileWriter(file_name=self.output_filename)
        self.counter = 0

    def random_neighbor(self, distance: int):
        mask_list1 = General.get_mask_list(self.solution.n, distance, climb=False)
        (value_list1, weight_list1) = General.parse_item_list_data(self.item_list)

        solution_binary = "".join([str(item) for item in self.solution.item_list])
        solution_number = int(solution_binary, 2)

        mask_list = deepcopy(mask_list1)
        random.shuffle(mask_list)

        for mask in mask_list:
            masked_number = solution_number ^ int(mask, 2)
            masked_binary = bin(masked_number)[2:].zfill(self.solution.n)
            neighbor = [int(digit) for digit in masked_binary]
            neighbor_weight_list = [a*b for a,b in zip(neighbor, weight_list1)]

            if sum(neighbor_weight_list) <= self.solution.capacity:
                neighbor_value_list = [a*b for a,b in zip(neighbor, value_list1)]
                self.solution.value = sum(neighbor_value_list)
                self.solution.weight =sum(neighbor_weight_list)
                self.solution.item_list = deepcopy(neighbor)
                return True

        return False
        