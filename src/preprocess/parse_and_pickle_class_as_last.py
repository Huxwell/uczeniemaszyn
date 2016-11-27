import cPickle as pickle
import random
data = []
#iris i indians
name="iris"
with open('../../data/raw/'+name) as f:
    for line in f:
        print line
        params = line.split(",")
        params = [a.strip() for a in params]
        if len(params) < 2:  # empty/broken line
            continue
        #label = params.pop(0)
        label = params.pop(-1) #if label is at the end of line
        data.append(([float(a) for a in params], label))
random.shuffle(data)
print data[4:7]
with open('../../data/interim/'+name+'.pkl', 'wb') as f:
    pickle.dump(data,f)
with open('../../data/interim/'+name+'.pkl', 'rb') as f:
    print pickle.load(f)[0:20]

name="pima-indians-diabetes"
with open('../../data/raw/'+name) as f:
    for line in f:
        print line
        params = line.split(",")
        params = [a.strip() for a in params]
        if len(params) < 2:  # empty/broken line
            continue
        #label = params.pop(0)
        label = params.pop(-1) #if label is at the end of line
        data.append(([float(a) for a in params], label))
random.shuffle(data)
print data[4:7]
with open('../../data/interim/'+name+'.pkl', 'wb') as f:
    pickle.dump(data,f)
with open('../../data/interim/'+name+'.pkl', 'rb') as f:
    print pickle.load(f)[0:20]

