# -*- coding: utf-8 -*-
import numpy as np

def simulate_gr4j(nStep, x1, x2,x3,x4, upperTankRatio, lowerTankRatio, maxDayDelay, UH1, UH2, Pn, En):
    # 定义一些产汇流计算需要用到的数值及数组
    S0 = upperTankRatio * x1  # 产流水库初始土壤含水量=比例*产流水库容量
    R0 = lowerTankRatio * x3  # 汇流水库初始土壤含水量=比例*汇流水库容量
    S_TEMP = S0  # 用S_TEMP存储当前产流水库储量
    R_TEMP = R0  # 用R_TEMP存储当前汇流水库储量
    S = np.zeros(nStep)  # S：产流水库逐日水量
    R = np.zeros(nStep)  # R：汇流水库逐日水量
    UH_Fast = np.zeros((nStep, maxDayDelay))  # UH_Fast: 用于记录UH1单位线作用下的产流信息
    UH_Slow = np.zeros((nStep, maxDayDelay * 2))  # UH_Slow: 用于记录UH2单位线作用下的产流信息
    Ps = np.zeros(nStep)
    Es = np.zeros(nStep)
    Perc = np.zeros(nStep)
    Pr = np.zeros(nStep)
    F = np.zeros(nStep)
    Qr = np.zeros(nStep)  # Qr：汇流水库快速流出流量
    Qd = np.zeros(nStep)  # Qd：汇流水库慢速流出流量
    Q = np.zeros(nStep)  # Q：汇流总出流量

    # 获取En及Pn值后，更新产流水库蓄水量
    for i in range(nStep):
        S[i] = S_TEMP
        R[i] = R_TEMP

        # Pn(i)及En(i)有且仅有一个大于0，所以下面两个if判断只可能一个为真
        if Pn[i] != 0:  # 净雨量大于0，此时一部分净雨形成地面径流，一部分下渗
            Ps[i] = x1 * (1 - ((S[i] / x1) ** 2)) * np.tanh(Pn[i] / x1) / (1 + S[i] / x1 * np.tanh(Pn[i] / x1))
            Es[i] = 0
        if En[i] != 0:  # 净蒸发能力大于0，此时土壤中水分一部分用于消耗
            Ps[i] = 0
            Es[i] = (S[i] * (2 - (S[i] / x1)) * np.tanh(En[i] / x1)) / (1 + (1 - S[i] / x1) * np.tanh(En[i] / x1))

        # 更新上层水库蓄水量
        S_TEMP = S[i] - Es[i] + Ps[i]
        Ratio_TEMP = S_TEMP / x1

        # 计算产流水库渗漏
        Perc[i] = S_TEMP * (1 - (1 + (4.0 / 9.0 * (S_TEMP / x1)) ** 4) ** (-0.25))

        # 计算产流总量
        Pr[i] = Perc[i] + (Pn[i] - Ps[i])

        # 更新当前产流水库水量，作为次日产流水库水量
        S_TEMP = S_TEMP - Perc[i]

        # 至此产流过程全部结束，进入汇流阶段

        # 汇流计算
        # 计算地表水与地下水之间的水量交换
        F[i] = x2 * (R[i] / x3) ** 3.5

        # 计算地表水汇流，将产流量按照90%(快速)和10%(慢速)划分
        # 快速地表径流汇流使用单位线UH1；慢速地表径流汇流使用单位线UH2
        R_Fast = Pr[i] * 0.9
        R_Slow = Pr[i] * 0.1

        if i == 0:
            UH_Fast[i, :] = R_Fast * UH1  # 第1时段产流量在时间上的分配
            UH_Slow[i, :] = R_Slow * UH2  # 第1时段产流量在时间上的分配
        else:
            UH_Fast[i, :] = R_Fast * UH1  # 先计算当前时段产流量在时间上的分配
            for j in range(maxDayDelay - 1):
                UH_Fast[i, j] = UH_Fast[i, j] + UH_Fast[i - 1, j + 1]  # 第2时段总汇流=第2时段产流量当前汇流+第1时段产流量第2部分汇流

            UH_Slow[i, :] = R_Slow * UH2  # 先计算当前时段产流量在时间上的分配
            for j in range(2 * maxDayDelay - 1):
                UH_Slow[i, j] = UH_Slow[i, j] + UH_Slow[i - 1, j + 1]  # 第2时段总汇流=第2时段产流量当前汇流+第1时段产流量第2部分汇流

        # 此处应注意下标
        # 更新汇流水库水量变化
        R_TEMP = max(0, R_TEMP + UH_Fast[i, 1] + F[i])

        # 计算汇流水库快速流出流量
        Qr[i] = R_TEMP * (1 - (1 + (R_TEMP / x3) ** 4) ** (-0.25))

        # 再次更新汇流水库水量变化
        R_TEMP = R_TEMP - Qr[i]

        # 此处应注意下标
        # 计算汇流水库慢速流出流量
        Qd[i] = max(0, UH_Slow[i, 1] + F[i])

        # 计算汇流总出流量
        Q[i] = Qr[i] + Qd[i]

    return Q

