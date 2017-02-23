import inputreader
import outputwriter
import score_calc
import random
import sys


class Servings(object):
    def __init__(self):
        self.y = set()
    def serve(self, video, endpoint, cache):
        self.y.add((video, endpoint, cache))
    def has(self, video, endpoint, cache):
        return (video, endpoint, cache) in self.y

def update_servings(videos, endpoints, cservers, requests):
    S = Servings()
    for r in requests:
        max_csid = None
        max_val = -1e6
        for csid, cache in r.endpoint.cache_servers.iteritems():
            val = r.count * cache.has_video(r.video) * (r.endpoint.master_latency - r.endpoint.cs_latencies[csid])
            if val > max_val:
                max_val = val
                max_csid = csid
        S.serve(r.video.vid, r.endpoint.eid, max_csid)
    return S


def update_caches(videos, endpoints, cservers, requests, servings):
    values = {}
    video_map = {}
    for r in requests:
        video_map[r.video.vid] = r.video
        for csid, cache in r.endpoint.cache_servers.iteritems():
            key = (r.video.vid, csid)
            values[key] = values.get(key, 0) + r.count * servings.has(r.video.vid, r.endpoint.eid, cache.csid) * (r.endpoint.master_latency - r.endpoint.cs_latencies[csid])
    tups = []
    for key, val in values.iteritems():
        tups.append((val / float(video_map[key[0]].size), key))
    tups.sort(reverse=True)

    # Empty cache servers
    for c in cservers.itervalues():
        c.clear()

    for _, (vid, csid) in tups:
        v = video_map[vid]
        if cservers[csid].has_room_for(v):
            cservers[csid].add_video(v)

def solve(videos, endpoints, cservers, requests, do_print):
    # Init solution
    rlim = float(sys.argv[2])
    for cs in cservers.values():
        for v in videos:
            if random.random() < rlim and cs.has_room_for(v):
                cs.add_video(v)
    if do_print:
        print("Initial score: {}".format(score_calc.calculate_score(videos, endpoints, cservers, requests)))

    n_iter = 5
    for i in range(n_iter):
        S = update_servings(videos, endpoints, cservers, requests)
        #inputreader.debug_output(videos, endpoints, cservers, requests)
        update_caches(videos, endpoints, cservers, requests, S)
        if do_print:
            print("score: {}".format(score_calc.calculate_score(videos, endpoints, cservers, requests)))
        #inputreader.debug_output(videos, endpoints, cservers, requests)

if __name__ == "__main__":
    videos, endpoints, cservers, requests = inputreader.read_file(sys.argv[1])
    if len(sys.argv) > 3:
        do_print = True
    else:
        do_print = False
    solve(videos, endpoints, cservers, requests, do_print)
    outputwriter.write_output(cservers)
