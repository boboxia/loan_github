# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:53:36 2016

@author: Administrator
"""

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import time
from sklearn import preprocessing
# 特征工程
# 下面分别对user_info, bank_detail, browse_data, bill_detail, loan_data进行预处理

# user_info
# 读取数据集
time1=time.time()
'''
user_info_train = pd.read_csv('./train/small10/loan_small_user_info_train.csv',
                                  header = None)
user_info_test = pd.read_csv('./test/user_info_test.csv',
                                 header = None)
bank_detail_train = pd.read_csv('./train/small10/loan_small_bank_detail_train.csv',
                                    header = None)
bank_detail_test = pd.read_csv('./test/bank_detail_test.csv',
                                    header = None)
browse_history_train = pd.read_csv('./train/small10/loan_small_browse_history_train.csv',
                                       header = None)
browse_history_test = pd.read_csv('./test/browse_history_test.csv',
                                       header = None)
bill_detail_train = pd.read_csv('./train/small10/loan_small_bill_detail_train.csv',
                                       header = None)
bill_detail_test = pd.read_csv('./test/bill_detail_test.csv',
                                       header = None)
loan_time_train = pd.read_csv('./train/small10/loan_small_loan_time_train.csv',
                              header = None)
loan_time_test = pd.read_csv('./test/loan_time_test.csv',
                              header = None)

'''
user_info_train = pd.read_csv('./train/user_info_train.csv',
                                  header = None)
user_info_test = pd.read_csv('./test/user_info_test.csv',
                                 header = None)
bank_detail_train = pd.read_csv('./train/bank_detail_train.csv',
                                    header = None)
bank_detail_test = pd.read_csv('./test/bank_detail_test.csv',
                                    header = None)
browse_history_train = pd.read_csv('./train/browse_history_train.csv',
                                       header = None)
browse_history_test = pd.read_csv('./test/browse_history_test.csv',
                                       header = None)
bill_detail_train = pd.read_csv('./train/bill_detail_train.csv',
                                       header = None)
bill_detail_test = pd.read_csv('./test/bill_detail_test.csv',
                                       header = None)
loan_time_train = pd.read_csv('./train/loan_time_train.csv',
                              header = None)
loan_time_test = pd.read_csv('./test/loan_time_test.csv',
                              header = None)
time2=time.time()
print time2-time1
                        
# 设置字段（列）名称
col_names = ['userid', 'sex', 'occupation', 'education', 'marriage', 'household']
user_info_train.columns = col_names
user_info_test.columns = col_names
# 合并train、test
user_info = pd.concat([user_info_train, user_info_test])
# 将userid（用户id）设置为数据集的index，并删除原userid所在列
user_info.index = user_info['userid']
user_info.drop('userid',
                axis = 1,
                inplace = True)
# 查看处理后的数据集，输出前5行
print user_info.head(5)

# 下面的处理方式类似，我仅注释不同的地方
# bank_detail
#bank_detail_train = pd.read_csv('D:/data/DataCastle/train/bank_detail_train.txt',
                                    #header = None)
#bank_detail_test = pd.read_csv('D:/data/DataCastle/test/bank_detail_test.txt',
                                    #header = None)

col_names = ['bk_userid', 'bk_tm_encode', 'bk_trade_type', 'bk_trade_amount', 'bk_salary_tag']
bank_detail_train.columns = col_names
bank_detail_test.columns = col_names
bank_detail = pd.concat([bank_detail_train, bank_detail_test])
print "bank_detail.head(5)"
print bank_detail.head(5)
# 在该数据集中，一个用户对应多条记录，这里我们采用对每个用户每种交易类型取均值进行聚合

bank_detail_n = (bank_detail.loc[:, ['bk_userid', 'bk_trade_type', 'bk_trade_amount', 'bk_tm_encode']]).groupby(['bk_userid', 'bk_trade_type']).mean()
# 重塑数据集，并设置字段（列）名称
#print bank_detail_n.head(5)
bank_detail_n = bank_detail_n.unstack()
bank_detail_n.columns = ['bk_income', 'bk_outcome', 'bk_income_tm', 'bk_outcome_tm']
#print "detail_n"
#print bank_detail_n.head(5)

bank_detail_times = (bank_detail.loc[:, ['bk_userid',  'bk_trade_type']]).groupby('bk_userid').count()
#print "bank_detail_times(5)"
#print bank_detail_times
bank_detail_times.columns = ['bk_alltimes']
#print bank_detail_times

bank_detail_processed= bank_detail_n.join(bank_detail_times, how = 'outer')
#print "bank_detail_processed"
#print bank_detail_processed

bank_detail_trade_type_time = (bank_detail.loc[:, ['bk_userid', 'bk_trade_type', 'bk_trade_amount' ]]).groupby(['bk_userid', 'bk_trade_type']).count()
# 重塑数据集，并设置字段（列）名称
#print bank_detail_trade_type_time.head(5)
bank_detail_trade_type_time = bank_detail_trade_type_time.unstack()
bank_detail_trade_type_time.columns = ['bk_type0times', 'bk_type1times']
#print "after unstack"
#print bank_detail_trade_type_time.head(5)
bank_detail_processed= bank_detail_processed.join(bank_detail_trade_type_time, how = 'outer')

bank_detail_trade_type_amount = (bank_detail.loc[:, ['bk_userid', 'bk_trade_type', 'bk_trade_amount' ]]).groupby(['bk_userid', 'bk_trade_type']).sum()
# 重塑数据集，并设置字段（列）名称
#print bank_detail_trade_type_amount.head(5)
bank_detail_trade_type_amount = bank_detail_trade_type_amount.unstack()
bank_detail_trade_type_amount.columns = ['bk_type0amount', 'bk_type1amount']
#print "after unstack"
#print bank_detail_trade_type_amount.head(5)
bank_detail_processed= bank_detail_processed.join(bank_detail_trade_type_amount, how = 'outer')

bank_detail_from_salary_time = (bank_detail.loc[:, ['bk_userid', 'bk_salary_tag', 'bk_trade_amount' ]]).groupby(['bk_userid', 'bk_salary_tag']).count()
# 重塑数据集，并设置字段（列）名称
#print bank_detail_from_salary_time.head(20)
bank_detail_from_salary_time = bank_detail_from_salary_time.unstack()
bank_detail_from_salary_time.columns = ['bk_notfromsalarytimes', 'bk_fromsalarytimes']
#print "after unstack"
#print bank_detail_from_salary_time.head(20)
bank_detail_processed= bank_detail_processed.join(bank_detail_from_salary_time, how = 'outer')

bank_detail_trade_type_max = (bank_detail.loc[:, ['bk_userid', 'bk_trade_type', 'bk_trade_amount' ]]).groupby(['bk_userid', 'bk_trade_type']).max()
# 重塑数据集，并设置字段（列）名称
#print bank_detail_trade_type_max.head(5)
bank_detail_trade_type_max = bank_detail_trade_type_max.unstack()
bank_detail_trade_type_max.columns = ['bk_outcome_max', 'bk_income_max']
#print "after unstack"
#print bank_detail_trade_type_max.head(5)
bank_detail_processed= bank_detail_processed.join(bank_detail_trade_type_max, how = 'outer')
#bank_detail_processed= bank_detail_n.join(bank_detail_n, how = 'outer')
bank_detail_processed = bank_detail_processed.fillna(0.0)
#print bank_detail_processed

bank_detail_processed['bk_income_times_ratio']=100*bank_detail_processed['bk_type1times']/(bank_detail_processed["bk_alltimes"]+1)
bank_detail_processed['bk_outcome_times_ratio']=100*bank_detail_processed['bk_type0times']/(bank_detail_processed["bk_alltimes"]+1)
bank_detail_processed['bk_income_times_out_times_ratio']=100*bank_detail_processed['bk_type1times']/(bank_detail_processed['bk_type0times']+1)
bank_detail_processed['bk_net_income']=bank_detail_processed['bk_type1amount']-bank_detail_processed["bk_type0amount"]
bank_detail_processed['bk_net_income_income_ratio']=100*bank_detail_processed['bk_net_income']/(bank_detail_processed["bk_type1amount"]+1)
bank_detail_processed['bk_outcome_income_ratio']=100*bank_detail_processed['bk_type0amount']/(bank_detail_processed["bk_type1amount"]+1)
bank_detail_processed['bk_isfromsalary_alltimes_ratio']=100*bank_detail_processed['bk_fromsalarytimes']/(bank_detail_processed["bk_alltimes"]+1)
bank_detail_processed['bk_avg_income']=bank_detail_processed['bk_type1amount']/(bank_detail_processed["bk_type1times"]+1)
bank_detail_processed['bk_avg_outcome']=bank_detail_processed['bk_type0amount']/(bank_detail_processed["bk_type0times"]+1)
print bank_detail_processed

# browse_history
#browse_history_train = pd.read_csv('D:/data/DataCastle/train/browse_history_train.txt',
#                                       header = None)
#browse_history_test = pd.read_csv('D:/data/DataCastle/test/browse_history_test.txt',
#                                       header = None)
col_names = ['bw_userid', 'bw_tm_encode_2', 'bw_browse_data', 'bw_browse_tag']
browse_history_train.columns = col_names
browse_history_test.columns = col_names
browse_history = pd.concat([browse_history_train, browse_history_test])
# 这里采用计算每个用户总浏览行为次数进行聚合

browse_history_sum = browse_history.loc[:, ['bw_userid', 'bw_browse_data']].groupby(['bw_userid']).sum()
#print browse_history_count.head(5)
browse_history_sum.columns=['bw_datasum']

browse_history_times = (browse_history.loc[:, ['bw_userid',  'bw_browse_data']]).groupby('bw_userid').count()
#print "bank_detail_times(5)"
#print bank_detail_times
browse_history_times.columns = ['bw_alltimes']
#print browse_history_times
browse_history_processed= browse_history_sum.join(browse_history_times, how = 'outer')

browse_history_browse_type_time = (browse_history.loc[:, ['bw_userid', 'bw_browse_tag', 'bw_browse_data' ]]).groupby(['bw_userid', 'bw_browse_tag']).count()
# 重塑数据集，并设置字段（列）名称
#print browse_history_browse_type_time.head(10)
browse_history_browse_type_time = browse_history_browse_type_time.unstack()
browse_history_browse_type_time.columns = ['bw_1times', 'bw_2times','bw_3times','bw_4times','bw_5times','bw_6times','bw_7times','bw_8times','bw_9times','bw_10times','bw_11times']
#print "after unstack"
#print browse_history_browse_type_time.head(5)
browse_history_processed= browse_history_processed.join(browse_history_browse_type_time, how = 'outer')

browse_history_browse_type_datasum = (browse_history.loc[:, ['bw_userid', 'bw_browse_tag', 'bw_browse_data' ]]).groupby(['bw_userid', 'bw_browse_tag']).sum()
# 重塑数据集，并设置字段（列）名称
#print browse_history_browse_type_datasum.head(10)
browse_history_browse_type_datasum = browse_history_browse_type_datasum.unstack()
browse_history_browse_type_datasum.columns = ['bw_1datasum', 'bw_2datasum','bw_3datasum','bw_4datasum','bw_5datasum','bw_6datasum','bw_7datasum','bw_8datasum','bw_9datasum','bw_10datasum','bw_11datasum']
#print "after unstack"
#print browse_history_browse_type_datasum.head(5)
browse_history_processed= browse_history_processed.join(browse_history_browse_type_datasum, how = 'outer')

browse_history_browse_type_datamax = (browse_history.loc[:, ['bw_userid', 'bw_browse_tag', 'bw_browse_data' ]]).groupby(['bw_userid', 'bw_browse_tag']).max()
# 重塑数据集，并设置字段（列）名称
#print browse_history_browse_type_datamax.head(10)
browse_history_browse_type_datamax = browse_history_browse_type_datamax.unstack()
browse_history_browse_type_datamax.columns = ['bw_1datamax', 'bw_2datamax','bw_3datamax','bw_4datamax','bw_5datamax','bw_6datamax','bw_7datamax','bw_8datamax','bw_9datamax','bw_10datamax','bw_11datamax']
#print "after unstack"
#print browse_history_browse_type_datamax.head(5)
browse_history_processed= browse_history_processed.join(browse_history_browse_type_datamax, how = 'outer')
browse_history_processed = browse_history_processed.fillna(0.0)
for i in range(1,12):
    tempcolumn1="bw_"+str(i)+"times_ratio"
    usecolumn1="bw_"+str(i)+"times"
    tempcolumn2="bw_"+str(i)+"avgdata"
    usecolumn2="bw_"+str(i)+"datasum"
    
    browse_history_processed[tempcolumn1]=100*browse_history_processed[usecolumn1]/(browse_history_processed["bw_alltimes"]+1)
    browse_history_processed[tempcolumn2]=browse_history_processed[usecolumn2]/(browse_history_processed[usecolumn1]+1)
print browse_history_processed


# bill_detail
#bill_detail_train = pd.read_csv('D:/data/DataCastle/train/bill_detail_train.txt',
#                                       header = None)
#bill_detail_test = pd.read_csv('D:/data/DataCastle/test/bill_detail_test.txt',
#                                       header = None)
col_names = ['bi_userid', 'bi_tm_encode_3', 'bi_bank_id', 'bi_prior_account', 'bi_prior_repay',
             'bi_credit_limit', 'bi_account_balance', 'bi_minimun_repay', 'bi_consume_count',
             'bi_account', 'bi_adjust_account', 'bi_circulated_interest', 'bi_avaliable_balance',
             'bi_cash_limit', 'bi_repay_state']
bill_detail_train.columns = col_names
bill_detail_test.columns = col_names
bill_detail = pd.concat([bill_detail_train, bill_detail_test])

bill_detail_mean = bill_detail.groupby(['bi_userid']).mean()
bill_detail_mean.drop('bi_bank_id',axis = 1,inplace = True)
#print bill_detail_mean.head(5)



bill_detail_times = (bill_detail.loc[:, ['bi_userid',  'bi_tm_encode_3']]).groupby('bi_userid').count()
#print "bill_detail_times(5)"
#print bill_detail_times(5)
bill_detail_times.columns = ['bi_alltimes']
#print bill_detail_times.head(5)
bill_detail_processed= bill_detail_mean.join(bill_detail_times, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_bank_id",'bi_tm_encode_3']]
bill_detail_times_bk_notzero = bill_detail_temp[bill_detail_temp.bi_bank_id<17].groupby(['bi_userid','bi_bank_id']).count()
#bill_detail_times_bk_notzero.columns = ['alltimes_bk_notzero']
bill_detail_times_bk_notzero = bill_detail_times_bk_notzero.unstack()
bill_detail_times_bk_notzero.columns = ['bi_1bank_id', "bi_2bank_id",'bi_3bank_id', "bi_4bank_id",'bi_5bank_id', "bi_6bank_id",'bi_7bank_id', "bi_8bank_id",'bi_9bank_id', "bi_10bank_id",'bi_11bank_id', "bi_12bank_id",'bi_13bank_id', "bi_14bank_id",'bi_15bank_id', "bi_16bank_id"]
#print "after unstack"
#print bill_detail_times_bk_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_bk_notzero, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_prior_account"]]
bill_detail_times_pa_notzero = bill_detail_temp[bill_detail_temp.bi_prior_account!=0].groupby('bi_userid').count()
bill_detail_times_pa_notzero.columns = ['bi_alltimes_pa_notzero']
#print bill_detail_times_pa_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_pa_notzero, how = 'outer')

bill_detail_prior_account_sum = bill_detail_temp[bill_detail_temp.bi_prior_account!=0].groupby('bi_userid').sum()
bill_detail_prior_account_sum.columns = ['bi_prior_account_sum']
#print bill_detail_prior_account_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_prior_account_sum, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_prior_repay"]]
bill_detail_times_pr_notzero = bill_detail_temp[bill_detail_temp.bi_prior_repay!=0].groupby('bi_userid').count()
bill_detail_times_pr_notzero.columns = ['bi_alltimes_pr_notzero']
#print bill_detail_times_pr_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_pr_notzero, how = 'outer')

bill_detail_prior_repay_sum = bill_detail_temp[bill_detail_temp.bi_prior_repay!=0].groupby('bi_userid').sum()
bill_detail_prior_repay_sum.columns = ['bi_prior_repay_sum']
#print bill_detail_prior_repay_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_prior_repay_sum, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_credit_limit"]]
bill_detail_credit_limit_sum = bill_detail_temp[bill_detail_temp.bi_credit_limit!=0].groupby('bi_userid').sum()
bill_detail_credit_limit_sum.columns = ['bi_credit_limit_sum']
#print bill_detail_credit_limit_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_credit_limit_sum, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_account_balance"]]
bill_detail_times_ab_notzero = bill_detail_temp[bill_detail_temp.bi_account_balance!=0].groupby('bi_userid').count()
bill_detail_times_ab_notzero.columns = ['bi_alltimes_ab_notzero']
#print bill_detail_times_ab_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_ab_notzero, how = 'outer')

bill_detail_account_balance_sum = bill_detail_temp[bill_detail_temp.bi_account_balance!=0].groupby('bi_userid').sum()
bill_detail_account_balance_sum.columns = ['bi_account_balance_sum']
#print bill_detail_account_balance_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_account_balance_sum, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_minimun_repay"]]
bill_detail_times_mr_notzero = bill_detail_temp[bill_detail_temp.bi_minimun_repay!=0].groupby('bi_userid').count()
bill_detail_times_mr_notzero.columns = ['bi_alltimes_mr_notzero']
#print bill_detail_times_mr_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_mr_notzero, how = 'outer')

bill_detail_minimun_repay_sum = bill_detail_temp[bill_detail_temp.bi_minimun_repay!=0].groupby('bi_userid').sum()
bill_detail_minimun_repay_sum.columns = ['bi_minimun_repay_sum']
#print bill_detail_minimun_repay_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_minimun_repay_sum, how = 'outer')

bill_detail_consume_times_sum = (bill_detail.loc[:, ['bi_userid',  'bi_consume_count']]).groupby('bi_userid').sum()
bill_detail_consume_times_sum.columns = ['bi_consume_times_sum']
#print bill_detail_consume_times_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_consume_times_sum, how = 'outer')

bill_detail_account_sum = (bill_detail.loc[:, ['bi_userid',  'bi_account']]).groupby('bi_userid').sum()
bill_detail_account_sum.columns = ['bi_account_sum']
#print bill_detail_account_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_account_sum, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_adjust_account"]]
bill_detail_times_aa_notzero = bill_detail_temp[bill_detail_temp.bi_adjust_account!=0].groupby('bi_userid').count()
bill_detail_times_aa_notzero.columns = ['bi_alltimes_aa_notzero']
#print bill_detail_times_aa_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_aa_notzero, how = 'outer')

bill_detail_adjust_account_sum = bill_detail_temp[bill_detail_temp.bi_adjust_account!=0].groupby('bi_userid').sum()
bill_detail_adjust_account_sum.columns = ['bi_adjust_account_sum']
#print bill_detail_adjust_account_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_adjust_account_sum, how = 'outer')

bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_circulated_interest"]]
bill_detail_times_ci_notzero = bill_detail_temp[bill_detail_temp.bi_circulated_interest!=0].groupby('bi_userid').count()
bill_detail_times_ci_notzero.columns = ['bi_alltimes_ci_notzero']
#print bill_detail_times_ci_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_ci_notzero, how = 'outer')

bill_detail_circulated_interest_sum = bill_detail_temp[bill_detail_temp.bi_circulated_interest!=0].groupby('bi_userid').sum()
bill_detail_circulated_interest_sum.columns = ['bi_circulated_interest_sum']
#print bill_detail_circulated_interest_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_circulated_interest_sum, how = 'outer')


bill_detail_avaliable_balance_sum = (bill_detail.loc[:, ['bi_userid',  'bi_avaliable_balance']]).groupby('bi_userid').sum()
bill_detail_avaliable_balance_sum.columns = ['bi_avaliable_balance_sum']
#print bill_detail_avaliable_balance_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_avaliable_balance_sum, how = 'outer')



bill_detail_temp=bill_detail.loc[:, ['bi_userid',  "bi_cash_limit"]]
bill_detail_times_cl_notzero = bill_detail_temp[bill_detail_temp.bi_cash_limit!=0].groupby('bi_userid').count()
bill_detail_times_cl_notzero.columns = ['bi_alltimes_cl_notzero']
#print bill_detail_times_cl_notzero.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_times_cl_notzero, how = 'outer')

bill_detail_cash_limit_sum = bill_detail_temp[bill_detail_temp.bi_cash_limit!=0].groupby('bi_userid').sum()
bill_detail_cash_limit_sum.columns = ['bi_cash_limit_sum']
#print bill_detail_cash_limit_sum.head(5)
bill_detail_processed= bill_detail_processed.join(bill_detail_cash_limit_sum, how = 'outer')

bill_detail_repay_state_sum = (bill_detail.loc[:, ['bi_userid',  'bi_repay_state']]).groupby('bi_userid').sum()
bill_detail_repay_state_sum.columns = ['bi_repay_state_sum']
#print bill_detail_repay_state_sum.head(250)
bill_detail_processed= bill_detail_processed.join(bill_detail_repay_state_sum, how = 'outer')
bill_detail_processed = bill_detail_processed.fillna(0.0)

bill_detail_processed["bi_prior_account_avg"]=bill_detail_processed["bi_prior_account_sum"]/(bill_detail_processed["bi_alltimes_pa_notzero"]+1)
bill_detail_processed["bi_prior_repay_avg"]=bill_detail_processed["bi_prior_repay_sum"]/(bill_detail_processed["bi_alltimes_pr_notzero"]+1)
bill_detail_processed["bi_account_balance_avg"]=bill_detail_processed["bi_account_balance_sum"]/(bill_detail_processed["bi_alltimes_ab_notzero"]+1)
bill_detail_processed["bi_minimun_repay_avg"]=bill_detail_processed["bi_minimun_repay_sum"]/(bill_detail_processed["bi_alltimes_mr_notzero"]+1)
bill_detail_processed["bi_adjust_account_avg"]=bill_detail_processed["bi_adjust_account_sum"]/(bill_detail_processed["bi_alltimes_aa_notzero"]+1)
bill_detail_processed["bi_circulated_interest_avg"]=bill_detail_processed["bi_prior_account_sum"]/(bill_detail_processed["bi_alltimes_ci_notzero"]+1)
bill_detail_processed["bi_cash_limit_avg"]=bill_detail_processed["bi_cash_limit_sum"]/(bill_detail_processed["bi_alltimes_cl_notzero"]+1)
bill_detail_processed["bi_avaliable_balance_avg"]=bill_detail_processed["bi_avaliable_balance_sum"]/(bill_detail_processed["bi_alltimes"]+1)
bill_detail_processed["bi_account_avg"]=bill_detail_processed["bi_account_sum"]/(bill_detail_processed["bi_alltimes"]+1)
bill_detail_processed["bi_prior_net_sum"]=bill_detail_processed["bi_prior_repay_sum"]-bill_detail_processed["bi_prior_account_sum"]
bill_detail_processed["bi_prior_net_avg"]=bill_detail_processed["bi_prior_net_sum"]/(bill_detail_processed["bi_alltimes_pa_notzero"]+1)

print bill_detail_processed



# loan_time
#loan_time_train = pd.read_csv('D:/data/DataCastle/train/loan_time_train.txt',
#                              header = None)
#loan_time_test = pd.read_csv('D:/data/DataCastle/test/loan_time_test.txt',
#                              header = None)
loan_time = pd.concat([loan_time_train, loan_time_test])
loan_time.columns = ['userid', 'loan_time']
loan_time.index = loan_time['userid']
loan_time.drop('userid',axis = 1,inplace = True)
print loan_time.head(5)


loan_data=user_info.join(bank_detail_processed, how = 'outer')
loan_data=loan_data.join(bill_detail_processed, how = 'outer')
loan_data=loan_data.join(browse_history_processed, how = 'outer')
#loan_data = loan_data.join(loan_time, how = 'outer')

loan_data = loan_data.fillna(0.0)


#loan_data['time'] = loan_data['loan_time'] - loan_data['bi_tm_encode_3']
print loan_data.head(5)

train=loan_data.iloc[0:55596,:]
test=loan_data.iloc[55596:,:]
train.to_csv('loan_data_train.csv')
test.to_csv('loan_data_test.csv')
    
train_data_scaled=preprocessing.scale(train)#对列表的列表可以
test_data_scaled=preprocessing.scale(test)#对列表的列表可以

train.to_csv('loan_data_train_scaled.csv')
test.to_csv('loan_data_test_scaled.csv')

target = pd.read_csv('./train/overdue_train.txt',header = None)
target.columns=['userid','label']
target.index=target['userid']
target.drop('userid',axis=1,inplace=True)
print target.head(5)
target.to_csv('loan_data_train_target.csv')
