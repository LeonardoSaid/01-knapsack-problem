"""

https://stackoverflow.com/questions/1851134/generate-all-binary-strings-of-length-n-with-k-bits-set
https://stackoverflow.com/questions/11344827/summing-elements-in-a-list

gera n combinacoes da lista original
multiplica uma lista com listade pesos elemento a elemento e faz a somatoria
filtra por capacity
multiplica mesma lista com lista de valores
acha a que tem mais


get solution
parse to binary
get kbits list with n=n and k=distance
for each kbit:
  parse to number?binary?
  do solution xor kbit
  parse result to list
  multiply with weight list
  if capacity ok save it to neighbors

return best neighbor

['1000', '0100', '0010', '0001']
['1100', '1010', '1001', '0110', '0101', '0011']
"""

import itertools

def kbits(n, k):
    result = []
    for bits in itertools.combinations(range(n), k):
        s = ['0'] * n
        for bit in bits:
            s[bit] = '1'
        result.append(''.join(s))
    return result

#item_list = [0, 1, 1, 1, 1, 1, 0, 1, 0, 0]
item_list = ([0]*22) + [1]
weight_list = [983.0, 982.0, 981.0, 980.0, 979.0, 978.0, 488.0, 976.0, 972.0, 486.0, 486.0, 972.0, 972.0, 485.0, 485.0, 969.0, 966.0, 483.0, 964.0, 963.0, 961.0, 958.0, 959.0]
value_list = [981.0, 980.0, 979.0, 978.0, 977.0, 976.0, 487.0, 974.0, 970.0, 485.0, 485.0, 970.0, 970.0, 484.0, 484.0, 976.0, 974.0, 482.0, 962.0, 961.0, 959.0, 958.0, 857.0]
item_list_binary = "".join([str(item) for item in item_list])
#print(item_list_binary)
number = int(item_list_binary, 2)
#print(number)

masked_list = []
for i in range(1, 23):
    masked_list += kbits(23, i)
#print(masked_list)

neighbors = []
capacity = 10000

for mask in masked_list:
    result = number ^ int(mask, 2)
    result2 = bin(result)[2:].zfill(23)
    #print(result)
    #print(result2)
    result3 = [int(digit) for digit in result2]
    #print(f"mascarado: {result3}")
    qq = [a * b for a,b in zip(result3, weight_list)]
    #print(qq)
    #print(sum(qq))
    if sum(qq) <= capacity:
        neighbors.append(result3)

optimum_value = 959
best_solution = 0
for neighbor in neighbors:
    result4 = [a * b for a,b in zip(neighbor, value_list)]
    if sum(result4) > optimum_value:
        optimum_value = sum(result4)
        best_solution = result4

print(best_solution)
print(optimum_value)

