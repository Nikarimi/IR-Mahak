
'''

    Nima Karimi
    Email: nimakarimi@gmail.com
    phD of Computer Eng(software)


'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

diagramTitle = []
diagramTitle.append('Alpha=0.0 -- Beta=1.0')
fileName = []
fileName.append('Output(PageRank-BM25)Alpha=0.0 Beta=1.0.txt')
for i in range(1,10):
    fileName.append('Output(PageRank-BM25)Alpha=0.' + str(i%10) + ' Beta=0.'+str(10-i%10)+'.txt')
    diagramTitle.append('Alpha=0.' + str(i%10) + ' -- Beta=0.'+str(10-i%10))

fileName.append('Output(PageRank-BM25)Alpha=1.0 Beta=0.0.txt')
diagramTitle.append('Alpha=1.0 -- Beta=0.0')
print(fileName)
print(len(fileName))
print(diagramTitle)
print(len(diagramTitle))

dflist = []
at_ten = []
at_twenty = []
at_fifty = []
avgFinal = []
avgAll = []
for i in range(11):
    at_ten = []
    at_twenty = []
    at_fifty = []
    avgvec = []
    freads = open(fileName[i],'r')
    for line in freads:
        line = line.split()
        at_ten.append(int(line[0]))
        at_twenty.append(int(line[1]))
        at_fifty.append(int(line[2]))


    avgten = np.average(at_ten)
    avgtwenty = np.average(at_twenty)
    avgfifty = np.average(at_fifty)
    avgvec.append(avgten)
    avgvec.append(avgtwenty)
    avgvec.append(avgfifty)
    avgFinal.append(avgvec)

    avgAll.append((avgten + avgtwenty + avgfifty)/3)





print(avgFinal)

avgFinal_at_ten = []
avgFinal_at_twenty = []
avgFinal_at_fifty = []
for i in range(11):
    avgFinal_at_ten.append(avgFinal[i][0])
    avgFinal_at_twenty.append(avgFinal[i][1])
    avgFinal_at_fifty.append(avgFinal[i][2])




plt.xlabel('N(for Precision @N)')
plt.ylabel('Precision(Related DOCs in N results)')
plt.title('Average Precision per Alpha(PageRank),Beta(BM25)')
plt.plot([10,20,50],avgFinal[0],'bo-.',label = str(diagramTitle[0]))
plt.plot([10,20,50],avgFinal[1],'c^-',label = str(diagramTitle[1]))
plt.plot([10,20,50],avgFinal[2],'k*-',label = str(diagramTitle[2]))
plt.plot([10,20,50],avgFinal[3],'y+-',label = str(diagramTitle[3]))
plt.plot([10,20,50],avgFinal[4],'b*-',label = str(diagramTitle[4]))
plt.plot([10,20,50],avgFinal[5],'g^-',label = str(diagramTitle[5]))
plt.plot([10,20,50],avgFinal[6],'k+-',label = str(diagramTitle[6]))
plt.plot([10,20,50],avgFinal[7],'y*-',label = str(diagramTitle[7]))
plt.plot([10,20,50],avgFinal[8],'c*-',label = str(diagramTitle[8]))
plt.plot([10,20,50],avgFinal[9],'r+-',label = str(diagramTitle[9]))
plt.plot([10,20,50],avgFinal[10],'bo-.',label = str(diagramTitle[10]))
plt.legend(loc = 0)
plt.show()


'''
print(avgFinal_at_ten)
#plt.bar(avgFinal_at_ten,height=10,width=0.5, color = ['b','c','y','k','r','g','r','c','y','g','b'])
for i in range(11):
    plt.plot(i+1 , avgFinal_at_ten[i],'o-',label = diagramTitle[i])
plt.legend(loc = 0)
plt.show()
'''
################################################################################################
###################### BAR DIAGRAM #############################################################
barColor = ['k','b','c','c','c','c','c','c','c','c','k']
barTitle = ['0.0,1.0','0.1,0.9','0.2,0.8','0.3,0.7','0.4,0.6','0.5,0.5','0.6,0.4','0.7,0.3','0.8,0.2','0.9,0.1','1.0,0.0']
x_pos = [i for i, _ in enumerate(avgFinal_at_ten)]
plt.bar(x_pos, avgFinal_at_ten,color = barColor)
plt.xlabel("Alpha(PageRank), Beta(BM25)")
plt.ylabel("Precision at 10")
plt.title("PRECISION DIAGRAM(@10)")
plt.xticks(x_pos,barTitle)

plt.show()

##################################################################################
barTitle = ['0.0,1.0','0.1,0.9','0.2,0.8','0.3,0.7','0.4,0.6','0.5,0.5','0.6,0.4','0.7,0.3','0.8,0.2','0.9,0.1','1.0,0.0']
x_pos = [i for i, _ in enumerate(avgFinal_at_twenty)]
plt.bar(x_pos, avgFinal_at_twenty,color = barColor)
plt.xlabel("Alpha(PageRank), Beta(BM25)")
plt.ylabel("Precision at 20")
plt.title("PRECISION DIAGRAM(@20)")
plt.xticks(x_pos,barTitle)

plt.show()


#####################################################################################
barTitle = ['0.0,1.0','0.1,0.9','0.2,0.8','0.3,0.7','0.4,0.6','0.5,0.5','0.6,0.4','0.7,0.3','0.8,0.2','0.9,0.1','1.0,0.0']
x_pos = [i for i, _ in enumerate(avgFinal_at_fifty)]
plt.bar(x_pos, avgFinal_at_fifty,color = barColor)
plt.xlabel("Alpha(PageRank), Beta(BM25)")
plt.ylabel("Precision at 50")
plt.title("PRECISION DIAGRAM(@50)")
plt.xticks(x_pos,barTitle)

plt.show()

#####################################################################################
print('================AVG ALL================')
print(avgAll)
#####################################################################################
barTitle = ['0.0,1.0','0.1,0.9','0.2,0.8','0.3,0.7','0.4,0.6','0.5,0.5','0.6,0.4','0.7,0.3','0.8,0.2','0.9,0.1','1.0,0.0']
x_pos = [i for i, _ in enumerate(avgAll)]
plt.bar(x_pos, avgAll,color = barColor)
plt.xlabel("Alpha(PageRank), Beta(BM25)")
plt.ylabel("Precision")
plt.title("PRECISION DIAGRAM(Average @N(s))")
plt.xticks(x_pos,barTitle)

plt.show()


