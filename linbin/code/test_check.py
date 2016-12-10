# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 21:59:14 2016

@author: Administrator
"""

import pickle as pk
import csv
import re
import time
data_bank_detail_test=[]
data_bill_detail_test=[]
data_browse_history_test=[]
data_usersID_test=[]
data_bank_detail_uid=[]
data_bill_detail_uid=[]
data_browse_history_uid=[]
with open('./test/bank_detail_test.csv','rb') as f:
        reader = csv.reader(f)
        for item in reader:
            data_bank_detail_test.append(item)
with open('./test/bill_detail_test.csv','rb') as f:
        reader = csv.reader(f)
        for item in reader:
            data_bill_detail_test.append(item)
with open('./test/browse_history_test.csv','rb') as f:
        reader = csv.reader(f)
        for item in reader:
            data_browse_history_test.append(item)            
with open('./test/usersID_test.csv','rb') as f:
        reader = csv.reader(f)
        for item in reader:
            data_usersID_test.append(int(item[0]))
for item in data_bank_detail_test:
        uid=int(item[0])
        data_bank_detail_uid.append(uid)
for item in data_bill_detail_test:
        uid=int(item[0])
        data_bill_detail_uid.append(uid)
for item in data_browse_history_test:
        uid=int(item[0])
        data_browse_history_uid.append(uid)
data_bank_detail_uid=list(set(data_bank_detail_uid))                       
data_bill_detail_uid=list(set(data_bill_detail_uid))
data_browse_history_uid=list(set(data_browse_history_uid))

print "all_uid: "+str(len(data_usersID_test))
print "bank_uid:"+str(len(data_bank_detail_uid))
print "bill_uid:"+str(len(data_bill_detail_uid))
print "browse_uid:"+str(len(data_browse_history_uid))  

id_check={}
classication_check={}
classication_check["123"]=[]
classication_check["12"]=[]
classication_check["13"]=[]
classication_check["23"]=[]
classication_check["1"]=[]
classication_check["2"]=[]
classication_check["3"]=[]
classication_check["0"]=[]
print data_usersID_test[1] 
if  data_usersID_test[1] in data_bill_detail_uid and data_usersID_test[1] in data_browse_history_uid:
    print "true"
else:
    print "false"

for item in data_usersID_test:
    if item in data_bank_detail_uid and item in data_bill_detail_uid and item in data_browse_history_uid:
        id_check[item]="123"
        classication_check["123"].append(item)
    elif item in data_bank_detail_uid and item in data_bill_detail_uid:
        id_check[item]="12"
        classication_check["12"].append(item)
    elif item in data_bank_detail_uid and item in data_browse_history_uid:
        id_check[item]="13"
        classication_check["13"].append(item)
    elif item in data_bill_detail_uid and item in data_browse_history_uid:
        id_check[item]="23"
        classication_check["23"].append(item)
    elif item in data_bank_detail_uid:
        id_check[item]="1"
        classication_check["1"].append(item)
    elif item in data_bill_detail_uid:
        id_check[item]="2"
        classication_check["2"].append(item)
    elif item in data_browse_history_uid:
        id_check[item]="3"
        classication_check["3"].append(item)
    else:
        id_check[item]="0"
        classication_check["0"].append(item)

print "len(classication_check[123])"+str(len(classication_check["123"]))
print "len(classication_check[12])"+str(len(classication_check["12"]))        
print "len(classication_check[13])"+str(len(classication_check["13"]))
print "len(classication_check[23])"+str(len(classication_check["23"]))
print "len(classication_check[1])"+str(len(classication_check["1"]))
print "len(classication_check['2'])"+str(len(classication_check["2"]))    
print "len(classication_check['3'])"+str(len(classication_check["3"]))
print "len(classication_check['0'])"+str(len(classication_check["0"]))