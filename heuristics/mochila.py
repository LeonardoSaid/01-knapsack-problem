import time
import json
from multiprocessing import Process
from copy import deepcopy
from icecream import ic

from models.item import Item
from models.solution import Solution
from file_reader import FileReader
from file_writer import FileWriter
from methods.local_search import run_local_search, run_local_search2
from methods.vns import VNS


VALID_INSTANCE_OPTIONS = ["1", "2"]
INSTANCE_OPTIONS_FOLDER_NAMES = {
    "1": "instances_01_KP/large_scale",
    "2": "instances_01_KP/low-dimensional"
}
INSTANCE_OPTIONS_SOLUTION_FOLDER_NAMES = {
    "1": "instances_01_KP/large_scale-optimum",
    "2": "instances_01_KP/low-dimensional-optimum"
}

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
        random_seed=10
    )
    solution.print_solution()
    run_local_search(
        solution=solution,
        item_list=instance_dict.get('item_list'),
        distance=2,
        output_filename=output_filename
    )
    print(f"ic| Optimum Solution")
    solution.print_solution(item_list=instance_dict.get('item_list'))
    return solution

def multi_start_local_search(optimum_value: float, instance_dict: dict, max_iterations: int, output_filename: str) -> Solution:
    best_solution = None
    output_file = FileWriter(file_name=f"{output_filename}_temp")
    output_file.write_line(output_filename.replace('TEMP-', ''))
    output_file.write_line(str(optimum_value))
    counter = 0
    for i in range(max_iterations):
        random_solution = Solution(
            n=instance_dict.get('n'),
            capacity=instance_dict.get('capacity'),
            optimum=optimum_value
        )
        random_solution.generate_starter_solution(
            item_list=instance_dict.get('item_list'),
            random_seed=(10+i)
        )
        random_solution.print_solution()

        if counter == 0:
            ic(f"{counter} {random_solution.value}")
            output_file.write_line(f"{counter} {random_solution.value}")
            counter += 1

        run_local_search2(
            solution=random_solution,
            item_list=instance_dict.get('item_list'),
            distance=2,
            output_filename=f"{output_filename}_temp"
        )

        if not best_solution or random_solution.value > best_solution.value:
            best_solution = deepcopy(random_solution)
        
        ic(f"{counter} {best_solution.value}")
        output_file.write_line(f"{counter} {best_solution.value}")
        counter += 1

    output_file.close_file()
    FileWriter.rewrite_file(
        file_to_read=f"{output_filename}_temp_output.txt",
        file_to_write=f"{output_filename}_output.txt"
    )
    print(f"ic| Optimum Solution")
    best_solution.print_solution(item_list=instance_dict.get('item_list'))
    return best_solution

def iterated_local_search(optimum_value: float, instance_dict: dict, max_iterations: int, output_filename: str) -> Solution:

    def check_acceptance_criteria(best_solution: Solution, candidate_solution: Solution) -> bool:
        """
            Aceite soluções melhores ou que sejam no máximo 10% pior da melhor solução atual.
        """
        if candidate_solution.value > best_solution.value or \
                abs(1 - (candidate_solution.value / best_solution.value)) <= 0.1:
            return True
        return False
    
    best_solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    best_solution.generate_starter_solution(
        item_list=instance_dict.get('item_list'),
        random_seed=10
    )
    print(f"ic| Initial Optimum Solution (randomized)")
    best_solution.print_solution()

    # gravar a sol 0
    output_file = FileWriter(file_name=f"{output_filename}_temp")
    output_file.write_line(output_filename.replace('TEMP-', ''))
    output_file.write_line(str(best_solution.optimum))
    output_file.write_line(f"{0} {best_solution.value}")

    counter = 1

    for i in range(max_iterations):
        perturbed_solution = deepcopy(best_solution)
        perturbed_solution.perturb_solution(item_list=instance_dict.get('item_list'))
        run_local_search2(
            solution=perturbed_solution,
            item_list=instance_dict.get('item_list'),
            distance=2,
            output_filename=f"{output_filename}_temp"
        )

        while not check_acceptance_criteria(best_solution, perturbed_solution):
            perturbed_solution.perturb_solution(item_list=instance_dict.get('item_list'))
            run_local_search2(
                solution=perturbed_solution,
                item_list=instance_dict.get('item_list'),
                distance=2,
                output_filename=f"{output_filename}_temp"
            )

        if perturbed_solution.value > best_solution.value:
            best_solution = deepcopy(perturbed_solution)
            best_solution.print_solution()
        
        ic(f"{counter} {best_solution.value}")
        output_file.write_line(f"{counter} {best_solution.value}")
        counter += 1

    output_file.close_file()
    FileWriter.rewrite_file(
        file_to_read=f"{output_filename}_temp_output.txt",
        file_to_write=f"{output_filename}_output.txt"
    )

    print(f"ic| Optimum Solution")
    best_solution.print_solution(item_list=instance_dict.get('item_list'))
    return best_solution

def vns(optimum_value: float, instance_dict: dict, max_iterations: int, neighborhood_size: int, output_filename: str) -> Solution:
    solution = Solution(
        n=instance_dict.get('n'),
        capacity=instance_dict.get('capacity'),
        optimum=optimum_value
    )
    solution.generate_starter_solution(
        item_list=instance_dict.get('item_list')
    )
    solution.print_solution()

    vns_method = VNS(neighborhood_size)
    vns_method.run_vns(
        solution=solution,
        item_list=instance_dict.get('item_list'),
        max_iterations=max_iterations,
        neighborhood_size=neighborhood_size,
        output_filename=output_filename
    )
    print(f"ic| Optimum Solution")
    solution.print_solution(item_list=instance_dict.get('item_list'))
    return solution

def evaluate_method(**kwargs):
    start = time.time()
    if not kwargs.get('max_iterations'):
        solution: Solution = kwargs['method_function'](
            optimum_value=kwargs['optimum_value'],
            instance_dict=kwargs['instance_dict'],
            output_filename=kwargs['output_filename']
        )
    elif not kwargs.get('neighborhood_size'):
        solution: Solution = kwargs['method_function'](
            optimum_value=kwargs['optimum_value'],
            instance_dict=kwargs['instance_dict'],
            output_filename=kwargs['output_filename'],
            max_iterations=kwargs['max_iterations']
        )
    else:
        solution: Solution = kwargs['method_function'](
            optimum_value=kwargs['optimum_value'],
            instance_dict=kwargs['instance_dict'],
            output_filename=kwargs['output_filename'],
            max_iterations=kwargs['max_iterations'],
            neighborhood_size=kwargs['neighborhood_size'],
        )
    end = time.time()
    
    solution_dict = solution.to_dict()
    accuracy = (solution_dict.get('value') / kwargs['optimum_value']) * 100
    is_valid_str = "VALID" if solution.is_valid(item_list=kwargs.get('instance_dict', {}).get('item_list')) else "INVALID"

    result_file = FileWriter(file_name="evaluation_result", mode="append")
    result_file.write_line(f"ic | Method: {kwargs['output_filename']}")
    if kwargs.get('max_iterations'):
        result_file.write_line(f"ic | Number of iterations: {kwargs['max_iterations']}")
    if kwargs.get('neighborhood_size'):
        result_file.write_line(f"ic | Neighborhood size: {kwargs['neighborhood_size']}")
    result_file.write_line(json.dumps(solution_dict))
    result_file.write_line(f"ic | {is_valid_str} SOLUTION |  Execution time: {end - start}  |  Accuracy: {accuracy} \n")
    result_file.close_file()

def evaluate_methods(optimum_value: float, instance_dict: dict, max_iterations: int, neighborhood_size: int, output_filename: str):    
    process_list = []
    ssl_process = Process(
        target=evaluate_method,
        kwargs=dict(
            method_function=single_start_local_search,
            optimum_value=optimum_value,
            instance_dict=instance_dict,
            output_filename=f"output/ssl_{output_filename}",
        )
    )
    process_list.append(ssl_process)
    ssl_process.start()

    msl_process = Process(
        target=evaluate_method,
        kwargs=dict(
            method_function=multi_start_local_search,
            optimum_value=optimum_value,
            instance_dict=instance_dict,
            output_filename=f"output/msl_{output_filename}",
            max_iterations=max_iterations
        )
    )
    process_list.append(msl_process)
    msl_process.start()

    ils_process = Process(
        target=evaluate_method,
        kwargs=dict(
            method_function=iterated_local_search,
            optimum_value=optimum_value,
            instance_dict=instance_dict,
            output_filename=f"output/ils_{output_filename}",
            max_iterations=max_iterations
        )
    )
    process_list.append(ils_process)
    ils_process.start()

    # vns_process = Process(
    #     target=evaluate_method,
    #     kwargs=dict(
    #         method_function=vns,
    #         optimum_value=optimum_value,
    #         instance_dict=instance_dict,
    #         max_iterations=max_iterations,
    #         neighborhood_size=neighborhood_size,
    #         output_filename=f"output/vns_{output_filename}"
    #     )
    # )
    # process_list.append(vns_process)
    # vns_process.start()

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

    ic(instance_type_option)

    file_names = FileReader.get_file_names(path=INSTANCE_OPTIONS_FOLDER_NAMES.get(instance_type_option))

    for file_name in file_names:
            print(f"{file_names.index(file_name)} - {file_name}")

    print("Selecione uma instância:")

    instance_option = input()
    while not validate_instance_option(instance_option, file_names):
        print("Opção inválida, digite outra")
        instance_option = input()

    ic(instance_option)
    ic(file_names[int(instance_option)])

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

    evaluate_methods(optimum_value, instance_dict, 20, 3, f"{file_names[int(instance_option)]}")

if __name__ == "__main__":
    main()