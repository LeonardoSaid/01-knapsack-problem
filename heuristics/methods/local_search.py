from copy import deepcopy
from icecream import ic

from file_writer import FileWriter
from models.solution import Solution
from utils.general import General

class LocalSearch:

    def __init__(
        self,
        solution: Solution,
        item_list: list,
        distance: int,
        output_filename: str,
        improved: bool
    ):
        self.solution = solution
        self.item_list = item_list
        self.distance = distance
        self.output_filename = output_filename
        self.improved = improved

    def run(self):
        if self.improved:
            self.run_local_search_improved()
        else:
            self.run_local_search()

    # original code
    def evaluate_neighborhood(self, solution: Solution, item_list: list, distance: int) -> bool:
        optimum_value = solution.value
        optimum_weight = solution.weight
        pos1 = -1
        pos2 = -1
        posd1 = -1
        has_improved = False

        if distance == 1:
            for i in range(solution.n):
                if solution.item_list[i] == 0:
                    aux_weight = solution.weight + item_list[i].weight
                    aux_value = solution.value + item_list[i].value
                else:
                    aux_weight = solution.weight - item_list[i].weight
                    aux_value = solution.value - item_list[i].value
                
                if aux_weight <= solution.capacity and aux_value > optimum_value:
                    pos1 = i
                    optimum_value = aux_value
                    optimum_weight = aux_weight
            
            if pos1 != -1:
                solution.item_list[pos1] = (solution.item_list[pos1] + 1) % 2
                solution.value = optimum_value
                solution.weight = optimum_weight
                return True

            return False

        elif distance == 2:
            for i in range(solution.n):
                if solution.item_list[i] == 0:
                    aux_weight = solution.weight + item_list[i].weight
                    aux_value = solution.value + item_list[i].value
                else:
                    aux_weight = solution.weight - item_list[i].weight
                    aux_value = solution.value - item_list[i].value

                if aux_weight <= solution.capacity and aux_value > optimum_value:
                    posd1 = i
                    optimum_value = aux_value
                    optimum_weight = aux_weight
            
            if posd1 != -1:
                has_improved = True
            
            for i in range(solution.n - 1):
                if solution.item_list[i] == 0:
                    aux_weight = solution.weight + item_list[i].weight
                    aux_value = solution.value + item_list[i].value
                else:
                    aux_weight = solution.weight - item_list[i].weight
                    aux_value = solution.value - item_list[i].value
                
                for j in range(i + 1, solution.n):
                    if solution.item_list[j] == 0:
                        aux_weight2 = aux_weight + item_list[j].weight
                        aux_value2 = aux_value + item_list[j].value
                    else:
                        aux_weight2 = aux_weight - item_list[j].weight
                        aux_value2 = aux_value - item_list[j].value
                    
                    if aux_weight2 <= solution.capacity and aux_value2 > optimum_value:
                        pos1 = i
                        pos2 = j
                        optimum_value = aux_value2
                        optimum_weight = aux_weight2
            
            if pos1 != -1:
                solution.item_list[pos1] = (solution.item_list[pos1] + 1) % 2
                solution.item_list[pos2] = (solution.item_list[pos2] + 1) % 2
                solution.value = optimum_value
                solution.weight = optimum_weight
                return True
            
            if has_improved:
                solution.item_list[posd1] = (solution.item_list[posd1] + 1) % 2
                solution.value = optimum_value
                solution.weight = optimum_weight
                return True

            return False

        return False

    # original code
    def run_local_search(self):
        print(f"ic| run_local_search: Executing Local Search with distance {self.distance}")
        counter = 0
        output_file = FileWriter(file_name=self.output_filename)

        output_file.write_line(self.output_filename.replace('TEMP-', ''))
        output_file.write_line(str(self.solution.optimum))
        output_file.write_line(f"{counter} {self.solution.value}")
        
        while self.evaluate_neighborhood(self.solution, self.item_list, self.distance):
            counter += 1
            self.solution.print_solution()
            ic(f"{counter} {self.solution.value}")
            output_file.write_line(f"{counter} {self.solution.value}")

    # improved method
    def evaluate_neighborhood_improved(self, solution: Solution, mask_list1, value_list1, weight_list1) -> bool:
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

    # improved method
    def run_local_search_improved(self):
        print(f"ic| run_local_search_improved: Executing Local Search with distance {self.distance}")
        counter = 0
        output_file = FileWriter(file_name=self.output_filename)

        output_file.write_line(self.output_filename.replace('TEMP-', ''))
        output_file.write_line(str(self.solution.optimum))
        output_file.write_line(f"{counter} {self.solution.value}")

        mask_list = General.get_mask_list(self.solution.n, self.distance, climb=True)
        (value_list, weight_list) = General.parse_item_list_data(self.item_list)
        while self.evaluate_neighborhood_improved(self.solution, mask_list, value_list, weight_list):
            counter += 1
            #self.solution.print_solution()
            #ic(f"{counter} {self.solution.value}")
            output_file.write_line(f"{counter} {self.solution.value}")