import cPickle as pickle
with open('../../data/raw/pima-indians-diabetes') as f:
    data = [line for line in f]
print data[15:20]
with open('../../data/interim/pima-indians-diabetes.pkl', 'rb') as f:
    data = pickle.load(f)
print data[15:20]
with open('pima-indians-diabetes_discretized_equal_enc_4.pkl', 'rb') as f:
    data = pickle.load(f)
print data[15:20]
with open('pima-indians-diabetes_discretized_equal_4.pkl', 'rb') as f:
    data = pickle.load(f)
print data[15:20]
with open('pima-indians-diabetes_discretized_no_rows_4.pkl', 'rb') as f:
    data = pickle.load(f)
print data[15:20]