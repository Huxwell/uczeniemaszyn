import cPickle as pickle


def discr(name):
    raw=[]
    with open('../../data/interim/'+name+'.pkl', 'rb') as f:
        raw = pickle.load(f)
    for n_parts in xrange(2,20):
        max_v = []
        min_v = []
        diff_v = []
        for values in zip(*[a[0] for a in raw]):
            max_v.append(max(values))
            min_v.append(min(values))
            diff_v.append((max(values) - min(values)) / n_parts)

        buckets = []
        for ma, mi, di in zip(max_v, min_v, diff_v):
            b = []
            for i in range(1, 1 + n_parts):
                b.append((mi + i * di, i))
            buckets.append(b)
        print "buckets" + str(buckets) + "\n"
        discretized_enc = []
        discretized = []
        for pair in raw:
            new_v = []
            disc_v = []
            for value, b in zip(pair[0], buckets):
                for threshold, tier in b:
                    if threshold > value:
                        new_v.append(tier)
                        disc_v.append(threshold)
                        break
            discretized_enc.append((new_v, pair[1]))
            discretized.append((disc_v, pair[1]))

        with open('../../data/processed/'+name+'_discretized_equal_'+str(n_parts)+'.pkl', 'wb') as f:
            pickle.dump(discretized,f)

        with open('../../data/processed/'+name+'_discretized_equal_enc_'+str(n_parts)+'.pkl', 'wb') as f:
            pickle.dump(discretized_enc,f)
            print discretized_enc[3:6]
discr("pima-indians-diabetes")
discr("iris")
discr("wine")