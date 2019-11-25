from collections import deque

mylist = [3, 1, 2]
sorted_list = sorted(mylist)
mydeque = deque(sorted_list)
for val in mydeque:
    print(val)