import collections
import random


zeroes = [0]*10
d = collections.deque(zeroes)
removed_nums = []


def randomly_process(number):
    add_back_to_deque = random.choice((True, True, True, False))
    if add_back_to_deque:
        d.append(number + 1)
    else:
        removed_nums.append(number)


while d:
    next_num = d.popleft()
    randomly_process(next_num)
print(removed_nums)
