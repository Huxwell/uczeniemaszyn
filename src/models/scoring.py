from __future__ import division
def _create_conf_matrix(expected, predicted):
    # dict[predicted value][expected value] = number of occurrences
    len_labels = len(set(expected))
    d = {}
    for a in set(expected) | set(predicted):
        d[a] = {}
        for b in set(expected) | set(predicted):
            d[a][b] = 0
    for pred, exp in zip(predicted, expected):
        d[pred][exp] += 1
    return d


def _precision(conf_matrix):
    sum = 0
    for k, v in conf_matrix.items():
        TP = conf_matrix[k][k]
        FP = 0
        for k2, v2 in v.items():
            if k2 != k:
                FP += v2
        if TP + FP != 0:
            sum += TP / (TP + FP)
    return sum / len(conf_matrix)


def _recall(conf_matrix):
    sum = 0
    for k, v in conf_matrix.items():
        TP = conf_matrix[k][k]
        FN = 0
        for k2, v2 in conf_matrix.items():
            if k2 != k:
                FN += v2[k]
        if TP + FN != 0:
            sum += TP / (TP + FN)
    return sum / len(conf_matrix)


def _accuracy(conf_matrix):
    all = 0
    for k, v in conf_matrix.items():
        for k2, v2 in v.items():
            all += v2
    sum = 0
    for k, v in conf_matrix.items():
        TP = conf_matrix[k][k]
        TN = 0
        for k2, v2 in conf_matrix.items():
            if k2 != k:
                for k3, v3 in v2.items():
                    TN += v3
        sum += (TP + TN) / all
    return sum / len(conf_matrix)


def score(y_true, y_pred):
    conf_matrix = _create_conf_matrix(y_true, y_pred)
    # print conf_matrix
    prec = _precision(conf_matrix)
    rec = _recall(conf_matrix)
    acc = _accuracy(conf_matrix)
    if prec+rec != 0:
        f1 = 2 * prec * rec / (prec + rec)
    else:
        f1 = 0
    return prec, rec, acc, f1
