def discretize_values(self, n_parts=10):
    max_v = []
    min_v = []
    diff_v = []
    for values in zip(*[a[0] for a in self.raw]):
        max_v.append(max(values))
        min_v.append(min(values))
        diff_v.append((max(values) - min(values)) / n_parts)

    buckets = []
    for ma, mi, di in zip(max_v, min_v, diff_v):
        b=[]
        for i in range(1, 1+n_parts):
            b.append((mi+i*di, i))
        buckets.append(b)
    self.discretized = []
    for pair in self.raw:
        new_v = []
        for value, b in zip(pair[0], buckets):
            for threshold, tier in b:
                if threshold > value:
                    new_v.append(tier)
                    break
        self.discretized.append((new_v, pair[1]))