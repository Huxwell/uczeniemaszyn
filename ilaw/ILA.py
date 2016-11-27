import operator
import random
import re

_fill_value = ".*"


def list_to_string(lis):
    l = []
    for a in lis:
        try:
            l.append(str(a))
        except TypeError:
            pass  # string
    return l


class ILA(object):
    def __init__(self, train_set):
        self.rules = []
        new_train = []
        for attrs, lab in train_set:
            new_train.append((list_to_string(attrs), lab))
        self._train(new_train)

    def _maches_rule(self, rule, attr):
        for a, b in zip(list(rule), attr):
            # rec = re.compile(a)
            # if rec.match(b) is None:
            #     return False
            if a != _fill_value and a != b:
                return False
        return True

    def _combinations_rec(self, pattern, i, j):
        if len([x for x in pattern if x != _fill_value]) == j:
            return {tuple(pattern)}
        if i >= len(pattern):
            return set()
        new_pattern = pattern[:]
        new_pattern[i] = _fill_value
        return self._combinations_rec(pattern[:], i + 1, j) | self._combinations_rec(new_pattern, i + 1, j)

    def _combinations(self, attrs, j):
        combinations = set()
        for a in attrs:
            combinations |= self._combinations_rec(a, 0, j)
        return combinations

    def _train(self, train_set):
        length_of_attr_list = len(train_set[0][0])
        distinct_by_label = {}
        # break by_label
        for a in train_set:
            if a[1] in distinct_by_label:
                distinct_by_label[a[1]].append(a)
            else:
                distinct_by_label[a[1]] = [a]

        for label, label_table in distinct_by_label.items():
            unmarked = label_table[:]
            j = 1
            while (j < length_of_attr_list  # j jest mniejsze od ilosci atrybutow
                   and len(unmarked) > 0):  # w tablicy sa jeszcze elementy
                combinations = self._combinations([a[0] for a in unmarked], j)

                # eliminating rules matching for others classes
                matching_rules = []
                for c in combinations:
                    is_good = True
                    for label_2, label_table_2 in distinct_by_label.items():
                        if label != label_2:
                            for attr in [a[0] for a in label_table_2]:
                                if self._maches_rule(c, attr):
                                    is_good = False
                    if is_good:
                        matching_rules.append([c, 0])

                while len(matching_rules) > 0:
                    # couting matches
                    for m in matching_rules:
                        m[1] = 0
                        for attr in unmarked:
                            if self._maches_rule(m[0], attr[0]):
                                m[1] += 1

                    best_rule = max(matching_rules, key=operator.itemgetter(1))
                    # add rule
                    if best_rule[1] > 0:

                        self.rules.append((best_rule[0], label))
                        matching_rules.remove(best_rule)
                        # mark as matched
                        for attr in unmarked[:]:
                            if self._maches_rule(best_rule[0], attr[0]):
                                unmarked.remove(attr)
                    else:
                        matching_rules = []

                j += 1

    def test(self, values):
        values = (list_to_string(values[0]), values[1])
        for rule in self.rules:
            if self._maches_rule(rule[0], values[0]):
                return rule[1]
        else:
            labels = [a[1] for a in self.rules]
            return random.choice(labels)

    def get_predictions(self, values):
        return [self.test(a) for a in values]
