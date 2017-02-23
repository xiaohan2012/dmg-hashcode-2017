
def calculate_score(videos, endpoints, cservers, requests):
    total_latency = 0
    total_requests = 0
    for r in requests:
        latency = r.endpoint.master_latency
        for csid, cserver in r.endpoint.cache_servers.items():
            if cserver.has_video(r.video):
                latency = min(latency, r.endpoint.cs_latencies[csid])
        total_latency += (r.endpoint.master_latency - latency) * r.count
        total_requests += r.count
    return total_latency * 1000. / total_requests


def check_validity(cservers):
    for cs in cservers.values():
        recalc_size = sum([x.size for x in cs.get_video_list()])
        if recalc_size != cs.total_size:
            raise Exception("recalc_size {} and total_size {} differ for cs {}".format(recalc_size, cs.total_size, cs.csid))
        if recalc_size > cs.capacity:
            raise Exception("sum of cached file sizes over capacity for cs {}".format(cs.csid))


if __name__ == "__main__":
    import sys
    import inputreader
    videos, endpoints, cservers, requests = inputreader.read_file(sys.argv[1])
    for cs in cservers.values():
        for v in videos:
            cs.add_video(v)
    inputreader.debug_output(videos, endpoints, cservers, requests)
    print("total score: {} microseconds".format(calculate_score(videos, endpoints, cservers, requests)))

