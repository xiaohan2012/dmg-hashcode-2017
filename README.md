# Greedy algorithm

1. calculates the "improvement" score for each video-cache pair (putting video v into cache c)
2. assiging video to cache greedily using the above score
3. after the assignment `(v, c)`, update the improvement score for the pairs `(v, c')`.

# Lessons

- terminate after certain iterations (or it runs forever)

# Using C

1. `latency`: 2D array
2. `vc2reqs`: hashmap