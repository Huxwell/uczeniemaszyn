import random


class DataSet(object):
    def __init__(self, data):
        self.raw = data
        self.discretized = None

    def cross_validation(self, n_folds=5):
        if n_folds > len(self.raw):
            raise IndexError("N is larger than set size")
        if self.discretized is None:
            values = self.raw
        else:
            values = self.discretized
        data = []
        fold_size = int(len(values) / n_folds)
        random.shuffle(values)
        for i in range(n_folds):
            d = {"test": values[i * fold_size:][:fold_size],
                 "train": values[(i + 1) * fold_size:] + values[:i * fold_size]}
            data.append(d)
        return data

    def split_train_test(self, test_ratio=0.25):
        if test_ratio > 1 or test_ratio < 0:
            raise IndexError("Wrong ratio")
        if self.discretized is None:
            values = self.raw
        else:
            values = self.discretized
        test_size = int(len(values) * test_ratio)
        random.shuffle(values)
        return {"test": values[:test_size],
                "train": values[test_size:]}

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
            b = []
            for i in range(1, 1 + n_parts):
                b.append((mi + i * di, i))
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

    # def k_means_dicretization(self, n_parts=10):

    def remove_discretization(self):
        self.discretized = None
