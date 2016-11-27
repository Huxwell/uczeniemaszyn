import cPickle as pickle
import numpy as np
from itertools import izip

def discr(name):
    def discretize_equal_no_rows(data_column, number_of_final_sets):
        def __find_bads(elem, sets):
            for set in sets:
                if elem in set:
                    return min(set),max(set)
        sorted_data = sorted(data_column)
        splited_array = np.array_split(sorted_data, number_of_final_sets)
        parsed_data_column = []
        for elem in data_column:
            begin, end = __find_bads(elem, splited_array)
            parsed_data_column.append(begin)
        return parsed_data_column
    for n_parts in xrange(2,20):
        raw=[]
        with open('../../data/interim/'+name+'.pkl', 'rb') as f:
            raw = pickle.load(f)
        X = [row[0] for row in raw]
        X = map(list, zip(*X)) #transposition
        X = [discretize_equal_no_rows(x,n_parts) for x in X]
        X = map(list, zip(*X))

        data = [(r,l[1]) for r, l in izip(X,raw)]
        print data[12:17]
        with open('../../data/processed/'+name+'_discretized_no_rows_'+str(n_parts)+'.pkl', 'wb') as f:
            pickle.dump(data,f)
discr("pima-indians-diabetes")
discr("iris")
discr("wine")