from builtins import range

class Video(object):
    def __init__(self, vid, size):
        self.vid = vid
        self.size = size

class Endpoint(object):
    def __init__(self, eid, master_latency):
        self.eid = eid
        self.master_latency = master_latency
        self.cache_servers = {}
        self.cs_latencies = {}
    def add_cache_server(self, cache_server, latency):
        self.cache_servers[cache_server.csid] = cache_server
        self.cs_latencies[cache_server.csid] = latency
        cache_server.endpoints.append(self)

class CacheServer(object):
    def __init__(self, csid):
        self.csid = csid
        self.endpoints = []
        self.videos = []
    def add_video(self, video):
        self.videos.append(video)
    def has_video(self, video):
        return video in self.videos

class Request(object):
    def __init__(self, video, endpoint, count):
        self.video = video
        self.endpoint = endpoint
        self.count = count

def read_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        header = lines[0]
        videocount, endpointcount, rdcount, cservercount, capacitymb = [int(x) for x in header.split()]

        videos = []
        endpoints = []
        cservers = {}
        requests = []
        for vid, size_str in enumerate(lines[1].split()):
            videos.append(Video(vid, int(size_str)))
        line_i = 2
        for eid in range(endpointcount):
            line = lines[line_i]
            line_i += 1
            master_latency, cservers_count = [int(x) for x in line.split()]
            endpoint = Endpoint(eid, master_latency)
            for k in range(cservers_count):
                line2 = lines[line_i]
                line_i += 1
                cserver_id, latency = [int(x) for x in line2.split()]
                if cserver_id not in cservers:
                    cservers[cserver_id] = CacheServer(cserver_id)
                endpoint.add_cache_server(cservers[cserver_id], latency)
            endpoints.append(endpoint)
        for i in range(rdcount):
            line = lines[line_i]
            line_i += 1
            video_id, endpoint_id, request_count = [int(x) for x in line.split()]
            requests.append(Request(videos[video_id], endpoints[endpoint_id], request_count))
        return videos, endpoints, cservers, requests


def debug_output(videos, endpoints, cservers, requests):
    for video in videos:
        print("video {}, size {}".format(video.vid, video.size))
    for endpoint in endpoints:
        print("endpoint {}, mlat {}".format(endpoint.eid, endpoint.master_latency))
        for cs in sorted(endpoint.cache_servers.values(), key=lambda x:x.csid):
            print("    cache server {}, latency {}".format(cs.csid, endpoint.cs_latencies[cs.csid]))
    for cs in sorted(cservers.values(), key=lambda x:x.csid):
        print("cache server {}".format(cs.csid))
        for endpoint in cs.endpoints:
            print("    endpoint {}, latency {}".format(endpoint.eid, endpoint.cs_latencies[cs.csid]))
        for video in cs.videos:
            print("    cached video {}".format(video.vid))
    for r in requests:
        print("request for video {}, from endpoint {}, count {}".format(r.video.vid, r.endpoint.eid, r.count))


if __name__ == "__main__":
    import sys
    videos, endpoints, cservers, requests = read_file(sys.argv[1])
    cservers.values()[0].add_video(videos[0])
    debug_output(videos, endpoints, cservers, requests)
    
