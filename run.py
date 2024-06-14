# -*- coding: utf-8 -*-
"""
Version: 1.0
Date: 2024-04-11

Change log:
- V1.0 (2024-04-11): 初始版本

This code is released under the GNU General Public License (GPL) version 3.
see <http://www.gnu.org/licenses/>.
"""
import os

from simulate import *
import numpy as np
from mytools import *
from evaluate import *
from bayes_opt import BayesianOptimization
import pandas as pd


# 模型得分
def score(nStep, Qobs_mm, Q):
    # 精度评估
    count = 0  # 计数器：记录总天数
    Q_accum = 0.0  # 记录累计径流量
    Q_ave = 0.0  # 记录平均径流量
    NSE = 0.0  # 记录纳什效率系数
    Q_diff1 = 0.0
    Q_diff2 = 0.0

    for i in range(1000 , nStep):
        count += 1
        Q_accum += Qobs_mm[i]

    Q_ave = Q_accum / count  # 计算观测流量平均值

    for i in range(1000 , nStep):
        Q_diff1 += (Qobs_mm[i] - Q[i]) ** 2  # 计算Nash-Sutcliffe指数分子
        Q_diff2 += (Qobs_mm[i] - Q_ave) ** 2  # 计算Nash-Sutcliffe指数分母

    NSE = 1 - Q_diff1 / Q_diff2
    return NSE

# gr4j模型
def model(x1,x2,x3,x4,eval=False):
    # 加载GR4J其他参数
    other_para = np.loadtxt('data/others.txt')
    area = other_para[0]  # 流域面积(km2)
    upperTankRatio = other_para[1]  # 产流水库初始填充率 S0/x1
    lowerTankRatio = other_para[2]  # 汇流水库初始填充率 R0/x3

    # 加载数据文件
    data = np.loadtxt('data/inputData.txt')
    P = data[: , 0]  # 第二列: 日降雨量(mm)
    E = data[: , 1]  # 第三列: 蒸散发量(mm)
    Qobs = data[: , 2]  # 第四列: 流域出口观测流量(ML/day)

    Qobs_mm = Qobs * 86.4 / area  # 将径流量单位从ML/day转化为mm/s

    # 根据逐日降雨量及逐日蒸发量，计算流域出口断面逐日径流量
    nStep = data.shape[0]  # 计算数据中有多少天

    # 初始化变量，存储GR4J模型中间变量值
    Pn = np.zeros(nStep)  # Pn：降雨扣除损失（蒸发）后得净雨
    En = np.zeros(nStep)  # En：当日蒸发未被满足部分，此部分未得到满足得蒸发将消耗土壤中得水分
    Ps = np.zeros(nStep)  # Ps：中间变量，记录净雨补充土壤含水量
    Es = np.zeros(nStep)  # Es: 中间变量，记录剩余蒸发能力消耗土壤含水量
    Perc = np.zeros(nStep)  # Perc: 中间变量，记录产流水库壤中流产流量
    Pr = np.zeros(nStep)  # Pr: 记录产流总量

    # 根据输入参数x4计算S曲线以及单位线，这里假设单位线长度UH1为10，UH2为20;即x4取值不应该大于10
    maxDayDelay = 10

    # 定义几个数组以存储SH1, UH1, SH2, UH2
    SH1 = np.zeros(maxDayDelay)
    UH1 = np.zeros(maxDayDelay)
    SH2 = np.zeros(2 * maxDayDelay)
    UH2 = np.zeros(2 * maxDayDelay)


    # 计算SH1以及SH2，由于i是从0开始的，为避免第一个数值为0，我们在函数钟使用i+1
    for i in range(maxDayDelay):
        SH1[i] = SH1_CURVE(i , x4)

    for i in range(2 * maxDayDelay):
        SH2[i] = SH2_CURVE(i , x4)

    # 计算UH1以及UH2
    for i in range(maxDayDelay):
        if i == 0:
            UH1[i] = SH1[i]
        else:
            UH1[i] = SH1[i] - SH1[i - 1]

    for i in range(2 * maxDayDelay):
        if i == 0:
            UH2[i] = SH2[i]
        else:
            UH2[i] = SH2[i] - SH2[i - 1]

    # 计算逐日En及Pn值，En及Pn为GR4J模型的输入，可以提前计算出来
    for i in range(nStep):
        if P[i] >= E[i]:  # 若当日降雨量大于等于当日蒸发量，净降雨量Pn = P - E，净蒸发能力En = 0
            Pn[i] = P[i] - E[i]
            En[i] = 0
        else:  # 若当日降雨量小于当日蒸发量，净降雨量Pn = 0，净蒸发能力En = E - P
            Pn[i] = 0
            En[i] = E[i] - P[i]

    # Q值的计算

    Q = simulate_gr4j(nStep , x1 , x2 , x3 , x4 , upperTankRatio , lowerTankRatio , maxDayDelay , UH1 , UH2 , Pn , En)
    if eval == True:
        evaluate_gr4j_model(nStep , Qobs_mm , Q)
    return score(nStep,Qobs_mm , Q)

# 调参函数
def opt():
    # 使用贝叶斯优化调参
    params = {"x1":(10,700),"x2":(-5.5,3.5),"x3":(20,400),"x4":(1.0,2.5)}
    optimizer=BayesianOptimization(f=model,pbounds=params,random_state=1)
    optimizer.maximize(init_points=5,n_iter=150)
    # print(optimizer.res)
    reslist=[]
    for i in optimizer.res:
        l={"NSE":i['target']}
        # print(nse)
        l.update(i['params'])
        reslist.append(l)
    # print(reslist)
    data = pd.DataFrame(reslist)
    data=data.sort_values('NSE',ascending=False) #按照NSE值降序排序
    data.to_excel("GR4J_opt_log.xlsx")
    print("最优参数：\n",end='')
    # 最优参数保留到小数点后三位
    for k,v in optimizer.max['params'].items():
        print('\t%s:%0.3f'%(k,v))
    print("NSE="+str(optimizer.max['target']))
    return  optimizer.max['params']
if __name__ == '__main__':
    if  os.path.exists("GR4J_Parameter_best.txt"):
        params = np.loadtxt('GR4J_Parameter_best.txt')
        print("NSE:"+str(model(params[0],params[1],params[2],params[3],eval=True)))
    else:
        params=opt() #获取最优参数
        print("NSE:"+str(model(round(params['x1'],3),round(params['x2'],3),round(params['x3'],3),round(params['x4'],3),eval=True))) #加载最优模型
        with  open("GR4J_Parameter_best.txt","w") as f:
            for v in  params.values():
                f.write(str(round(v,3))+"\n")
    print("GR4J Simulation Finished")
