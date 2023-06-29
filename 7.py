# -*- coding: utf-8 -*-
import copy
import matplotlib.pyplot as plt
import pylab
import seaborn as sns
from tsmoothie.smoother import *
from mysql import mysql

sns.set_theme()
sns.set_style("darkgrid", {"font.sans-serif": ['simhei', 'Droid Sans Fallback']})

MYSQL_HOST = '127.0.0.1'  # 1~5号双目数据均存至该mysql
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'sonar_database'

temp_time = '2023-05-02'

begin_time = temp_time + ' 00:00:00'
exit_time = temp_time + ' 23:59:59'
current_time = temp_time + ' 23:30:04'

my = mysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT)
# Mysql
MYSQL_HOST = '127.0.0.1'  # 1~5号双目数据均存至该mysql
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'sonar_database'

sql = f"select proportion_avg from sonar_image_data_analysis_jh6 WHERE time between '{begin_time}' and '{exit_time}'"
count = my.select(sql)
data = np.array(count)
base_smoother_name = ['频谱平滑', '多项式平滑', '样条平滑', '高斯平滑', 'Binner平滑', '局部加权平滑', '卡尔曼平滑']
base_smoother_list = [SpectralSmoother(smooth_fraction=0.2, pad_len=20),
                      PolynomialSmoother(degree=6),
                      SplineSmoother(n_knots=6, spline_type='natural_cubic_spline'),
                      GaussianSmoother(n_knots=6, sigma=0.1),
                      BinnerSmoother(n_knots=6),
                      LowessSmoother(smooth_fraction=0.2, iterations=1),
                      KalmanSmoother(component='level_trend', component_noise={'level': 0.1, 'trend': 0.1})]

Sinusoidal_Smoothing_name = []

plt.figure(figsize=(18, 10))
plt.subplots_adjust(hspace=0.5)
for num, i in enumerate(base_smoother_list):
    data_temp = copy.deepcopy(data)
    smoother = i
    smoother.smooth(data_temp)
    plt.subplot(4, 2, num + 1 % 2)
    pylab.plot(range(len(data)), data, '-', linewidth=3, color='g')
    pylab.plot(range(len(data)), smoother.smooth_data.reshape(-1, 1), linewidth=3, color='blue')
    pylab.title(base_smoother_name[num])
plt.savefig('savefig.png', dpi=300)
pylab.show()
