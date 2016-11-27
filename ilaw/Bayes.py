from statistics import mean, stdev
import math


def calculate_probability(x, mean, stdev):
    if stdev == 0:
        return 1
    return math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2)))) / (math.sqrt(2 * math.pi) * stdev)


class Bayes(object):

    def __init__(self, train_set):
        self.mean_stdev_by_label = {}
        self._statistic_by_label(train_set)

    def _statistic_by_label(self, train_set):
        by_label = {}
        # break by_label
        for a in train_set:
            if a[1] in by_label:
                by_label[a[1]].append(a)
            else:
                by_label[a[1]] = [a]

        for k, v in by_label.items():
            params = [a[0] for a in v]
            self.mean_stdev_by_label[k] = [(mean(z), stdev(z)) for z in zip(*params)]

    def test(self, values):
        labels = {}
        for k, v in self.mean_stdev_by_label.items():
            probabilities = 1
            for i in range(len(values)):
                probabilities *= calculate_probability(values[0][i], v[i][0], v[i][1])
            labels[k] = probabilities
        return labels

    def get_label(self, values):
        labels = self.test(values)
        return max(labels, key=labels.get)

    def get_predictions(self, values):
        return [self.get_label(a) for a in values]

