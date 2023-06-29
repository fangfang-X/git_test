import math
# 计算点到直线的距离

def distance_to_line(x1, y1, x2, y2, x3, y3):
    # 计算直线的斜率
    slope = (y3 - y2) / (x3 - x2)

    # 计算直线的截距
    intercept = y2 - slope * x2

    # 计算点到直线的距离公式
    distance = abs(slope * x1 - y1 + intercept) / ((slope ** 2 + 1) ** 0.5)
    print(f'点到平面的距离为：{distance}\t实际距离为：{distance * 45 / 915}')

    return distance

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    print(f'两点之间的距离为：{distance}')
    return distance
#经海6号
# distance_to_line(927,934,1186,727,842,411)
# distance_to_line(927,934,1226,770,808,389)
# distance_to_line(927,934,985,528,1140,692)

#经海7号
# distance_to_line(927,934,824,399,1111,676)
# distance_to_line(927,934,931,501,1163,724)
# distance_to_line(927,934,932,437,1134,697)

#经海7号
# distance_to_line(927,934,912,501,1126,675)
# distance_to_line(927,934,944,485,1094,643)
distance_to_line(927,934,954,486,1112,656)


