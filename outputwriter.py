
def write_output(cservers):
    using = 0
    for cs in cservers.values():
        if cs.videos:
            using += 1
    print("{}".format(using))
    for cs in cservers.values():
        print(" ".join([str(cs.csid)] + [str(x.vid) for x in cs.videos]))


if __name__ == "__main__":
    import sys
    import inputreader
    videos, endpoints, cservers, requests = inputreader.read_file(sys.argv[1])
    for cs in cservers.values():
        for v in videos:
            cs.add_video(v)
    inputreader.debug_output(videos, endpoints, cservers, requests)
    write_output(cservers)
