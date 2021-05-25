import itertools
import random
from copy import deepcopy
from icecream import ic

from file_writer import FileWriter
from models.solution import Solution
from models.item import Item
from utils.general import General

"""
    !!!!!!!!!! NOT WORKING !!!!!!!!!!
"""

class Vns:
    mask_list = None

    def __init__(
        self,
        item_list: list,
        neighborhood_size: int
    ):
        self.neighborhood_size = neighborhood_size
        self.item_list = item_list

    def random_neighbor(self, solution: Solution, distance: int, value_list1, weight_list1):
        mask_list1 = General.get_mask_list(solution.n, distance, climb=False)

        solution_binary = "".join([str(item) for item in solution.item_list])
        solution_number = int(solution_binary, 2)

        mask_list = deepcopy(mask_list1)
        random.shuffle(mask_list)

        for mask in mask_list:
            masked_number = solution_number ^ int(mask, 2)
            masked_binary = bin(masked_number)[2:].zfill(solution.n)
            neighbor = [int(digit) for digit in masked_binary]
            neighbor_weight_list = [a*b for a,b in zip(neighbor, weight_list1)]

            if sum(neighbor_weight_list) <= solution.capacity:
                neighbor_value_list = [a*b for a,b in zip(neighbor, value_list1)]
                solution.value = sum(neighbor_value_list)
                solution.weight =sum(neighbor_weight_list)
                solution.item_list = deepcopy(neighbor)
                return solution

        return None

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
                    return solution

        return None

    def run_vns(self, solution: Solution, item_list: list, max_iterations: int, neighborhood_size: int, output_filename: str):
        print(f"ic| run_vns: Executing Variable Neighbourhood Search")
        counter = 0
        output_file = FileWriter(file_name=output_filename)

        output_file.write_line(output_filename.replace('TEMP-', ''))
        output_file.write_line(str(solution.optimum))
        output_file.write_line(f"{counter} {solution.value}")

        (value_list, weight_list) = General.parse_item_list_data(self.item_list)

        for i in range(max_iterations):
            initial_solution = solution
            k = 1
            while k <= neighborhood_size:
                mask_list = General.get_mask_list(solution.n, k, climb=False)
                initial_solution = self.random_neighbor(solution, k, value_list, weight_list)
                if not initial_solution:
                    continue
                best_neighbor = self.evaluate_neighborhood(initial_solution, mask_list, value_list, weight_list)

                if best_neighbor and best_neighbor.value > solution.value:
                    counter += 1
                    solution = deepcopy(best_neighbor)
                    #solution.print_solution()
                    #ic(f"{counter} {solution.value}")
                    output_file.write_line(f"{counter} {solution.value}")
                else:
                    k += 1
