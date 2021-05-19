import sys
import traceback
from matplotlib import pyplot as plt

asd = [
    ".\ssl_f10_l-d_kp_20_879_output.txt",
    ".\msl_f10_l-d_kp_20_879_output.txt",
    ".\ils_f10_l-d_kp_20_879_output.txt"
]

# key / length
longest = (1, 0)

def parse_name(name: str):
    if "ssl" in name:
        return "Busca Local"
    if "msl" in name:
        return "Busca Local Multistart"
    if "ils" in name:
        return "Busca Local Iterada"
    if "VNS" in name:
        return "Busca Vizinhança Variável"
    return name

try:
    for i in range(1, len(sys.argv)):
        graph = sys.argv[i]
        #graph = asd[i-1]
        graph_file = open(graph, "r")
        graph_name = graph_file.readline()
        graph_optimum = graph_file.readline()
        counter_list = []
        value_list = []
        for line in graph_file:
            (counter, value) = line.split()
            counter_list.append(int(counter))
            value_list.append(float(value))
        graph_file.close()

        if len(counter_list) > longest[1]:
            longest = (i, len(counter_list))

        plt.plot(counter_list, value_list, label=parse_name(graph_name))

    print(f"LONGEST {longest}")

    graph = sys.argv[longest[0]]
    #graph = asd[0]
    graph_file = open(graph, "r")
    graph_name = graph_file.readline()
    graph_optimum = graph_file.readline()
    optimum_list = []
    counter_list = []
    for line in graph_file:
        (counter, _) = line.split()
        counter_list.append(int(counter))
        optimum_list.append(float(graph_optimum))
    graph_file.close()
    plt.plot(counter_list, optimum_list, label="Melhor Valor")

    plt.xlabel('Iteração')
    plt.ylabel('Valor')
    plt.title("Comparação Métodos")
    plt.legend()
    plt.grid()
    plt.show()
except Exception:
    traceback.print_exc()