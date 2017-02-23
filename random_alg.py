import inputreader
import outputwriter
import score_calc
import random
import sys

if __name__ == "__main__":
    videos, endpoints, cservers, requests = inputreader.read_file(sys.argv[1])
    rlim = float(sys.argv[2])
    for cs in cservers.values():
        for v in videos:
            if random.random() < rlim and cs.has_room_for(v):
                cs.add_video(v)
    print("score: {}".format(score_calc.calculate_score(videos, endpoints, cservers, requests)))
    outputwriter.write_output(cservers)
