import math
from copy import copy


def build_heap(keys, es=None):
    if es is None:
        es = copy(keys)
    hp = heap(keys, es)
    for i in range(int(math.ceil(hp.size/2)), -1, -1):
        hp.max_heapify(i)

    return hp


class heap():
    def __init__(self, keys, es):
        self.size = len(keys)
        self.keys = keys
        self.es = es
        self.e2i = {e: i for i, e in enumerate(es)}

    def li(self, i):
        return 2*i

    def ri(self, i):
        return 2*i+1
    
    def parent(self, i):
        return int(i/2)

    def peep_max(self):
        return self.keys[0], self.es[0]
    
    def max_heapify(self, i):
        val = self.keys[i]
        largest = i
        li, ri = self.li(i), self.ri(i)
        if li < self.size and self.keys[li] > val:
            largest = li
        if ri < self.size and self.keys[ri] > self.keys[largest]:
            largest = ri
            
        if largest != i:
            self.e2i[self.es[largest]], self.e2i[self.es[i]] = i, largest
            self.keys[i], self.keys[largest] = self.keys[largest], self.keys[i]
            self.es[i], self.es[largest] = self.es[largest], self.es[i]
            self.max_heapify(largest)

    def pop_max(self):
        largest = self.keys[0]
        largest_e = self.es[0]
        del self.e2i[largest_e]
        
        self.keys[0] = self.keys[self.size-1]
        self.es[0] = self.es[self.size-1]
        self.size -= 1
        
        self.keys.pop()
        self.es.pop()

        if self.size > 0:
            self.max_heapify(0)

        return largest, largest_e

    def move_up(self, i):
        while True:
            p = self.parent(i)
            if self.keys[i] > self.keys[p]:
                self.e2i[self.es[i]], self.e2i[self.es[p]] = p, i
                self.keys[i], self.keys[p] = self.keys[p], self.keys[i]
                self.es[i], self.es[p] = self.es[p], self.es[i]
                i = p
            else:
                break
        
    def insert(self, key, e):
        self.size += 1
        self.keys.append(key)
        self.es.append(e)
        i = self.size - 1
        self.e2i[e] = i
        self.move_up(i)
        
    def increase_key(self, e, k):
        i = self.e2i[e]
        self.keys[i] = k
        self.move_up(i)

    def decrease_key(self, e, k):
        i = self.e2i[e]
        self.keys[i] = k
        self.max_heapify(i)

    def update_key(self, e, k):
        i = self.e2i[e]
        old_k = self.keys[i]
        if old_k < k:
            self.increase_key(e, k)
        elif old_k > k:
            self.decrease_key(e, k)
