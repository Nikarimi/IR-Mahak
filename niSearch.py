
'''

    Nima Karimi
    Email: nimakarimi@gmail.com
    phD of Computer Eng(software)


'''


import time
import heapq
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import index, scoring
from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
import numpy as np
import math




RESULTS = []
QUERIES = {}

RESULTS_DOCID=[]
RESULTS_DOCSCORE=[]

have_result = np.zeros(46)

weight_title = 0.6
weight_body = 0.4



#####################################################################
########### READ RESULTS from XMLs ##################################

for i in range(1, 46):
   sub_result =[]
   fiName = r"Meta\query-%s.xml" % (i)
   dom_docs = xml.dom.minidom.parse(fiName)
   doc_in_file = dom_docs.documentElement
   Docs = doc_in_file.getElementsByTagName('doc')

   for document in Docs:
       temp_id = document.getElementsByTagName('docid')[0]
       doc_Id = temp_id.childNodes[0].data

       temp_label = document.getElementsByTagName('label')[0]
       doc_Label = temp_label.childNodes[0].data

       if doc_Label == '1' or doc_Label == '2':
            sub_result.append(doc_Id)

        #print(sub_result)
        #print(len(sub_result))


   RESULTS.append(sub_result)


##############################################################
########## Read PageRank score ###############################

page_rank = pd.read_csv('prank.txt', header=None)

page_rank = np.array(page_rank)



##############################################################
########## Read QUERIES from Indexs ############################


fiName = r"Meta\query.xml"
dom_query = xml.dom.minidom.parse(fiName)
query_in_file = dom_query.documentElement
Queries = query_in_file.getElementsByTagName("QUERY")
for query in Queries:
   id = query.getElementsByTagName('ID')[0].childNodes[0].data
   QUERIES[id] = {}
   temp_title = query.getElementsByTagName('TITLE')[0]
   QUERIES[id]['title'] = temp_title.childNodes[0].data
   temp_description = query.getElementsByTagName('DESCRIPTION')[0]
   QUERIES[id]['description'] = temp_description.childNodes[0].data
   temp_narrative = query.getElementsByTagName('NARRATIVE')[0]
   QUERIES[id]['narrative'] = temp_narrative.childNodes[0].data


ix = index.open_dir('indexFolder')
srch = ix.searcher()


#have_result = np.zeros(41)
for query_No in range(1,46):
    docids=[]
    docscores=[]
    query_parser = MultifieldParser(fieldnames=['title','body'], schema=ix.schema, fieldboosts={'title':weight_title,'body':weight_body,})
    query = QUERIES[str(query_No)]['title']
    query = query_parser.parse(query)
    results = srch.search(query, limit= None)

    doc_result_count = len(results)
    print(len(results))
    if len(results) != 0:
        have_result[query_No] = 1
        for res in results:
            docids.append(res['docid'])
            docscores.append(res.score)
    RESULTS_DOCID.append(docids)
    RESULTS_DOCSCORE.append(docscores)


    #print('============================================================================================')





############################################################################################
################## Make Results by BM25 , BM25-PageRank ####################################
'''
patNall = []
patNres = []

for i in range(1,51):
     patNres = []
     for patN in [10, 20, 50]:
         result_set = set(RESULTS[i-1])
         quresult_set = set(RESULTS_DOCID[i-1][:patN])
         inter = result_set.intersection(quresult_set)
         print(result_set)
         print(quresult_set)
         print(inter)
         print(len(inter))
         print('===========================================================')
         print('===========================================================')
         patNres.append(len(inter))
     patNall.append(patNres)
#print(patNall) #This list has the result of BM25 for each Query


fw = open('OutputBM25.txt','w')
for line in patNall:
    fw.write(str(line[0])+' '+ str(line[1])+' '+str(line[2])+'\n')

fw.close()
'''

############################################################################################
################## Make Results by  BM25-PageRank ####################################
alpha = 0.0
beta = 0.0
patNallBMPR = []
patNresBMPR = []
for i in range(1,46):
     patNresBMPR = []
     for patN in [10, 20, 50]:
         qreslt = []
         ##############################################
         ########### Page Rank Score Extract and Normalization #################
         prResultIndexTmp = np.array(RESULTS_DOCID[i-1])
         #print(prResultIndexTmp)
         prResultIndex = []
         for indxs in prResultIndexTmp:
             prResultIndex.append(int(indxs) - 1)
         prResultIndex = np.array(prResultIndex,dtype=int)
         prResult = np.array(page_rank[prResultIndex])
         ######################################
         #print(prResultIndex)
         #print(prResult)
         if len(prResult) > 0 :
            minPR = np.min(prResult)
            maxPR = np.max(prResult)
            NormalprResult = (prResult - minPR) / (maxPR - minPR) #It has Normalized PageRank
         ########### BM25 Score Normalization #################################
            bm25Result = np.array(RESULTS_DOCSCORE[i-1])
            minBM25 = np.min(bm25Result)
            maxBM25 = np.max(bm25Result)
            Normalbm25Result = (bm25Result - minBM25) / (maxBM25 - minBM25)

         ##################### NEW SCORE (BM25 and PageRank)

            newScore =[]
            for j in range(len(NormalprResult)):
                newScore.append((alpha * NormalprResult[j]) + (beta * Normalbm25Result[j]))

            newScore = np.array(newScore)
            minNEWSCR = np.min(newScore)
            maxNEWSCR = np.max(newScore)
            NormalNewScore = (newScore - minNEWSCR) / (maxNEWSCR - minNEWSCR)
            print('===============Normal PageRank Score ====================')
            print(NormalprResult)
            print(np.min(NormalprResult),np.max(NormalprResult))
            print('===============Normal BM25 Score ====================')
            print(Normalbm25Result)
            print(np.min(Normalbm25Result),np.max(Normalbm25Result))
            print('===============Normal NEW Score ====================')
            print(NormalNewScore)
            print(np.min(NormalNewScore), np.max(NormalNewScore))


         ############### Take N top score indices #################
            NormalNewScore = np.array(NormalNewScore)
            patNindex = heapq.nlargest(patN, range(len(NormalNewScore)), NormalNewScore.take)
            patNindex = np.array(patNindex,dtype=int)
         #patNindex.shape = patNindex.shape[0]
            print('patNindex is:')
            print(patNindex)
        ###########################################
            qres = np.array(RESULTS_DOCID[i-1])

            for j in (patNindex):
               qreslt.append(qres[j])

         #print('============= QRESLT ===================')
         #print(qreslt)
         #print('============ END qreslt =================')
         qunewResult_set = set(qreslt)
         #print(qunewResult_set)
         ##########################################
         #print('==================== Length of RESULTS ==================')
         #print(len(RESULTS))
         #print('============= i - 1 ============')
         #print(i-1)
         result_set = set(RESULTS[i-1])
         #qunewResult_set =set(RESULTS_DOCID[i-1][patNindex])
         newinter = result_set.intersection(qunewResult_set)
         #print(result_set)
         #print(qunewResult_set)
         #print(newinter)
         #print(len(newinter))
         #print('===========================================================')
         #print('===========================================================')
         patNresBMPR.append(len(newinter))

         #################################################
     patNallBMPR.append(patNresBMPR)
#print(patNallBMPR) #This list has the result of BM25 for each Query

fileName = 'Output(PageRank-BM25)Alpha=' + str(alpha) + ' Beta='+str(beta)+'.txt'
fw = open(fileName,'w')
for line in patNallBMPR:
    fw.write(str(line[0])+' '+ str(line[1])+' '+str(line[2])+'\n')

fw.close()




