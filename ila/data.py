import csv
import functools
import numpy as np
from random import shuffle


def is_float(s):
    return s.replace('.', '', 1).isdigit()


def flatten(list):
    return functools.reduce(lambda x, y: x + y, list)


class Data(object):
    def __init__(self):
        self.target = []
        self.dataset = []

    def load(self, filename, target_column, nominal_columns=None):
        target_column -= 1  # count from 1 not 0
        lines = list(csv.reader(open(filename, "r")))
        self.dataset, self.target = self.parse_lines(lines, nominal_columns, target_column)

    def discretizie(self, discretization_method, atr_no=None, number_of_final_sets=10):
        new_dataset = []
        for index, column in enumerate(np.array(self.dataset).T):
            if (atr_no is None or atr_no[index]) and column[0] is not np.str_:
                new_dataset.append(discretization_method(column, number_of_final_sets))
            else:
                new_dataset.append(column)
        self.dataset = np.array(new_dataset).T

    def crossvalidation_sets(self, number_of_parts):
        datasets, targets = self.get_split(number_of_parts)
        return [x for x in self.split(datasets, targets)]

    def crossvalidation_gen(self, number_of_parts):
        datasets, targets = self.get_split(number_of_parts)
        return self.split(datasets, targets)

    def parse_lines(self, _lines, nominal_values, target_column):
        # mixing elements, so crosswalidation wont have one class
        lines = [line for line in _lines]
        shuffle(lines)
        # parsing
        target, dataset = [], []
        for line in lines:
            if line: # lines on the end of file
                target.append(line[target_column])
                dataset.append(self.parse_line(line[:target_column] + line[target_column + 1:], nominal_values))
        return dataset, target

    def parse_line(self, line, nominal_values=None):
        if nominal_values:
            return [x if nominal_values[i] else float(x) for i, x in enumerate(line)]
        else:
            return [float(x) if is_float(x) else x for x in line]

    def split(self, datasets, targets):
        for i in range(len(datasets)):
            training_set = flatten(datasets[:i] + datasets[i + 1:])
            training_target = flatten(targets[:i] + targets[i + 1:])
            test_set = datasets[i]
            test_target = targets[i]
            yield ((training_set, training_target), (test_set, test_target))

    def get_split(self, n):
        datasets = [[] for _ in range(n)]
        targets = [[] for _ in range(n)]
        for key, elem in enumerate(self.dataset):
            datasets[key % n].append(elem)
            targets[key % n].append(self.target[key])
        return datasets, targets
