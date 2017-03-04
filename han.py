
# coding: utf-8

import numpy as np
from collections import defaultdict, namedtuple
from tqdm import tqdm
from heap import build_heap


def split2int(s):
    return list(map(int, s.split()))



Req = namedtuple('Request', ['v', 'e', 'n'])


# data = 'me_at_the_zoo.in'
# data = 'trending_today.in'
data = 'videos_worth_spreading.in'
# data = 'kittens.in'

outpath = 'outputs/{}.out'.format(data.split('.')[0])
reqs = {}
latency = {}
v2reqs = defaultdict(list)
c2ends = defaultdict(set)

CENTER = -1
with open('data/{}'.format(data), 'r') as f:
    V, E, R, C, X = split2int(f.readline())
    v2size = {i: int(size)
              for i, size in enumerate(f.readline().strip().split())}
    for endpoint_i in range(E):
        latency2center, n_caches = split2int(f.readline())
        latency[(endpoint_i, CENTER)] = latency2center
        # g.add_edge(end(endpoint_i), CENTER, d=latency2center)
        for _ in range(n_caches):
            cache_i, l = split2int(f.readline())
            latency[(endpoint_i, cache_i)] = l
            c2ends[cache_i].add(endpoint_i)
        endpoint_i += 1
        
    for l in f:
        vid, eid, n = split2int(l)
        v2reqs[vid].append(Req(vid, eid, n))
        

vc2reqs = {}  # video, cache to list of requests
for v, reqs in tqdm(v2reqs.items()):
    for c in range(C):
        vc2reqs[(v, c)] = set([r for r in reqs if r.e in c2ends[c]])


cv_pairs = []
imps = []

for c in tqdm(range(C)):
    for v in range(V):
        if (v, c) in vc2reqs:
            cv_pairs.append((c, v))
            imps.append(sum(r.n * (latency[(r.e, CENTER)] - latency[(r.e, c)])
                            for r in vc2reqs[(v, c)]))  #  / v2size[v]

cv_heap = build_heap(imps, cv_pairs)

@profile
def main(vc2reqs, v2size, latency, cv_heap, debug=False):

    caps = {i: X for i in range(C)}
    c2v = defaultdict(set)
    req2c = {}  # which cache serves *the* request
    
    while True:
        if cv_heap.size % 100 == 0:
            print(cv_heap.size)
            print('caps remaining: {}'.format(sum(caps.values()) / (X * C)))
        success = False
        while cv_heap.size > 0:
            imp, (cb, vb) = cv_heap.pop_max()
            if imp > 0 and caps[cb] >= v2size[vb]:

                if debug:
                    print('putting video {} (size {}) into cache {}'.format(vb, v2size[vb], cb))

                caps[cb] -= v2size[vb]

                if debug:
                    print('remaining capacity of cache {}: {}'.format(cb, caps[cb]))

                c2v[cb].add(vb)
                success = True
                break

        if not success:
            # not enough capacity, we are done
            break

        # the video vb being put into cache cb
        # will make some change to req2c
        for r in v2reqs[vb]:
            if r.e in c2ends[cb]:  # cb can serve r
                if r in req2c:
                    if latency[(r.e, req2c[r])] > latency[(r.e, cb)]:
                        req2c[r] = cb
                else:
                    req2c[r] = cb
                # caches that can serve r should update the score
                
                
        # update the I matrix
        for c in range(C):
            if (c, vb) in cv_heap.e2i and (vb, c) in vc2reqs:
                improvement = 0
                for r in vc2reqs[(vb, c)]:
                    # cb serve r and r is served by some c
                    if r in req2c and r.e in c2ends[cb]:
                        if latency[(r.e, req2c[r])] > latency[(r.e, c)]:
                            improvement += r.n * (latency[(r.e, req2c[r])] - latency[(r.e, c)])
                    else:
                        improvement += r.n * (latency[(r.e, CENTER)] - latency[(r.e, c)])
                cv_heap.update_key((c, vb), improvement)  #  / v2size[vb]

    if debug:
        print('remaining caps: {}'.format(caps))
    return c2v

c2v = main(vc2reqs, v2size, latency, cv_heap, debug=False)

with open(outpath, 'w') as f:
    f.write('{}\n'.format(len(c2v)))
    for c, videos in c2v.items():
        f.write('{} {}\n'.format(c, ' '.join(map(str, videos))))


