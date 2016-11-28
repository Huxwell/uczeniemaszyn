from __future__ import division
from scoring import *
from ILA import ILA
import os
import random
import cPickle as pickle

# model = ILA(data[:int(len(data)*0.8)])
# test = data[int(len(data)*0.8):]
# # print test
# y_pred = model.get_predictions(test)
# print model.rules
# # print y_pred
# y_true = [a[1] for a in test]
# print y_true
# print score(y_true,y_pred)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
def cross_validation(values,n_folds):
    data = []
    fold_size = int(len(values) / n_folds)
    random.shuffle(values)
    for i in range(n_folds):
        d = {"test": values[i * fold_size:][:fold_size],
             "train": values[(i + 1) * fold_size:] + values[:i * fold_size]}
        data.append(d)
    return data
def fit(data):
    cv = cross_validation(data,n_folds)
    scores=[]
    for row in cv:
        model = ILA(row['train'])
        print model.rules
        y_pred = model.get_predictions(row['test'])
        y_true = [a[1] for a in row['test']]
        scores.append(score(y_true,y_pred))
    scores = map(list, zip(*scores))
    means = [mean(s) for s in scores]
    return means

def fit_cv(datapath,dirpath):
    # with open("../../data/processed/"+raw_dataset+"_discretized_equal_3.pkl","rb") as f:
    #     data = pickle.load(f)



    # print fit(data)
    names = [l for l in os.listdir(dirpath) if datapath in l]
    # print names

    results = {}
    for name in names:
        with open(dirpath+name,"rb") as f:
            data = pickle.load(f)
            # print name
            # print fit(data)
            results[name] = fit(data)

    # nos = [n.split('_')[-1] for n in names]
    # print nos
    print results
    with open(datapath+'log','w') as f:
        f.write(str(results))


n_folds = 5
dirpath = '../../data/processed/'


# datapath = 'iris_discretized_equal_'
# fit_cv(datapath,dirpath)
# datapath = 'iris_discretized_no_rows_'
# fit_cv(datapath,dirpath)

# datapath = 'wine_discretized_no_rows_'
# fit_cv(datapath,dirpath)
# datapath = 'wine_discretized_no_rows_'
# fit_cv(datapath,dirpath)

# datapath = 'pima-indians-diabetes_discretized_no_rows_'
# fit_cv(datapath,dirpath)
datapath = 'pima-indians-diabetes_discretized_equal_'
fit_cv(datapath,dirpath)