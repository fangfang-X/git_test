# -*- coding: utf-8 -*-



import datetime
from mysql import mysql
import numpy as np
from pyod.models.copod import COPOD
import math
import pylab
import seaborn as sns
# Mysql
MYSQL_HOST = '127.0.0.1'  # 1~5号双目数据均存至该mysql
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'sonar_database'


sns.set_theme()
sns.set_style("darkgrid", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})

my = mysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT)
no_delete_error_data_all = [[],[]]
delete_error_data_all = [[],[]]
data_all_max = [[],[]]
DATA = []
temp_time = '2023-05-24'

begin_time = temp_time + ' 00:00:00'
exit_time = temp_time + ' 23:59:59'
current_time = temp_time + ' 23:30:04'

print(current_time,end='\t')

sql = f"select proportion_avg from sonar_image_data_analysis_jh6 WHERE time between '{begin_time}' and '{exit_time}'"

count = my.select(sql)
data = np.array(count)


old_10 = np.array(sorted(data.tolist())[-math.ceil(len(count) * 0.1):]).reshape(-1, 1)

if len(old_10) == 0:
    temp_time = datetime.datetime.strptime(temp_time, '%Y-%m-%d')
    temp_time = temp_time + datetime.timedelta(days=1)
    temp_time = str(temp_time)[:10]
    print('num = 0')


clf = COPOD()
clf.fit(data)

y_train_pred = np.array(clf.labels_)  # 返回训练数据上的分类标签 (0: 正常值, 1: 异常值)
x_True = np.array(data[y_train_pred == 0]).reshape(-1, 1)
new_10 = np.array(sorted(x_True.tolist())[-math.ceil(len(count) * 0.1):]).reshape(-1, 1)

data_max = np.max(data)
data_mean_old_10 = np.mean(old_10)
data_mean_bew_10 = np.mean(new_10)
#JH7
# x = [2, 13.1, 10.4, 12.23, 30]
# y = [30, 92.0096, 90.1263, 91.8792, 200]
#JH8
x = [2, 5.85, 13.6, 11.7]
y = [0, 12.6, 42.6, 38.3]

z1 = np.polyfit(x, y, 2)
p1 = np.poly1d(z1)
finall_num = p1(data_mean_old_10) * 10000
finall_num2 = p1(data_mean_bew_10) * 10000
finall_num3 = p1(data_max) * 10000
print(data_mean_old_10, end='\t')
print(finall_num)

no_delete_error_data_all[0].append(round(data_mean_old_10,2))
no_delete_error_data_all[1].append(int(finall_num))

delete_error_data_all[0].append(round(data_mean_bew_10,2))
delete_error_data_all[1].append(int(finall_num2))


data_all_max[0].append(data_max)
data_all_max[1].append(int(finall_num3))

DATA.append(str(temp_time))

temp_time = datetime.datetime.strptime(temp_time, '%Y-%m-%d')
temp_time = temp_time + datetime.timedelta(days=1)
temp_time = str(temp_time)[:10]

pylab.figure(figsize=(40, 10))

X = range(len(no_delete_error_data_all[1]))
Y1 = no_delete_error_data_all[1]
Y2 = delete_error_data_all[1]
Y3 = data_all_max[1]

pylab.plot(DATA, Y3, '-', color='g', label='每天最高值')
pylab.plot(DATA, Y1 , '-', color='b', label='全部数据前10%')
pylab.plot(DATA, Y2, '-', color='r', label='去除异常值后的前10%')

for a, b in zip(X, Y3):
    pylab.text(a, b, b, ha='center', va='bottom', fontsize=15)
for a, b in zip(X, Y1):
    pylab.text(a, b, b, ha='center', va='bottom', fontsize=15)

for a, b in zip(X, Y2):
    pylab.text(a, b, b, ha='center', va='bottom', fontsize=15)

pylab.setp(pylab.gca().get_xticklabels(), rotation=30)
pylab.title('经海6号数据处理方式对比' ,fontsize=15)
pylab.legend(loc=1)
pylab.savefig('JH6.png', dpi=300)
pylab.show()


