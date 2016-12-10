# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 09:18:24 2016

@author: Administrator
"""

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# user_info
#user_info_train=pd.read_csv('./train/small10/loan_small_user_info_train.csv',header=None)
user_info_train=pd.read_csv('./train/user_info_train.txt',header=None)
user_info_test=pd.read_csv('./test/user_info_test.csv',header=None)

col_names=['userid','sex','occupation','education','marriage','household']
user_info_train.columns=col_names
user_info_test.columns=col_names

#合并train,test
user_info=pd.concat([user_info_train,user_info_test])
#将userid设置为数据集的index,并删除之前的userid所在列
user_info.index=user_info['userid']
user_info.drop('userid',axis=1,inplace=True)

print user_info.head(5)


# 下面的处理方式类似，我仅注释不同的地方
# bank_detail
#bank_detail_train = pd.read_csv('./train/small10/loan_small_bank_detail_train.csv',header = None)
bank_detail_train = pd.read_csv('./train/bank_detail_train.txt',header = None)
bank_detail_test = pd.read_csv('./test/bank_detail_test.csv',header = None)
col_names = ['userid', 'tm_encode', 'trade_type', 'trade_amount', 'salary_tag']
bank_detail_train.columns = col_names
bank_detail_test.columns = col_names
bank_detail = pd.concat([bank_detail_train, bank_detail_test])
#在该数据集中，一个用户是有多条记录的，这里采用对每个用户每种交易类型去均值进行聚合
bank_detail_n=(bank_detail.loc[:,['userid','trade_type','trade_amount','tm_encode']]).groupby(['userid','trade_type']).mean()
bank_detail_n=bank_detail_n.unstack()
bank_detail_n.columns=['income','outcome','income_tm','outcome_tm']
print bank_detail_n.head(5)

# browse_history
#browse_history_train = pd.read_csv('./train/small10/loan_small_browse_history_train.txt',\
#                                       header = None)
browse_history_train = pd.read_csv('./train/browse_history_train.txt',header = None)
                                       
browse_history_test = pd.read_csv('./test/browse_history_test.txt',\
                                       header = None)
col_names = ['userid', 'tm_encode_2', 'browse_data', 'browse_tag']
browse_history_train.columns = col_names
browse_history_test.columns = col_names
browse_history = pd.concat([browse_history_train, browse_history_test])
# 这里采用计算每个用户总浏览行为次数进行聚合
browse_history_count = browse_history.loc[:, ['userid', 'browse_data']].groupby(['userid']).sum()
##这个地方为什么在此时没有像bank_detail一样进行unstack的处理呢？？

print browse_history_count.head(5)

# bill_detail
#bill_detail_train = pd.read_csv('./train/small10/loan_small_bill_detail_train.txt',\
#                                       header = None)
bill_detail_train = pd.read_csv('./train/bill_detail_train.txt',\
                                       header = None)                                       
bill_detail_test = pd.read_csv('./test/bill_detail_test.txt',\
                                       header = None)
col_names = ['userid', 'tm_encode_3', 'bank_id', 'prior_account', 'prior_repay',
             'credit_limit', 'account_balance', 'minimun_repay', 'consume_count',
             'account', 'adjust_account', 'circulated_interest', 'avaliable_balance',
             'cash_limit', 'repay_state']
bill_detail_train.columns = col_names
bill_detail_test.columns = col_names
bill_detail = pd.concat([bill_detail_train, bill_detail_test])

bill_detail_mean = bill_detail.groupby(['userid']).mean()
bill_detail_mean.drop('bank_id',
                      axis = 1,
                      inplace = True)
print bill_detail_mean.head(5)

# loan_time
#loan_time_train = pd.read_csv('./train/small10/loan_small_loan_time_train.txt',
#                              header = None)
loan_time_train = pd.read_csv('./train/loan_time_train.txt',
                              header = None)                              
loan_time_test = pd.read_csv('./test/loan_time_test.txt',
                              header = None)
loan_time = pd.concat([loan_time_train, loan_time_test])
loan_time.columns = ['userid', 'loan_time']
loan_time.index = loan_time['userid']
loan_time.drop('userid',
               axis = 1,
               inplace = True)
print loan_time.head(5)


##分别处理完各个表的数据后，根据userid进行join,方式为“outer”,没有bill或者bank的数据的user在对应字段上将为Na值。
loan_data=user_info.join(bank_detail_n,how='outer')
loan_data=loan_data.join(bill_detail_mean,how="outer")
loan_data=loan_data.join(browse_history_count,how="outer")
loan_data=loan_data.join(loan_time,how="outer")

##这里是直接填补缺失值为（0.0），难道就可以了吗？？
loan_data=loan_data.fillna(0.0)
print loan_data.head(5)


##构造新的特征，（这里应该很多特征待构造的）
loan_data['time']=loan_data['loan_time']-loan_data['tm_encode_3']
print loan_data.head(5)

#对性别，职业，等因子变量，需要对他们构造出哑变量。
category_col=['sex','occupation','education','marriage','household']
def set_dummies(data,colname):
    for col in colname:
        data[col]=data[col].astype('category')
        dummy=pd.get_dummies(data[col])
        dummy=dummy.add_prefix('{}#'.format(col))
        data.drop(col,axis=1,inplace=True)
        data=data.join(dummy)
    return data
loan_data=set_dummies(loan_data,category_col)
print loan_data.head(5)

# overdue_train，这是我们模型所要拟合的目标
#target = pd.read_csv('./train/small10/loan_small_overdue_train.txt',header = None)
target = pd.read_csv('./train/overdue_train.txt',header = None)

target.columns=['userid','label']
target.index=target['userid']
target.drop('userid',axis=1,inplace=True)
print target.head(5)

#构建模型
#分开训练集，测试集
#train=loan_data.iloc[0:5560,:]
#test=loan_data.iloc[5560:,:]
train=loan_data.iloc[0:55596,:]
test=loan_data.iloc[55596:,:]
print train.head(5)
print train.tail(5)
print test.head(5)
print test.tail(5)

##避免过拟合，采用的是交叉验证，验证集级占20%，固定随机种子。
train_X,test_X,train_y,test_y=train_test_split(train,target,test_size=0.2,random_state=0)
train_y=train_y['label']
test_y=test_y['label']
lr_model=LogisticRegression(C=2.0,penalty='l2')
lr_model.fit(train_X,train_y)
#给出交叉验证集的预测结果，评估准确率，召回率，F1值。
pred_test=lr_model.predict(test_X)
##有一个报告。
print classification_report(test_y,pred_test)

##真正的预测结果。
pred=lr_model.predict_proba(test)
result=pd.DataFrame(pred)
result.index=test.index
result.columns=['0','probability']
result.drop('0',axis=1,inplace=True)
print result.head(5)

result.to_csv('result.csv')
##end!
'''
'''