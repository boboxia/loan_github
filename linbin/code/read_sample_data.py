# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 08:59:53 2016

@author: Linbin
"""

import pickle as pk
import csv
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
#import re
#import time

def read_sample():
    small_train_data = []
    small_train_target = []
    small_test_data = []
    small_test_target_true = []
    sample_data_bank_detail=[]
    sample_data_bank_detail_train=[]
    sample_data_bank_detail_test=[]
    sample_data_bill_detail=[]
    sample_data_bill_detail_train=[]
    sample_data_bill_detail_test=[]
    sample_data_browse_history=[]
    sample_data_browse_history_train=[]
    sample_data_browse_history_test=[]
    sample_data_loan_time=[]
    sample_data_loan_time_train=[]
    sample_data_loan_time_test=[]
    sample_data_overdue=[]
    sample_data_overdue_train=[]
    sample_data_overdue_test=[]
    sample_data_user_info=[]
    sample_data_user_info_train=[]
    sample_data_user_info_test=[]
#    small_test = []
    with open('./train/small10/loan_small_bank_detail_train.csv','rb') as f1:
        reader = csv.reader(f1)
        for item in reader:
            sample_data_bank_detail.append(item)
            if(int(item[0])<=5000):
                sample_data_bank_detail_train.append(item)
            else:
                sample_data_bank_detail_test.append(item)
    
    print "len(sample_data_bank_detail_train)"+str(len(sample_data_bank_detail_train))
    print "len(sample_data_bank_detail_test)"+str(len(sample_data_bank_detail_test))
        
    with open('./train/small10/loan_small_bill_detail_train.csv','rb') as f2:
        reader = csv.reader(f2)
        for item in reader:
            sample_data_bill_detail.append(item)
            if(int(item[0])<=5000):
                sample_data_bill_detail_train.append(item)
            else:
                sample_data_bill_detail_test.append(item)
            
    with open('./train/small10/loan_small_browse_history_train.csv','rb') as f3:
        reader = csv.reader(f3)
        for item in reader:
            sample_data_browse_history.append(item)
            if(int(item[0])<=5000):
                sample_data_browse_history_train.append(item)
            else:
                sample_data_browse_history_test.append(item)
            
    with open('./train/small10/loan_small_loan_time_train.csv','rb') as f4:
        reader = csv.reader(f4)
        for item in reader:
            sample_data_loan_time.append(map(int,item))
            if(int(item[0])<=5000):
                sample_data_loan_time_train.append(map(int,item))
            else:
                sample_data_loan_time_test.append(map(int,item))
            
    with open('./train/small10/loan_small_overdue_train.csv','rb') as f5:
        reader = csv.reader(f5)
        for item in reader:
            sample_data_overdue.append(map(int,item))
            if(int(item[0])<=5000):
                sample_data_overdue_train.append(map(int,item))
            else:
                sample_data_overdue_test.append(map(int,item))
                
           
    with open('./train/small10/loan_small_user_info_train.csv','rb') as f6:
        reader = csv.reader(f6)
        for item in reader:
            sample_data_user_info.append(map(int,item))
            
            if(int(item[0])<=5000):
                sample_data_user_info_train.append(map(int,item))
            else:
                sample_data_user_info_test.append(map(int,item))
    
    print "len(sample_data_user_info_train)"+str(len(sample_data_user_info_train))
    print "len(sample_data_user_info_test)"+str(len(sample_data_user_info_test))
    sdbkd_tr=sample_data_bank_detail_train
    sdbkd_te=sample_data_bank_detail_test
    sdbid_tr=sample_data_bill_detail_train
    sdbid_te=sample_data_bill_detail_test
    sdbh_tr=sample_data_browse_history_train
    sdbh_te=sample_data_browse_history_test
    sdlt_tr=sample_data_loan_time_train
    sdlt_te=sample_data_loan_time_test
    sdo_tr=sample_data_overdue_train
    sdo_te=sample_data_overdue_test
    sdui_tr=sample_data_user_info_train
    sdui_te=sample_data_user_info_test
    
    
    
    user_info={}
    for uid in range(len(sample_data_user_info)):
        user_info[uid+1]=[0]*6
    print "len(sample_data_user_info_train)"+str(len(sample_data_user_info_train))
    print "len(user_info)"+str(len(user_info))
    print user_info[1]#键最小
    print user_info[5000]#键最大
    print user_info[5560]#键最大
    for item in sample_data_user_info:
        uid=item[0]
        user_info[uid][0]=item[0]
        user_info[uid][1]=item[1]
        user_info[uid][2]=item[2]
        user_info[uid][3]=item[3]
        user_info[uid][4]=item[4]
        user_info[uid][5]=item[5]
    print "len(user_info)"+str(len(user_info))
    print "该表特征维度"
    print "len(user_info[1])"+str(len(user_info[1]))#该表特征维度
    print "user_info[1]"
    print user_info[1]
    print user_info[5000]
    print user_info[5560]
    
    user_loantime={}
    for uid in range(len(sample_data_user_info)):
        user_loantime[uid+1]=[0]
    print "len(sample_data_loan_time_train)"+str(len(sample_data_loan_time_train))
    print "len(user_loantime)"+str(len(user_loantime))
    print user_loantime[1]#键最小
    print user_loantime[5000]#键最大
    print user_loantime[5560]#键最大
    for item in sample_data_loan_time:
        uid=item[0]
        user_loantime[uid][0]=item[1]
        
    print "len(user_loantime)"+str(len(user_loantime))
    print "该表特征维度"
    print "len(user_loantime[1])"+str(len(user_loantime[1]))#该表特征维度
    print "user_loantime[1]"
    print user_loantime[1]
    print user_loantime[5000]
    print user_loantime[5560]
    
    user_overdue={}
    for uid in range(len(sample_data_user_info)):
        user_overdue[uid+1]=[0]
    print "len(sample_data_overdue_train)"+str(len(sample_data_overdue_train))
    print "len(sample_data_overdue)"+str(len(sample_data_overdue))
    print user_overdue[1]#键最小
    print user_overdue[5000]#键最大
    print user_overdue[5560]#键最大
    for item in sample_data_overdue:
        uid=item[0]
        user_overdue[uid][0]=item[1]
        
    print "len(user_overdue)"+str(len(user_overdue))
    print "该表特征维度"
    print "len(user_overdue[1])"+str(len(user_overdue[1]))#该表特征维度
    print "user_overdue[1]"
    print user_overdue[1]
    print user_overdue[5000]
    print user_overdue[5560]
    
    
    print  "len(sdui_tr) "+ str(len(sdui_tr)) 
    
    print "len(sample_data_user_info)"+str(len(sample_data_user_info))
    user_bank = {}
    for uid in range(len(sample_data_user_info)):
        user_bank[uid+1]=[0]*17
    print "len(sample_data_bank_detail_train)"+str(len(sample_data_bank_detail_train))
    print "len(user_bank)"+str(len(user_bank))
    print user_bank[1]#键最小
    print user_bank[5000]#键最大
    print user_bank[5560]#键最大
    for item in sample_data_bank_detail:
        uid=int(item[0])
        #print uid
#        user_bank.setdefault(uid,[0]*17)
       
        user_bank[uid][0]+=1#总次数
       
        if int(item[2])==1:
            user_bank[uid][1]+=1#收入次数
            user_bank[uid][2]+=float(item[3])#收入总金额
            user_bank[uid][3]+=float(item[3])#净收入总金额
            user_bank[uid][15]=(user_bank[uid][15] if user_bank[uid][15]>float(item[3]) else float(item[3]))#收入最大金额
        if int(item[2])==0:
            user_bank[uid][4]+=1#支出次数
            user_bank[uid][5]+=float(item[3])#支出总金额
            user_bank[uid][3]-=float(item[3])#净收入总金额
            user_bank[uid][16]=(user_bank[uid][16] if user_bank[uid][16]>float(item[3]) else float(item[3]))#支出最大金额
        if int(item[4])==1:
            user_bank[uid][6]+=1#工资收入次数
             
    for uid in user_bank:
        user_bank[uid][7]=100*user_bank[uid][1]/(user_bank[uid][0]+1.0)#收入次数占比
        user_bank[uid][8]=100*user_bank[uid][4]/(user_bank[uid][0]+1.0)#支出次数占比
        user_bank[uid][9]=100*user_bank[uid][1]/(user_bank[uid][4]+1.0)#支出次数/收入次数
        user_bank[uid][10]=100*user_bank[uid][3]/(user_bank[uid][2]+1.0)#净收入/总收入  
        user_bank[uid][11]=100*user_bank[uid][5]/(user_bank[uid][2]+1.0)#总支出/总收入 
        user_bank[uid][12]=100*user_bank[uid][6]/(user_bank[uid][1]+1.0)#工资收入次数/总收入次数
        user_bank[uid][13]=user_bank[uid][2]/(user_bank[uid][1]+1.0)#收入平均金额
        user_bank[uid][14]=user_bank[uid][5]/(user_bank[uid][4]+1.0)#支出平均金额
        
    print "len(user_bank)"+str(len(user_bank))
    print "该表特征维度"
    print "len(user_bank[1])"+str(len(user_bank[1]))#该表特征维度
    print "user_bank[1]"
    print user_bank[1]
    print user_bank[5000]
    print user_bank[5560]
    
    user_browse=dict()
    for uid in range(len(sample_data_user_info)):
        user_browse.setdefault(uid+1,[0]*56)
    print "len(sample_data_browse_history_train)"+str(len(sample_data_browse_history_train))
    print "len(user_browse)"+str(len(user_browse))
    print user_browse[1]#键最小
    print user_browse[5000]#键最大
    print user_browse[5560]#键最大
    for item in sample_data_browse_history:
        uid=int(item[0])
        #user_browse.setdefault(uid,[0]*56)
        user_browse[uid][0]+=1#总次数
        user_browse[uid][int(item[3])]+=1#index1-11,各浏览子行为对应次数
        user_browse[uid][11+int(item[3])]+=int(item[2])#index12-22,各浏览子行为对应数据总和
        user_browse[uid][22+int(item[3])]=(user_browse[uid][22+int(item[3])] if user_browse[uid][22+int(item[3])]>item[2] else int(item[2]))#index23-33,各浏览子行为对应数据最大值
        
    for uid in user_browse:
        for i in range(11):
            user_browse[uid][33+i+1]=100*user_browse[uid][i+1]/(user_browse[uid][0]+1.0)#index34-44,各浏览子行为对应次数,占比
            user_browse[uid][44+i+1]=100*user_browse[uid][i+12]/(user_browse[uid][i+1]+1.0)#index45-55,各浏览子行为的平均数据
        
    print "len(user_browse)"+str(len(user_browse))
    print "该表特征维度"
    print "len(user_browse[2])"+str(len(user_browse[2]))#该表特征维度
    print user_browse[1]#键最小
    print user_browse[5000]#键最大
    print user_browse[5560]#键最大    
    
    user_bill=dict()
    for uid in range(len(sample_data_user_info)):
        user_bill.setdefault(uid+1,[0]*49)
    print "len(sample_data_bill_detail_train)"+str(len(sample_data_bill_detail_train))
    print "len(user_bill)"+str(len(user_bill))
    print user_bill[1]#键最小
    print user_bill[5000]#键最大
    print user_bill[5560]#键最大
    for item in sample_data_bill_detail:
        uid=int(item[0])
        user_bill.setdefault(uid,[0]*49)
        user_bill[uid][0]+=1
        #user_bill[uid][int(item[2])]+=1#index1-16,各银行的次数
        if int(item[2])<17:
            user_bill[uid][int(item[2])]+=1#index1-11,各浏览子行为对应次数
        
        user_bill[uid][17]+=(1 if int(float(item[3]))!=0 else 0)#上期账单金额非0次数
        user_bill[uid][18]+=float(item[3]) #上期账单金额非0总和
        
        user_bill[uid][19]+=(1 if int(float(item[4]))!=0 else 0)#上期还款金额非0次数
        user_bill[uid][20]+=float(item[4]) #上期还款金额非0总和 
        user_bill[uid][21]+=(0 if int(float(item[3]))==0 and int(float(item[4]))==0 else 1)#上期还款金额非0且账单金额非0次数
        user_bill[uid][22]+= float(item[4])-float(item[3])#上期（还款金额非0 - 账单金额非0 ）的总和
        user_bill[uid][23]+=(float(item[5]) if int(float(item[5]))!=0 else 0)#上期信用卡额度的总和
        user_bill[uid][24]+=(1 if int(float(item[6]))!=0 else 0)#本期发放账单余额额度的次数
        user_bill[uid][25]+=float(item[6]) #本期账单余额额度的总和
        user_bill[uid][26]+=(1 if int(float(item[7]))!=0 else 0)#本期账单余额余额的有效次数
        user_bill[uid][27]+=float(item[7]) #本期账单余额额度的总和
        user_bill[uid][28]+=float(item[8])#消费次数总和
        
        user_bill[uid][29]+=float(item[9])#本期账单金额总和，除以user_bill[uid][19]
        user_bill[uid][30]+=(1 if int(float(item[10]))!=0 else 0)#调整金额的有效次数
        user_bill[uid][31]+=float(item[10]) #本期账单调整金额的总和
        user_bill[uid][32]+=(1 if int(float(item[11]))!=0 else 0)#循环利息的有效次数
        user_bill[uid][33]+=float(item[11]) #循环利息的总和
        
        user_bill[uid][34]+=float(item[12])#可用余额总和，除以user_bill[uid][0]+=1
        
        user_bill[uid][35]+=(1 if int(float(item[13]))!=0 else 0)#预借现金额度的有效次数
        user_bill[uid][36]+=float(item[13]) #预借现金额度的总和
        
        user_bill[uid][37]+=float(item[14])#还款状态累计。
        
        
    
    for uid in user_bill:
        user_bill[uid][38]=user_bill[uid][18]/(user_bill[uid][17]+1.0)#上期账单金额非0平均
        user_bill[uid][39]=user_bill[uid][20]/(user_bill[uid][19]+1.0)#上期还款金额非0平均
        user_bill[uid][40]=user_bill[uid][22]/(user_bill[uid][21]+1.0)#上期（还款金额非0 - 账单金额非0 ）的平均
        user_bill[uid][41]=user_bill[uid][23]/(user_bill[uid][21]+1.0)#上期信用卡金额非0平均
        user_bill[uid][42]=user_bill[uid][25]/(user_bill[uid][24]+1.0)#本期账单金额非0平均
        user_bill[uid][43]=user_bill[uid][27]/(user_bill[uid][26]+1.0)#本期账单余额非0平均
        user_bill[uid][44]=user_bill[uid][29]/(user_bill[uid][19]+1.0)#本期账单金额平均
        user_bill[uid][45]=user_bill[uid][31]/(user_bill[uid][30]+1.0)#调整金额平均
        user_bill[uid][46]=user_bill[uid][33]/(user_bill[uid][32]+1.0)#循环利息平均
        user_bill[uid][47]=user_bill[uid][34]/(user_bill[uid][0]+1.0)#可用余额平均
        user_bill[uid][48]=user_bill[uid][36]/(user_bill[uid][35]+1.0)#可用余额平均
    print "len(user_bill)"+str(len(user_bill))
    print "该表特征维度"
    print "len(user_bill[2])"+str(len(user_bill[2]))#该表特征维度
    print user_bill[1]#键最小
    print user_bill[5000]#键最大
    print user_bill[5560]#键最大


    
    print  "len(user_bank)"+str(len(user_bank))
    print  "len(user_bill)"+str(len(user_bill))
    print  "len(user_browse)"+str(len(user_browse))
    print  "len(sdui_tr)"+str(len(sdui_tr))
    print  "len(sdlt_tr)"+str(len(sdlt_tr))
    print  "len(sdo_tr)"+str(len(sdo_tr))
    print "len(sample_data_user_info_train)"+str(len(sample_data_user_info_train))
    print sdui_tr[0]
    
    
    print sdui_tr[0][1:]+user_bank[1]+user_bill[1]+user_browse[1]
    print user_bank[5000]
    print type(user_bank[5000])
    print sdui_tr[4999][1:]+user_bank[5000]+user_bill[5000]+user_browse[5000]
    print type(sdui_tr[4999][1:]+user_bank[5000]+user_bill[5000]+user_browse[5000])
    small_train_data=[]
   
    print sdui_tr[1]
    print sdui_tr[1][1:]
    print sdlt_tr[1]
    print sdlt_tr[1][1:]

    for i in range(len(sample_data_user_info_train)):
        
        
        small_train_data.append(user_info[i+1][1:]+user_bank[i+1]+user_bill[i+1]+user_browse[i+1])
        small_train_target.append(user_overdue[i+1])
    print "len(small_train_data)"+str(len(small_train_data))
   
    print small_train_data[0]
    print small_train_target[0]
    print small_train_data[4999]
    print small_train_target[4999]
    print  "len(sdui_te)"+str(len(sdui_te))
    print  "len(sdlt_te)"+str(len(sdlt_te))
    print  "len(sdo_te)"+str(len(sdo_te))
    
    
    print "len(sample_data_user_info_test)"+str(len(sample_data_user_info_test))
    for i in range(len(sample_data_user_info_test)):
        
        #small_test_data.append(user_info[i+5001]+ user_loantime[i+5001]+user_bank[i+5001]+user_bill[i+5001]+user_browse[i+5001])
        small_test_data.append(user_info[i+5001][1:]+user_bank[i+5001]+user_bill[i+5001]+user_browse[i+5001])
        small_test_target_true.append(user_overdue[i+5001])
    print "len(small_test_data)"+str(len(small_test_data))
     

    
    print small_test_data[0]#small_test_data[0]对应uid为[5000]
    print small_test_target_true[0]#small_test_data[0]对应uid为5000
    print small_test_data[559]#small_test_data[559]对应uid为5560
    print small_test_target_true[559]#small_test_data[559]对应uid为5560
   
    f = file('small_train_data.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(small_train_data)
    f = file('small_train_target.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(small_train_target)
    f = file('small_test_data.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(small_test_data)
    f = file('small_test_target_true.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(small_test_target_true)
    
    small_train_data_scaled=preprocessing.scale(small_train_data)#对列表的列表可以
    small_test_data_scaled=preprocessing.scale(small_test_data)#对列表的列表可以
    f = file('small_train_data_scaled.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(small_train_data_scaled)
    f = file('small_test_data_scaled.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(small_test_data_scaled)
    

   
def predict_pseudo_test():
    
    train_X = pd.read_csv('E:/DC_BIG_data/loan/small_train_data_scaled.csv',header = None)
    train_y= pd.read_csv('E:/DC_BIG_data/loan/small_train_target.csv',header = None)
    test_X = pd.read_csv('E:/DC_BIG_data/loan/small_test_data_scaled.csv',header = None)
    test_y_true= pd.read_csv('E:/DC_BIG_data/loan/small_test_target_true.csv',header = None)
    lr_model=LogisticRegression(C=1.0,penalty='l2')
    lr_model.fit(train_X,train_y)
    test_y_predict=lr_model.predict(test_X)
    print classification_report(test_y_true,test_y_predict)
    predict_prob=lr_model.predict_proba(test_X)
    result=pd.DataFrame(predict_prob)
    result.to_csv("result_small.csv")
    

    
def split_sample(data):
    pos=[]
    neg=[]
    for item in data:
        if item[-1]==1:
            pos.append(item)
        if item[-1]==0:
            neg.append(item)
    return pos,neg



if __name__=='__main__':
    #read_sample()
    predict_pseudo_test()

