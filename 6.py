# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pylab
from tsmoothie.smoother import *
from mysql import mysql

MYSQL_HOST = '127.0.0.1'  # 1~5号双目数据均存至该mysql
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'sonar_database'


# Mysql
my = mysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT)

sql6 = f"select time from sonar_image_data_analysis_jh6 "
sql7 = f"select time from sonar_image_data_analysis_jh7 "

count6 = my.select(sql6)
count7 = my.select(sql7)

data6 = np.array(count6)
data7 = np.array(count7)

formatted_dates6 = []
for item in data6:
    formatted_date = item[0].date().strftime("%Y-%m-%d")
    if formatted_date not in formatted_dates6:
        formatted_dates6.append(formatted_date)

formatted_dates7 = []
for item in data7:
    formatted_date = item[0].date().strftime("%Y-%m-%d")
    if formatted_date not in formatted_dates7:
        formatted_dates7.append(formatted_date)

data_all = []

for date in formatted_dates6:
    if date in formatted_dates7:
        data_all.append(date)

for temp_time in data_all:
    begin_time = temp_time + ' 00:00:00'
    exit_time = temp_time + ' 23:59:59'
    current_time = temp_time + ' 23:30:04'

    sql6 = f"select time,proportion_avg from sonar_image_data_analysis_jh6 WHERE time between '{begin_time}' and '{exit_time}'"
    sql7 = f"select time,proportion_avg from sonar_image_data_analysis_jh7 WHERE time between '{begin_time}' and '{exit_time}'"

    count6 = my.select(sql6)
    count7 = my.select(sql7)

    times6 = [item[0].strftime('%H:%M') for item in count6]
    values6 = [item[1] for item in count6]

    times7 = [item[0].strftime('%H:%M') for item in count7]
    values7 = [item[1] for item in count7]

    data6 = np.array(values6)
    data7 = np.array(values7)

    if len(data6) < 80 or len(data7) < 80:
        continue
    # 平滑

    smoother6 = KalmanSmoother(component='level_trend', component_noise={'level': 0.1, 'trend': 0.1})
    smoother7 = KalmanSmoother(component='level_trend', component_noise={'level': 0.1, 'trend': 0.1})

    # smoother6 = SpectralSmoother(smooth_fraction=0.2, pad_len=20)
    # smoother7 = SpectralSmoother(smooth_fraction=0.2, pad_len=20)

    smoother6.smooth(data6)
    # _low, _up = smoother1.get_intervals('sigma_interval', n_sigma=2)
    # print(smoother1.smooth_data)
    smoother7.smooth(data7)

    plt.figure(figsize=(30, 10))
    plt.subplot(2, 1, 1)

    # data['low'] = np.hstack([data['low'], _low[:,[-1]]])
    # data['up'] = np.hstack([data['up'], _up[:,[-1]]])
    # is_anomaly = np.logical_or(
    #     data['original'][:,-1] > data['up'][:,-1],
    #     data['original'][:,-1] < data['low'][:,-1]
    # ).reshape(-1,1)

    pylab.plot(range(len(data6)), data6, '-', linewidth=3, color='g')
    pylab.plot(range(len(data6)), smoother6.smooth_data.reshape(-1, 1), linewidth=3, color='blue')
    pylab.title(temp_time)
    pylab.xticks(range(len(data6)), labels=times6, rotation=45)

    plt.subplot(2, 1, 2)
    pylab.plot(range(len(data7)), data7, '-', linewidth=3, color='g')
    pylab.plot(range(len(data7)), smoother7.smooth_data.reshape(-1, 1), linewidth=3, color='blue')
    pylab.xticks(range(len(data7)), labels=times7, rotation=45)

    print(temp_time)

    # pylab.plot( range(len(data)), _low.reshape(-1,1) ,color='blue')
    # pylab.plot( range(len(data)), _up.reshape(-1,1), color='blue')

    # path = 'duibi/{}.png'.format(str(temp_time))
    # plt.savefig(path, dpi=300)
    # pylab.show()
