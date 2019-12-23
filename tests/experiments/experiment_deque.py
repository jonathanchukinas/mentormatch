import collections
import random


zeroes = [0]*10
d = collections.deque(zeroes)
removed_nums = []


class MyClass:

    def __init__(self):
        self._list = list(range(5))

    def nextnum(self):
        if len(self._list) > 0:
            _nextnum = self._list.pop()
            print(_nextnum)
            yield _nextnum
        else:
            return
        # yield 1
        # yield 2
        # yield 3


myobj = MyClass()
for num in myobj.nextnum():
    print(num)

# def randomly_process(number):
#     add_back_to_deque = random.choice((True, True, True, False))
#     if add_back_to_deque:
#         d.append(number + 1)
#     else:
#         removed_nums.append(number)
#
#
# while d:
#     next_num = d.popleft()
#     randomly_process(next_num)
# print(removed_nums)
