# 开关门
CLOSE_DOOR_15 = False  # 关闭15号门
CLOSE_DOOR_16 = False  # 关闭16号门
CLOSE_DOOR_17 = False  # 关闭17号门
OPEN_DOOR_18 = False  # 打开18号门
OPEN_DOOR_19 = False  # 打开19号门
OPEN_DOOR_20 = False  # 打开20号门
OPEN_DOOR_21 = False  # 打开21号门
OPEN_DOOR_22 = False  # 打开22号门

# 外部人员进入
EMERGENCY_PERSONNEL_ENTRANCE = False  # 是否允许外部人员进入
EMERGENCY_PERSONNEL_TIME_DELAY = 60  # 外部人员进入需要的时间
EMERGENCY_PERSONNEL_DOOR = 15  # 外部人员进入的门的点位号，optional: 15, 16, 17

# 结果输出
OUTPUT_DIRECTORY = 'D:/mcm'
SAVE_INDIVIDUAL_DETAIL = False  # 输出个体细节图片
SAVE_TIME_HIST = False  # 输出时间直方图

# 模型假设与概况
TIME_SPAN = 50  # 定义单宽度楼梯几秒可以过一群人
TIME_DOWNSTAIRS = 10  # 定义下楼需要几秒
CHOICES = [
    # 目标点：数量
    {2: 1, 4: 2, 5: 1, 6: 1, 8: 2},
    {2: 3, 3: 1, 4: 2, 5: 2, 6: 2, 8: 2, 9: 1, 11: 2, 12: 1},
    {1: 4, 2: 2, 5: 2, 7: 2, 8: 2, 9: 4, 10: 4, 11: 2, 12: 1, 13: 2, 15: 4, 16: 4, 17: 4},
    {7: 1, 9: 1, 10: 2, 14: 3},
]
EXIT_CHOICES = (15, 16, 17, 18, 19, 20, 21, 22)  # 出口点号

# 点号
POSITIONS = {
    1: (265, 220), 2: (365, 220), 3: (465, 220), 4: (540, 185), 5: (615, 185),
    6: (615, 35), 7: (540, 35), 8: (465, 110), 9: (465, 0), 10: (365, 0),
    11: (265, 0), 12: (130, 0), 13: (615, 110), 14: (365, 110), 15: (100, 0),
    16: (265, 220), 17: (365, 220), 18: (615, 110), 19: (400, 0), 20: (465, 110),
    21: (615, 185), 22: (615, 35),
}

# 关于遗传算法
CHOICES_OF_ONE_PERSON = 10  # 每个人可以选择的路线数量，解空间为这个变量的500次方
LARGE_DATA = True  # 采用500的数据
POPULATION_RANGE = 100  # 种群规模
SELECT_MAX = 5  # 保留最优的个体数
MUTATE_THRESHOLD = 0.05  # 变异概率
MATE_THRESHOLD = 0.1  # 交配概率
MATE_NUMBER_COVER = 10  # 覆盖的次数
MATE_NUMBER_EXCHANGE = 10  # 交换的次数

# 一些后处理代码
if CLOSE_DOOR_15:
    del CHOICES[2][15]
if CLOSE_DOOR_16:
    del CHOICES[2][16]
if CLOSE_DOOR_17:
    del CHOICES[2][17]
if OPEN_DOOR_18:
    CHOICES[2][18] = 2
if OPEN_DOOR_19:
    CHOICES[2][19] = 2
if OPEN_DOOR_20:
    CHOICES[2][20] = 2
if OPEN_DOOR_21:
    CHOICES[2][21] = 2
if OPEN_DOOR_22:
    CHOICES[2][22] = 2
