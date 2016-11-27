from multiprocessing import Process
from statistics import mean

from ILA import ILA
from Bayes import Bayes
from DataSet import DataSet
from LoadDataSets import *
from scoring import *

tested_class = ILA


def cross_validation(dataset, n_folds=10, reapets=3):
    results = []
    for i in range(reapets):
        values = dataset.cross_validation(n_folds)
        for v in values:
            bayes = tested_class(v["train"])
            results.append(score(v["test"], bayes.get_predictions(v["test"])))
    return [mean(a) for a in zip(*results)]


def discretization_test(raw, filename):
    with open(filename, "w") as f:
        f.write("n;precision;recall;accuracy;f1\n")
        dataset = DataSet(raw)
        for i in [5, 7, 10, 15, 20, 40]:
            dataset.discretize_values(i)
            res = cross_validation(dataset)
            res = [str(i)] + [str(a) for a in res]
            f.write(";".join(res) + "\n")


def rules_generated_test(raw, filename):
    with open(filename, "w") as f:
        f.write("n;rules\n")
        dataset = DataSet(raw)
        for i in [3, 4, 5, 6, 7, 8, 9, 10]:
            dataset.discretize_values(i)
            results = []
            for j in range(3):  # liczba prób
                values = dataset.cross_validation(5)
                for v in values:
                    bayes = ILA(v["train"])
                    results.append(len(bayes.rules))
            f.write(str(i) + ";" + str(mean(results)) + "\n")


ths = []
ths.append(Process(target=rules_generated_test, args=(load_GLASS(), "results/rulesGLASS.csv")))
ths.append(Process(target=rules_generated_test, args=(load_WINE(), "results/rulesWINE.csv")))
ths.append(Process(target=rules_generated_test, args=(load_banknote(), "results/rulesbanknote.csv")))

ths.append(Process(target=discretization_test, args=(load_GLASS(), "results/discretizationGLASS.csv")))
ths.append(Process(target=discretization_test, args=(load_WINE(), "results/discretizationWINE.csv")))
ths.append(Process(target=discretization_test, args=(load_banknote(), "results/discretizationbanknote.csv")))

for t in ths:
    t.start()

for t in ths:
    t.join()

# ila = ILA(DataSet(load_weather()).split_train_test()["train"])
# print(ila.rules)
