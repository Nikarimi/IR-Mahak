
'''

    Nima Karimi
    Email: nimakarimi@gmail.com
    phD of Computer Eng(software)


'''

import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix
import math
import time

##############################################################
############ PRE PROCESSING ##################################

#df = pd.read_csv('nGraph.txt', header= None)
fop = open('web-graph.txt','r')
fwr = open('outdegree.txt','w')
webLinks = pd.read_csv('web-graph.txt',sep=' ', header= None)
countpages =webLinks.max()[0]

cnt = 0
outDeg=[]
sourcePages = []

rawSparsMat = pd.DataFrame()
for line in fop:
    nodeNo=line.split()[0]

    sourcePages.append(nodeNo)
    if cnt == 0:
        oldnodeNo = nodeNo
        counter = 0
        cnt += 1

    if nodeNo == oldnodeNo:
        counter += 1
    else:
        outDeg.append(counter)
        fwr.write(str(oldnodeNo) +' ' + str(counter) + '\n')
        oldnodeNo = nodeNo
        counter = 1

fwr.close()
fop.close()
webOut = webLinks.groupby(0).agg('count')
sourcePages = np.array(sourcePages,dtype=int)
rawSparsMat = webOut.loc[sourcePages].values
print(rawSparsMat.shape)
print(rawSparsMat)
rawSparsMat.shape = (rawSparsMat.shape[0],)
print(rawSparsMat.shape)


###################################################################
########################Make Sparse Matrix#########################

rowIndex = np.array(webLinks[0].values)
colIndex = np.array(webLinks[1].values)
rowIndex -= 1
colIndex -= 1
rwspMat = np.array(rawSparsMat)
rwspMat = 1 / rwspMat
spMat = csc_matrix((rwspMat,(rowIndex,colIndex)), shape=(countpages, countpages))

##################################################################
##################################################################
d = 0.85
eps = 10 ** -5
prankOri = np.ones(countpages)
prankTemp = np.zeros(countpages)

prankOri /= countpages

jumpScore = np.ones(countpages)
jumpScore *= (1-d)/countpages

iteration = 0
start_time = time.time()
while True:
    err = 0
    for i in range(countpages):
        fractionVal = spMat[:,i]
        linkScore = 0
        for j,value in zip(fractionVal.indices, fractionVal.data):
            linkScore += value * prankOri[j]
        prankTemp[i] = jumpScore[i] + d*linkScore
        err += abs(prankTemp[i] - prankOri[i])**2
    iteration += 1
    err = math.sqrt(err)
    prankTemp = prankTemp / np.sum(prankTemp)
    print('iteration:%02d error:%.12f sum:%.2f'% (iteration, err, np.sum(prankTemp)))
    if err <= eps or iteration > 100:
        break
    prankOri = np.copy(prankTemp)
    prankTemp = np.zeros(countpages)

end_time = time.time()
print('Run Time: %03d:%03d' % divmod((end_time - start_time), 60))
dfprank = pd.DataFrame(prankTemp)
dfprank.to_csv('prank.txt', header=False, index=False)
print(dfprank.describe())
