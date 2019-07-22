
'''

    Nima Karimi
    Email: nimakarimi@gmail.com
    phD of Computer Eng(software)


'''

import pandas as pd
import time
import xml.dom.minidom
from xml.dom.minidom import parse
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
import os, os.path
from whoosh import index



if not os.path.exists("indexFolder"):
    os.mkdir("indexFolder")

schema = Schema(docid=ID(stored=True), title=TEXT(stored=True), body=TEXT(stored=True))
ix = index.create_in("indexFolder", schema)
ix = index.open_dir("indexFolder")
writer = ix.writer()

start_time = time.time()
last_time = start_time

indexLog = []
fw = open('indexLog.txt','w')

for i in range(462):
    fiName = "WIR\WebIR-%03d.xml"
    if not os.path.exists(fiName % i):
        continue
    dom_data = xml.dom.minidom.parse(fiName % i)

    docs_in_file = dom_data.documentElement
    Documents = docs_in_file.getElementsByTagName('DOC')

    for document in Documents:

        temp_id = document.getElementsByTagName('DOCID')[0]
        doc_Id = temp_id.childNodes[0].data

        temp_title = document.getElementsByTagName('TITLE')[0]
        if temp_title.childNodes != []:
           doc_Title = temp_title.childNodes[0].data
        else:
           doc_Title = ''

        temp_body = document.getElementsByTagName('BODY')[0]
        if temp_body.childNodes != []:
           doc_Body = temp_body.childNodes[0].data
        else:
           doc_Body = ''

        writer.add_document(docid=doc_Id, title=doc_Title, body=doc_Body)

    now_time=time.time()
    print('File ID: %03d' % (i) + ' ---> Indexing RunTime:%02d:%02d' % divmod((now_time - last_time), 60))
    fw.write('File ID: %03d' % (i) + ' ---> Indexing RunTime:%02d:%02d' % divmod((now_time - last_time), 60))
    indexLog.append([i, divmod((now_time - last_time), 60)])
    last_time = now_time

writer.commit()
end_time = time.time()
print('Total RunTime:%03d:%03d' % divmod((end_time - start_time), 60))
fw.write('Total RunTime:%03d:%03d' % divmod((end_time - start_time), 60))
fw.close()
print(indexLog)
dfIndex = pd.DataFrame(indexLog)
dfIndex.to_csv('index-run.txt')