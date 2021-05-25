from typing import List
from copy import deepcopy
import random
from icecream import ic

from models.item import Item

class Solution:
    weight = None
    value = None

    def __init__(
        self, 
        n: int,
        capacity: float,
        optimum: float
    ):
        self.n = n
        self.weight = 0
        self.value = 0
        self.capacity = capacity
        self.optimum = optimum
        self.item_list = self.generate_item_list(length=n)

    def to_dict(self):
        return dict(
            n=self.n,
            weight=self.weight,
            value=self.value,
            capacity=self.capacity,
            optimum=self.optimum
        )

    def generate_item_list(self, length: int) -> List[int]:
        return [0] * length

    def clear_solution(self):
        self.weight = 0
        self.value = 0
        self.item_list = self.generate_item_list(length=self.n)

    def is_valid(self, item_list: List[Item]) -> bool:
        """
            Verifies if all the selected items exist and the solution parameters are valid
        """
        #print(' '.join([str(item) for item in self.item_list]))
        weight = 0
        value = 0
        for i in range(self.n):
            if self.item_list[i] == 1:
                weight += item_list[i].weight
                value += item_list[i].value

        if weight != self.weight:
            print(f"ic| INVALID WEIGHT - self.weight: {self.weight} - calculated: {weight}")
            return False
        
        if value != self.value:
            print(f"ic| INVALID VALUE - self.value: {self.value} - calculated: {value}")
            return False
        
        if weight > self.capacity:
            print(f"ic| INVALID CAPACITY - self.capacity: {self.capacity} - calculated weight: {weight}")
            return False

        return True   

    def add_item(self, index: str, item: Item):
        self.item_list[index] = 1
        self.weight += item.weight
        self.value += item.value

    def remove_item(self, index: str, item: Item):
        self.item_list[index] = 0
        self.weight -= item.weight
        self.value -= item.value

    def print_solution(self, item_list: list = None):
        print(self.to_dict())
        if item_list:
            counter = 0
            for i in range(self.n):
                if self.item_list[i] == 1:
                    #ic(item_list[i].__dict__)
                    counter += 1
            #print(f"{counter} items chosen")
    
    def generate_starter_solution(self, item_list: List[Item], random_seed: int = None, clear_solution: bool = False):
        if clear_solution:
            self.clear_solution()

        if random_seed:
            random.seed(random_seed)

        counter = 0
        tracking_list = [0] * self.n
        while self.weight < self.capacity and counter < self.n:
            i = random.randint(0, 2147483647) % self.n
            while tracking_list[i] == 1:
                i = (i + 1) % self.n
            
            if self.weight + item_list[i].weight <= self.capacity:
                self.add_item(index=i, item=item_list[i])
            
            tracking_list[i] = 1
            counter += 1

    def perturb_solution(self, item_list: List[Item], random_seed: int = None):
        """
            Removes and adds {counter} items, based on a random guess between 1 and the amount of items in solution
        """
        if random_seed:
            random.seed(random_seed)

        #counter = random.randint(1, self.item_list.count(1))
        counter = random.randint(1, 1 + int(self.item_list.count(1) * 0.25))
        #print(f"ic| Removing {counter} items in the solution")
        for i in range(counter):
            index = random.randint(0, 2147483647) % self.n
            while self.item_list[index] == 0:
                index = (index + 1) % self.n
            self.remove_item(index, item_list[index])

        #print(f"ic| Attempting to add {counter} items in the solution")
        tracking_list = [0] * self.n
        j = 0
        while j < counter:
            if tracking_list.count(1) == self.n:
                #print(f"ic| Unable to add anymore items")
                return

            index = random.randint(0, 2147483647) % self.n
            while tracking_list[index] == 1:
                index = (index + 1) % self.n
            
            if self.item_list[index] == 0 and \
                    (self.weight + item_list[index].weight) <= self.capacity:
                self.add_item(index=index, item=item_list[index])
            else:
                # item either is already selected or its too heavy
                tracking_list[index] = 1
                continue

            j += 1
            tracking_list[index] = 1
 