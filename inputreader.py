
class Video(object):
    def __init__(self, vid, size):
        self.vid = vid
        self.size = size

class Endpoint(object):
    def __init__(self, master_latency):
        self.master_latency = master_latency
        self.cache_servers = {}
    def add_cache_server(self, cache_server):
        self.cache_servers[cache_server.csid] = cache_server
        cache_server.endpoints.append(self)

class CacheServer(object):
    def __init__(self, csid):
        self.csid = csid
        self.endpoints = []

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
        for i in xrange(endpointcount):
            line = lines[line_i]
            line_i += 1
            master_latency, cservers_count = [int(x) for x in line.split()]
            endpoint = Endpoint(master_latency)
            for k in xrange(cservers_count):
                line2 = lines[line_i]
                line_i += 1
                cserver_id, latency = [int(x) for x in line.split()]
                if cserver_id not in cservers:
                    cservers[cserver_id] = CacheServer(cserver_id)
                endpoint.add_cache_server(cservers[cserver_id])
            endpoints.append(endpoint)
        for i in xrange(rdcount):
            line = lines[line_i]
            line_i += 1
            video_id, endpoint_id, request_count = [int(x) for x in line.split()]
            requests.append(Request(videos[video_id], endpoints[endpoint_id], request_count))
        return videos, endpoints, cservers, requests

if __name__ == "__main__":
    import sys
    videos, endpoints, cservers, requests = read_file(sys.argv[1])
    print(videos)
    print(endpoints)
    print(cservers)
    print(requests)
    
