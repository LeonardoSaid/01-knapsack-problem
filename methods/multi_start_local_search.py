from copy import deepcopy

from file_writer import FileWriter
from models.solution import Solution
from utils.general import General

class MultiStartLocalSearch:

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

    def evaluate_neighborhood(self, solution: Solution, mask_list1, value_list1, weight_list1) -> bool:
        solution_binary = "".join([str(item) for item in solution.item_list])
        solution_number = int(solution_binary, 2)

        mask_list = deepcopy(mask_list1)
        mask_list.reverse()

        for mask in mask_list:
            masked_number = solution_number ^ int(mask, 2)
            masked_binary = bin(masked_number)[2:].zfill(solution.n)

            neighbor = [int(digit) for digit in masked_binary]
            neighbor_weight_list = [a*b for a,b in zip(neighbor, weight_list1)]

            if sum(neighbor_weight_list) <= solution.capacity:
                neighbor_value_list = [a*b for a,b in zip(neighbor, value_list1)]
                if sum(neighbor_value_list) > solution.value:
                    solution.value = sum(neighbor_value_list)
                    solution.weight =sum(neighbor_weight_list)
                    solution.item_list = deepcopy(neighbor)
                    return True

        return False

    def run(self, counter):
        #print(f"ic| Executing Multi Start Local Search with distance {self.distance}")

        if counter == 0:
            self.output_file.write_line(self.output_filename.replace('TEMP-', ''))
            self.output_file.write_line(str(self.solution.optimum))
            self.output_file.write_line(f"{counter} {self.solution.value}")

        mask_list = General.get_mask_list(self.solution.n, self.distance, climb=True)
        (value_list, weight_list) = General.parse_item_list_data(self.item_list)

        counter_stop = 0

        while self.evaluate_neighborhood(self.solution, mask_list, value_list, weight_list):
            counter_stop += 1
            # prevent from looping indefinitely
            if counter_stop >= 100:
                return