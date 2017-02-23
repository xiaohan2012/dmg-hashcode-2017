import inputreader
import outputwriter
import score_calc
import random
import sys

if __name__ == "__main__":
    videos, endpoints, cservers, requests = inputreader.read_file(sys.argv[1])
    edges = {}
    videodict = {}
    for v in videos:
        videodict[v.vid] = v

    # for all cache servers
    for cs in sorted(cservers.values(), key=lambda x: len(x.endpoints), reverse=True):
        benefit = {}
        for endpoint in cs.endpoints:
            # gets latency of endpoint to cs
            latency = endpoint.cs_latencies[cs.csid]
            for req in endpoint.requests:
                mlat = endpoint.master_latency
                prev_lat = mlat
                # finds the lowest latency server that has the video
                for cs2 in endpoint.cache_servers.values():
                    if cs2.has_video(req.video):
                        prev_lat = min(prev_lat, endpoint.cs_latencies[cs.csid])
                # calculates benefit of adding the video to this server
                benefit[req.video.vid] = benefit.get(req.video.vid, 0.0) + req.count * (prev_lat - latency)
        # fills this cache server with videos with highest benefit
        for vid, value in sorted(benefit.items(), key=lambda (k,v):v, reverse=True):
            if cs.has_room_for(videodict[vid]):
                cs.add_video(videodict[vid])

    print("score: {}".format(score_calc.calculate_score(videos, endpoints, cservers, requests)))
    score_calc.check_validity(cservers)
    outputwriter.write_output(cservers)
