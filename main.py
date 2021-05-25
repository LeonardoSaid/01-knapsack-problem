import time
import json
from multiprocessing import Process
from copy import deepcopy
from math import exp
from random import random

import settings
from models.solution import Solution
from file_reader import FileReader
from file_writer import FileWriter

from methods.local_search import LocalSearch
from methods.multi_start_local_search import MultiStartLocalSearch
from methods.iterated_local_search import IteratedLocalSearch
from methods.vns import Vns
from methods.tabu_search import TabuSearch
from methods.simulated_annealing import SimulatedAnnealing

VALID_INSTANCE_OPTIONS = ["1", "2"]
INSTANCE_OPTIONS_FOLDER_NAMES = {
    "1": "instances_01_KP/large_scale",
    "2": "instances_01_KP/low-dimensional"
}
INSTANCE_OPTIONS_SOLUTION_FOLDER_NAMES = {
    "1": "instances_01_KP/large_scale-optimum",
    "2": "instances_01_KP/low-dimensional-optimum"
}

# Random seed for initial solution
RANDOM_SEED = 1234


def validate_instance_option(option: str, options: list):
    try:
        return bool(options[int(option)])
    except:
        return False

def single_start_local_search(optimum_value: float, instance_dict: dict, output_filename: str) -> Solution:
    solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    solution.generate_starter_solution(
        item_list=instance_dict.get('item_list'),
        random_seed=RANDOM_SEED
    )
    #solution.print_solution()

    local_search = LocalSearch(
        solution=solution,
        item_list=instance_dict.get('item_list'),
        distance=2,
        output_filename=output_filename,
        improved=True
    )
    local_search.run()

    print(f"ic| SSL Optimum Solution")
    solution.print_solution(item_list=instance_dict.get('item_list'))
    return solution

def multi_start_local_search(optimum_value: float, instance_dict: dict, output_filename: str) -> Solution:
    config = settings.EVALUATE_METHODS_SETTINGS
    max_iterations = config.get('msl', {}).get('max_iterations')
    
    best_solution = None
    counter = 0
    msl = None

    for i in range(max_iterations):
        random_solution = Solution(
            n=instance_dict.get('n'),
            capacity=instance_dict.get('capacity'),
            optimum=optimum_value
        )
        random_solution.generate_starter_solution(
            item_list=instance_dict.get('item_list'),
            random_seed=(RANDOM_SEED+i)
        )
        #random_solution.print_solution()

        if i == 0:
            msl = MultiStartLocalSearch(
                solution=random_solution,
                item_list=instance_dict.get('item_list'),
                distance=2,
                output_filename=f"{output_filename}_temp"
            )
        else:
            msl.solution = deepcopy(random_solution)

        msl.run(counter=counter)

        if best_solution is None or msl.solution.value > best_solution.value:
            counter += 1
            msl.output_file.write_line(f"{counter} {msl.solution.value}")
            best_solution = deepcopy(msl.solution)

    print(f"ic| MSL Optimum Solution")
    best_solution.print_solution(item_list=instance_dict.get('item_list'))
    return best_solution

def iterated_local_search(optimum_value: float, instance_dict: dict, output_filename: str) -> Solution:
    config = settings.EVALUATE_METHODS_SETTINGS
    max_iterations = config.get('ils', {}).get('max_iterations')
    
    best_solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    best_solution.generate_starter_solution(
        item_list=instance_dict.get('item_list'),
        random_seed=RANDOM_SEED
    )

    counter = 0

    for i in range(max_iterations):
        perturbed_solution = deepcopy(best_solution)
        perturbed_solution.perturb_solution(item_list=instance_dict.get('item_list'))

        if i == 0:
            ils = IteratedLocalSearch(
                solution=perturbed_solution,
                item_list=instance_dict.get('item_list'),
                distance=2,
                output_filename=f"{output_filename}_temp"
            )
        else:
            ils.solution = deepcopy(perturbed_solution)

        ils.run(counter)

        while not ils.check_acceptance_criteria(best_solution):
            ils.solution.perturb_solution(item_list=instance_dict.get('item_list'))
            ils.run(counter)

        if ils.solution.value > best_solution.value:
            counter += 1
            best_solution = deepcopy(ils.solution)
            best_solution.print_solution()
            ils.output_file.write_line(f"{counter} {ils.solution.value}")

    print(f"ic| ILS Optimum Solution")
    best_solution.print_solution(item_list=instance_dict.get('item_list'))
    return best_solution

def vns(optimum_value: float, instance_dict: dict, output_filename: str) -> Solution:
    config = settings.EVALUATE_METHODS_SETTINGS
    max_iterations = config.get('vns', {}).get('max_iterations')
    neighborhood_size = config.get('vns', {}).get('neighborhood_size')
    
    solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    solution.generate_starter_solution(
        item_list=instance_dict.get('item_list'),
        random_seed=RANDOM_SEED
    )
    #solution.print_solution()

    vns_method = Vns(
        item_list=instance_dict.get('item_list'),
        neighborhood_size=neighborhood_size
    )
    
    vns_method.run_vns(
        solution=solution,
        item_list=instance_dict.get('item_list'),
        max_iterations=max_iterations,
        neighborhood_size=neighborhood_size,
        output_filename=output_filename
    )
    print(f"ic| VNS Optimum Solution")
    solution.print_solution(item_list=instance_dict.get('item_list'))
    return solution

def tabu_search(optimum_value: float, instance_dict: dict, output_filename: str):
    config = settings.EVALUATE_METHODS_SETTINGS
    max_iterations = config.get('tabu', {}).get('max_iterations')
    
    best_solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    best_solution.generate_starter_solution(
        item_list=instance_dict.get('item_list'),
        random_seed=RANDOM_SEED
    )
    best_solution.print_solution()

    tabu_list = {}
    tabu_tenure = config.get('tabu', {}).get('tenure')

    tabu_search = TabuSearch(
        solution=deepcopy(best_solution),
        item_list=instance_dict.get('item_list'),
        distance=2,
        output_filename=f"{output_filename}_temp"
    )

    for _ in range(max_iterations):
        tabu_search.run(tabu_list=tabu_list)
        if tabu_search.solution.value > best_solution.value:
            best_solution = deepcopy(tabu_search.solution)

        # decrement tenure, removes if 0
        for solution in tabu_list.copy():
            tabu_list[solution] -= 1
            if tabu_list[solution] == 0:
                del tabu_list[solution]

        # add new solution to list
        number = int(''.join([str(x) for x in tabu_search.solution.item_list]), 2)
        tabu_list[number] = tabu_tenure

    print(f"ic| Tabu Optimum Solution")
    best_solution.print_solution(item_list=instance_dict.get('item_list'))
    return best_solution

def simulated_annealing(optimum_value: float, instance_dict: dict, output_filename: str):
    config = settings.EVALUATE_METHODS_SETTINGS
    max_iterations = config.get('sa', {}).get('max_iterations')
    distance = config.get('sa', {}).get('distance')
    initial_temperature = config.get('sa', {}).get('initial_temperature')
    
    best_solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    best_solution.generate_starter_solution(
        item_list=instance_dict.get('item_list'),
        random_seed=RANDOM_SEED
    )
    best_solution.print_solution()

    sa = SimulatedAnnealing(
        solution=deepcopy(best_solution),
        item_list=instance_dict.get('item_list'),
        distance=2,
        output_filename=f"{output_filename}_temp"
    )

    current_solution = deepcopy(sa.solution)
    writer = FileWriter(file_name=f"{output_filename}_temp")

    for i in range(max_iterations):

        if i == 0:
            writer.write_line(output_filename.replace('TEMP-', ''))
            writer.write_line(str(current_solution.optimum))
            writer.write_line(f"{i} {current_solution.value}")

        sa.solution = deepcopy(current_solution)

        # random neighbor
        test = sa.random_neighbor(distance=distance)

        if not test:
            print(f"ERROR ! Could not find a random neighbor")

        # if better set as best_solution
        if sa.solution.value > best_solution.value:
            best_solution = deepcopy(sa.solution)
            writer.write_line(f"{i} {best_solution.value}")
        # calculate diff
        diff = current_solution.value - sa.solution.value
        # calculate temp
        t = initial_temperature / float(i + 1)
        if diff < 0 or random() < exp(-diff / t):
            current_solution = deepcopy(sa.solution)

    print(f"ic| SA Optimum Solution")
    best_solution.print_solution(item_list=instance_dict.get('item_list'))
    return best_solution

def evaluate_method(**kwargs):
    start = time.time()
    solution: Solution = kwargs['method_function'](
        optimum_value=kwargs['optimum_value'],
        instance_dict=kwargs['instance_dict'],
        output_filename=kwargs['output_filename']
    )
    end = time.time()
    
    solution_dict = solution.to_dict()
    accuracy = (solution_dict.get('value') / kwargs['optimum_value']) * 100
    is_valid_str = "VALID" if solution.is_valid(item_list=kwargs.get('instance_dict', {}).get('item_list')) else "INVALID"
    
    config = kwargs.get('config')
    del config['enable']

    result_file = FileWriter(file_name="evaluation_result", mode="append")
    result_file.write_line(f"----------------------------------------------------------------------------------------------------------")
    result_file.write_line(f"| Method: {kwargs['output_filename']}")
    for parameter in config:
        result_file.write_line(f"| {parameter}: {config[parameter]}")    
    result_file.write_line(f"| {json.dumps(solution_dict)}")
    result_file.write_line(f"| {is_valid_str} SOLUTION |  Execution time: {end - start}  |  Accuracy: {accuracy}")
    result_file.write_line(f"----------------------------------------------------------------------------------------------------------")
    result_file.close_file()

def evaluate_methods(optimum_value: float, instance_dict: dict, output_filename: str):
    process_list = []
    config = settings.EVALUATE_METHODS_SETTINGS
    
    if config.get('ssl', {}).get('enable'):
        ssl_process = Process(
            target=evaluate_method,
            kwargs=dict(
                method_function=single_start_local_search,
                optimum_value=optimum_value,
                instance_dict=instance_dict,
                output_filename=f"output/ssl_{output_filename}",
                config=config.get('ssl', {})
            )
        )
        process_list.append(ssl_process)
        ssl_process.start()

    if config.get('msl', {}).get('enable'):
        msl_process = Process(
            target=evaluate_method,
            kwargs=dict(
                method_function=multi_start_local_search,
                optimum_value=optimum_value,
                instance_dict=instance_dict,
                output_filename=f"output/msl_{output_filename}",
                config=config.get('msl', {})
            )
        )
        process_list.append(msl_process)
        msl_process.start()

    if config.get('ils', {}).get('enable'):
        ils_process = Process(
            target=evaluate_method,
            kwargs=dict(
                method_function=iterated_local_search,
                optimum_value=optimum_value,
                instance_dict=instance_dict,
                output_filename=f"output/ils_{output_filename}",
                config=config.get('ils', {})
            )
        )
        process_list.append(ils_process)
        ils_process.start()

    if config.get('vns', {}).get('enable'):
        vns_process = Process(
            target=evaluate_method,
            kwargs=dict(
                method_function=vns,
                optimum_value=optimum_value,
                instance_dict=instance_dict,
                output_filename=f"output/vns_{output_filename}",
                config=config.get('vns', {})
            )
        )
        process_list.append(vns_process)
        vns_process.start()

    if config.get('tabu', {}).get('enable'):
        tabu_process = Process(
            target=evaluate_method,
            kwargs=dict(
                method_function=tabu_search,
                optimum_value=optimum_value,
                instance_dict=instance_dict,
                output_filename=f"output/tabu_{output_filename}",
                config=config.get('tabu', {})
            )
        )
        process_list.append(tabu_process)
        tabu_process.start()

    if config.get('sa', {}).get('enable'):
        sa_process = Process(
            target=evaluate_method,
            kwargs=dict(
                method_function=simulated_annealing,
                optimum_value=optimum_value,
                instance_dict=instance_dict,
                output_filename=f"output/sa{output_filename}",
                config=config.get('sa', {})
            )
        )
        process_list.append(sa_process)
        sa_process.start()

    for process in process_list:
        process.join()

def main():
    print("Selecione o tipo de instância:")
    print("1 - Large Scale")
    print("2 - Low Dimensional")
    instance_type_option = input()

    while (instance_type_option not in VALID_INSTANCE_OPTIONS):
        print("Opção inválida, digite outra")
        instance_type_option = input()

    file_names = FileReader.get_file_names(path=INSTANCE_OPTIONS_FOLDER_NAMES.get(instance_type_option))

    for file_name in file_names:
            print(f"{file_names.index(file_name)} - {file_name}")

    print("Selecione uma instância:")

    instance_option = input()
    while not validate_instance_option(instance_option, file_names):
        print("Opção inválida, digite outra")
        instance_option = input()

    instance_reader = FileReader(
        path=INSTANCE_OPTIONS_FOLDER_NAMES.get(instance_type_option),
        file_name=file_names[int(instance_option)]
    )
    solution_reader = FileReader(
        path=INSTANCE_OPTIONS_SOLUTION_FOLDER_NAMES.get(instance_type_option),
        file_name=file_names[int(instance_option)]
    )

    optimum_value = solution_reader.parse_solution_data()
    instance_dict = instance_reader.parse_instance_data()
    evaluate_methods(optimum_value, instance_dict, f"{file_names[int(instance_option)]}")

if __name__ == "__main__":
    main()