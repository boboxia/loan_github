# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 19:34:27 2016

@author: Administrator
"""

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import preprocessing


train = pd.read_csv('./processed_pd/loan_data_train.csv')

train.index=train['userid']
train.drop('userid',axis=1,inplace=True)
print train.head(1)
train_scaled=preprocessing.scale(train)#对列表的列表可以
print train_scaled

train_target = pd.read_csv('./processed_pd/loan_data_train_target.csv')
train_target.index=train_target['userid']
train_target.drop('userid',axis=1,inplace=True)
#print train_target.head(5)

train_X,test_X,train_y,test_y=train_test_split(train_scaled,train_target,test_size=0.1,random_state=0)
train_y=train_y['label']
test_y=test_y['label']
lr_model=LogisticRegression(C=1.0,penalty='l2')
lr_model.fit(train_X,train_y)
#给出交叉验证集的预测结果，评估准确率，召回率，F1值。
pred_test=lr_model.predict(test_X)
##有一个报告。
print classification_report(test_y,pred_test)

##真正的预测结果。
test = pd.read_csv('./processed_pd/loan_data_test.csv')
test.index=test['userid']
test.drop('userid',axis=1,inplace=True)
print test.head(1)
test_scaled=preprocessing.scale(test)#对列表的列表可以
print test_scaled

pred=lr_model.predict_proba(test_scaled)
result=pd.DataFrame(pred)

result.index=test.index
result.columns=['0','probability']
result.drop('0',axis=1,inplace=True)
print result.head(5)

result.to_csv('result.csv')

