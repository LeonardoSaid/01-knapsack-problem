import os, sys
import multiprocessing as mp

processes = (sys.argv[1], sys.argv[2], sys.argv[3])

def run_graph(filename: str):
    os.system(f"py grafico.py {filename}")

if __name__ == '__main__':
    pool = mp.Pool(processes=3)
    pool.map(run_graph, processes)