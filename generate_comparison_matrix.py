""" 
    Generates an array to compare the results with the following setting:
         SSL MSL ILS VNS TABU SA
      SSL
      MSL
      ILS
      VNS
      TABU
      SA
    Each entry in the matrix is the number of datasets considered for which the heuristic in the row had a higher
    knapsack value returned than the heuristic in the column
"""

RESULT_LARGE = {
    "knapPI_1_100_1000_1": {
        "ssl": 8759.0,
        "msl": 9147.0,
        "ils": 9147.0,
        "vns": 2842.0,
        "tabu": 8759.0,
        "sa": 7486.0,
        "optimum": 9147.0
    },
    "knapPI_1_200_1000_1": {
        "ssl": 9245.0,
        "msl": 11013.0,
        "ils": 11238.0,
        "vns": 3941.0,
        "tabu": 9245.0,
        "sa": 9213.0,
        "optimum": 11238.0
    },
    "knapPI_1_500_1000_1": {
        "ssl": 23770.0,
        "msl": 23813.0,
        "ils": 26385.0,
        "vns": 6735.0,
        "tabu": 23770.0,
        "sa": 18496.0,
        "optimum": 28857.0
    },
    "knapPI_2_100_1000_1": {
        "ssl": 1275.0,
        "msl": 1497.0,
        "ils": 1514.0,
        "vns": 1023.0,
        "tabu": 1275.0,
        "sa": 1160.0,
        "optimum": 1514.0
    },
    "knapPI_2_200_1000_1": {
        "ssl": 1286.0,
        "msl": 1474.0,
        "ils": 1623.0,
        "vns": 756.0,
        "tabu": 1286.0,
        "sa": 1319.0,
        "optimum": 1634.0
    },
    "knapPI_2_500_1000_1": {
        "ssl": 3468.0,
        "msl": 3468.0,
        "ils": 3527.0,
        "vns": 2695.0,
        "tabu": 3468.0,
        "sa": 3139.0,
        "optimum": 4566.0
    },
    "knapPI_3_100_1000_1": {
        "ssl": 1296.0,
        "msl": 1997.0,
        "ils": 2195.0,
        "vns": 1294.0,
        "tabu": 1296.0,
        "sa": 1296.0,
        "optimum": 2397.0
    },
    "knapPI_3_200_1000_1": {
        "ssl": 1595.0,
        "msl": 1897.0,
        "ils": 2197.0,
        "vns": 1594.0,
        "tabu": 1595.0,
        "sa": 1796.0,
        "optimum": 2697.0
    },
    "knapPI_3_500_1000_1": {
        "ssl": 3217.0,
        "msl": 3517.0,
        "ils": 3417.0,
        "vns": 3215.0,
        "tabu": 3217.0,
        "sa": 3416.0,
        "optimum": 7117.0
    }
}

RESULT_LOW = {
    "f10_l-d_kp_20_879": {
        "ssl": 1025.0,
        "msl": 1025.0,
        "ils": 1025.0,
        "vns": 884.0,
        "tabu": 1025.0,
        "sa": 1017.0,
        "optimum": 1025.0
    },
    "f1_l-d_kp_10_269": {
        "ssl": 293.0,
        "msl": 295.0,
        "ils": 293.0,
        "vns": 251.0,
        "tabu": 293.0,
        "sa": 293.0,
        "optimum": 295.0
    },
    "f2_l-d_kp_20_878": {
        "ssl": 1024.0,
        "msl": 1024.0,
        "ils": 1024.0,
        "vns": 976.0,
        "tabu": 1024.0,
        "sa": 1024.0,
        "optimum": 1024.0
    },
    "f3_l-d_kp_4_20": {
        "ssl": 28.0,
        "msl": 35.0,
        "ils": 24.0,
        "vns": 28.0,
        "tabu": 28.0,
        "sa": 28.0,
        "optimum": 35.0
    },
    "f4_l-d_kp_4_11": {
        "ssl": 23.0,
        "msl": 23.0,
        "ils": 23.0,
        "vns": 19.0,
        "tabu": 23.0,
        "sa": 23.0,
        "optimum": 23.0
    },
    "f5_l-d_kp_15_375": {
        "ssl": 437.934507,
        "msl": 481.069368,
        "ils": 481.069368,
        "vns": 302.73751,
        "tabu": 437.934507,
        "sa": 469.161046,
        "optimum": 481.0694
    },
    "f6_l-d_kp_10_60": {
        "ssl": 50.0,
        "msl": 52.0,
        "ils": 52.0,
        "vns": 45.0,
        "tabu": 50.0,
        "sa": 52.0,
        "optimum": 52.0
    },
    "f7_l-d_kp_7_50": {
        "ssl": 96.0,
        "msl": 107.0,
        "ils": 105.0,
        "vns": 96.0,
        "tabu": 96.0,
        "sa": 96.0,
        "optimum": 107.0
    },
    "f8_l-d_kp_23_10000": {
        "ssl": 9762.0,
        "msl": 9767.0,
        "ils": 9767.0,
        "vns": 9702.0,
        "tabu": 9762.0,
        "sa": 9762.0,
        "optimum": 9767.0
    },
    "f9_l-d_kp_5_80": {
        "ssl": 130.0,
        "msl": 130.0,
        "ils": 130.0,
        "vns": 109.0,
        "tabu": 130.0,
        "sa": 130.0,
        "optimum": 130.0
    }
}

def print_pretty(result: list):
    for line in result:
        print(f"& {' & '.join(map(str, line))} & {sum(line)}")

def main2():
    for asd in RESULT_LARGE:
        print(asd)
        #print(RESULT_LARGE[asd].get('optimum'))
        #print(f"{RESULT_LARGE[asd].get('ssl')} {RESULT_LARGE[asd].get('msl')} {RESULT_LARGE[asd].get('ils')} {RESULT_LARGE[asd].get('vns')} {RESULT_LARGE[asd].get('tabu')} {RESULT_LARGE[asd].get('sa')}")

def main():
    index_order = ["ssl", "msl", "ils", "vns", "tabu", "sa"]
    result_matrix_low = [ [] for _ in range(6) ]
    result_matrix_large = [ [] for _ in range(6) ]
    
    for x in range(6):
        for y in range(6):
            value = 0
            if x == y:
                result_matrix_low[x].append(value)
                continue
            for instance in RESULT_LOW:
                if RESULT_LOW[instance][index_order[x]] > RESULT_LOW[instance][index_order[y]]:
                    value += 1
            result_matrix_low[x].append(value)
    
    print_pretty(result_matrix_low)

    print(f"------------------------")

    for x in range(6):
        for y in range(6):
            value = 0
            if x == y:
                result_matrix_large[x].append(value)
                continue
            for instance in RESULT_LARGE:
                if RESULT_LARGE[instance][index_order[x]] > RESULT_LARGE[instance][index_order[y]]:
                    value += 1
            result_matrix_large[x].append(value)
    
    print_pretty(result_matrix_large)

if __name__ == "__main__":
    main()