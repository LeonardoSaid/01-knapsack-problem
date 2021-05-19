import itertools
import random
from copy import deepcopy
from icecream import ic

from file_writer import FileWriter
from models.solution import Solution
from models.item import Item

"""
    !!!!!!!!!! NOT WORKING !!!!!!!!!!
"""

class Vns:
    mask_list = None

    def __init__(
        self,
        neighborhood_size: int
    ):
        self.neighborhood_size = neighborhood_size

    @staticmethod
    def kbits(n, k):
        result = []
        for bits in itertools.combinations(range(n), k):
            s = ['0'] * n
            for bit in bits:
                s[bit] = '1'
            result.append(''.join(s))
        return result

    @staticmethod
    def parse_item_list_data(item_list: list):
        value_list = [item.value for item in item_list]
        weight_list = [item.weight for item in item_list]
        return (value_list, weight_list)

    def set_mask_list(self, n: int, distance: int, climb: bool = False) -> list:
        mask_list = []
        if climb:
            for i in range(1, distance + 1):
                mask_list += self.kbits(n, i)
        else:
            mask_list += self.kbits(n, distance)
        self.mask_list = mask_list

    def find_random_neighboring_solution(self, solution: Solution, item_list: list, distance: int) -> Solution:
        (value_list, weight_list) = self.parse_item_list_data(item_list)
        solution_binary = "".join([str(item) for item in solution.item_list])
        solution_number = int(solution_binary, 2)
        #mask_list = get_mask_list(solution.n, distance, True)
        mask_list = deepcopy(self.mask_list)
        random.shuffle(mask_list)

        optimum_value = solution.optimum
        man = 1
        for mask in mask_list:
            masked_number = solution_number ^ int(mask, 2)
            masked_binary = bin(masked_number)[2:].zfill(solution.n)
            neighbor = [int(digit) for digit in masked_binary]
            neighbor_weight_list = [a*b for a,b in zip(neighbor, weight_list)]
            if sum(neighbor_weight_list) <= solution.capacity:
                neighbor_solution = deepcopy(solution)
                neighbor_solution.value = sum([a*b for a,b in zip(neighbor, value_list)])
                neighbor_solution.weight = neighbor_weight_list
                neighbor_solution.item_list = neighbor
                return neighbor_solution
            else:
                man += 1
        
        # is it possible for no valid neighboring solution?
        return solution

    def evaluate_neighborhood(self, solution: Solution, item_list: list, distance: int, climb: bool = False) -> Solution:
        """
            VND ????
            Returns the best neighbor solution IN THE NEIGHBORHOOD with the distance set
            if climb is True, also considers neighbors from smaller distances
        """
        (value_list, weight_list) = self.parse_item_list_data(item_list)
        solution_binary = "".join([str(item) for item in solution.item_list])
        solution_number = int(solution_binary, 2)
        #mask_list = get_mask_list(solution.n, distance, climb)
        mask_list = deepcopy(self.mask_list)

        optimum_value = solution.optimum
        best_neighbor = None

        for mask in mask_list:
            masked_number = solution_number ^ int(mask, 2)
            masked_binary = bin(masked_number)[2:].zfill(solution.n)
            neighbor = [int(digit) for digit in masked_binary]
            neighbor_weight_list = [a*b for a,b in zip(neighbor, weight_list)]
            if sum(neighbor_weight_list) <= solution.capacity:
                neighbor_value_list = [a*b for a,b in zip(neighbor, value_list)]
                if sum(neighbor_value_list) > optimum_value:
                        # optimum_value = sum(neighbor_value_list)
                        # best_neighbor = deepcopy(neighbor)
                        # print(f"best neighbor")
                        # print(best_neighbor)
                        best_neighbor_solution = deepcopy(neighbor)
                        best_neighbor_solution.value = sum([a*b for a,b in zip(neighbor, value_list)])
                        best_neighbor_solution.weight = sum([a*b for a,b in zip(neighbor, weight_list)])
                        best_neighbor_solution.item_list = neighbor
                        #print(f"BEST NEIGHBOR SOLUTION VALUE {best_neighbor_solution.value}")
                        return best_neighbor_solution
        
        # if best_neighbor:
        #     best_neighbor_solution = deepcopy(solution)
        #     best_neighbor_solution.value = sum([a*b for a,b in zip(best_neighbor, value_list)])
        #     best_neighbor_solution.weight = sum([a*b for a,b in zip(best_neighbor, weight_list)])
        #     best_neighbor_solution.item_list = best_neighbor
        #     print(f"BEST NEIGHBOR SOLUTION VALUE {best_neighbor_solution.value}")
        #     return best_neighbor_solution
        # else:
        #     return None

    def run_vns(self, solution: Solution, item_list: list, max_iterations: int, neighborhood_size: int, output_filename: str):
        print(f"ic| run_vns: Executing Variable Neighbourhood Search")
        counter = 0
        output_file = FileWriter(file_name=output_filename)

        output_file.write_line(output_filename.replace('TEMP-', ''))
        output_file.write_line(str(solution.optimum))
        output_file.write_line(f"{counter} {solution.value}")

        for i in range(max_iterations):
            print(f"ic| running iteration {i}")
            initial_solution = solution
            k = 1
            while k <= neighborhood_size:
                # update mask_list size
                self.set_mask_list(solution.n, k)
                initial_solution = self.find_random_neighboring_solution(solution, item_list, k)
                best_neighbor = self.evaluate_neighborhood(initial_solution, item_list, k)

                if best_neighbor:
                    ic(best_neighbor.value)
                ic(solution.value)

                if best_neighbor and best_neighbor.value > solution.value:
                    counter += 1
                    solution = deepcopy(best_neighbor)
                    solution.print_solution()
                    ic(f"{counter} {solution.value}")
                    output_file.write_line(f"{counter} {solution.value}")
                else:
                    k += 1


# def run_vns(solution: Solution, item_list: list, max_iterations: int, neighborhood_size: int, output_filename: str):
#     print(f"ic| run_vns: Executing Variable Neighbourhood Search")
#     counter = 0
#     output_file = FileWriter(file_name=output_filename)

#     output_file.write_line(output_filename.replace('TEMP-', ''))
#     output_file.write_line(str(solution.optimum))
#     output_file.write_line(f"{counter} {solution.value}")

#     max_iterations = 5
#     neighborhood_size = 3

#     for i in range(max_iterations):
#         print(f"ic| running iteration {i}")
#         best_solution = solution
#         k = 1
#         while k <= neighborhood_size:
#             print(f"ic| finding best in k-neighborhood {k}")
#             best_solution = find_random_neighboring_solution(solution, item_list, k)
#             print(best_solution.value)
#             l = 1
#             while l <= neighborhood_size:
#                 print(f"ic| finding best in l-neighborhood {l}")
#                 best_neighbor = evaluate_neighborhood(best_solution, item_list, l)
#                 if best_neighbor:
#                     print(best_neighbor.value)
#                 if best_neighbor and best_neighbor.value > best_solution.value:
#                     best_solution = deepcopy(best_neighbor)
#                     l = 1
#                 else:
#                     l += 1
#                     continue

#                 ic(best_solution.value)
#                 ic(solution.value)

#                 if best_solution.value > solution.value:
#                     counter += 1
#                     solution = deepcopy(best_solution)
#                     solution.print_solution()
#                     ic(f"{counter} {solution.value}")
#                     output_file.write_line(f"{counter} {solution.value}")
#                 else:
#                     k += 1