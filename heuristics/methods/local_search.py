import itertools
from functools import reduce
from copy import deepcopy
from icecream import ic

from file_writer import FileWriter
from models.solution import Solution
from models.item import Item

def kbits(n, k):    
    result = []
    for bits in itertools.combinations(range(n), k):
        s = ['0'] * n
        for bit in bits:
            s[bit] = '1'
        result.append(''.join(s))
    #print(f"D ====== {k} iterations {len(result)}")
    return result

def parse_item_list_data(item_list: list):
    value_list = [item.value for item in item_list]
    weight_list = [item.weight for item in item_list]
    return (value_list, weight_list)

def get_mask_list(n: int, distance: int, climb: bool = False) -> list:
    mask_list = []
    if climb:
        for i in range(1, distance + 1):
            mask_list += kbits(n, i)
    else:
        mask_list += kbits(n, distance)
    ic(len(mask_list))
    return mask_list

def evaluate_neighborhood(solution: Solution, item_list: list, distance: int) -> bool:
    optimum_value = solution.value
    optimum_weight = solution.weight
    pos1 = -1
    pos2 = -1
    posd1 = -1
    has_improved = False

    COUNTER = 0

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
            COUNTER += 1
            if solution.item_list[i] == 0:
                aux_weight = solution.weight + item_list[i].weight
                aux_value = solution.value + item_list[i].value
            else:
                aux_weight = solution.weight - item_list[i].weight
                aux_value = solution.value - item_list[i].value
            
            print(f"{aux_value} {aux_weight}")
            
            if aux_weight <= solution.capacity and aux_value > optimum_value:
                posd1 = i
                optimum_value = aux_value
                optimum_weight = aux_weight

        #print(f"D = 1 iterations {COUNTER}")
        COUNTER = 0
        
        if posd1 != -1:
            has_improved = True
        
        for i in range(solution.n - 1):
            if solution.item_list[i] == 0:
                aux_weight = solution.weight + item_list[i].weight
                aux_value = solution.value + item_list[i].value
            else:
                aux_weight = solution.weight - item_list[i].weight
                aux_value = solution.value - item_list[i].value

            #print(f"---- {aux_value} {aux_weight}")
            
            for j in range(i + 1, solution.n):
                COUNTER += 1
                if solution.item_list[j] == 0:
                    aux_weight2 = aux_weight + item_list[j].weight
                    aux_value2 = aux_value + item_list[j].value
                else:
                    aux_weight2 = aux_weight - item_list[j].weight
                    aux_value2 = aux_value - item_list[j].value

                print(f"{aux_value} {aux_weight}")
                
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
        
        print(f"D = 2 iterations {COUNTER}")

        return False

    return False

def evaluate_neighborhood2(solution: Solution, item_list: list, distance: int, mask_list1, value_list1, weight_list1) -> bool:
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

def run_local_search(solution: Solution, item_list: list, distance: int, output_filename: str):
    print(f"ic| run_local_search: Executing Local Search with distance {distance}")
    counter = 0
    output_file = FileWriter(file_name=output_filename)

    output_file.write_line(output_filename.replace('TEMP-', ''))
    output_file.write_line(str(solution.optimum))
    output_file.write_line(f"{counter} {solution.value}")
    
    while evaluate_neighborhood(solution, item_list, distance):
        counter += 1
        solution.print_solution()
        ic(f"{counter} {solution.value}")
        output_file.write_line(f"{counter} {solution.value}")

def run_local_search2(solution: Solution, item_list: list, distance: int, output_filename: str, counter: int = None):
    mask_list = get_mask_list(solution.n, distance, climb=True)
    (value_list, weight_list) = parse_item_list_data(item_list)
    while evaluate_neighborhood2(solution, item_list, distance, mask_list, value_list, weight_list):
         pass