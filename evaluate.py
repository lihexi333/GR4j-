# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def evaluate_gr4j_model(nStep, Qobs_mm, Q):
    # 精度评估
    count = 0  # 计数器：记录总天数
    Q_accum = 0.0  # 记录累计径流量
    Q_ave = 0.0  # 记录平均径流量
    NSE = 0.0  # 记录纳什效率系数
    Q_diff1 = 0.0
    Q_diff2 = 0.0

    for i in range(1000, nStep):
        count += 1
        Q_accum += Qobs_mm[i]

    Q_ave = Q_accum / count  # 计算观测流量平均值

    for i in range(1000, nStep):
        Q_diff1 += (Qobs_mm[i] - Q[i]) ** 2  # 计算Nash-Sutcliffe指数分子
        Q_diff2 += (Qobs_mm[i] - Q_ave) ** 2  # 计算Nash-Sutcliffe指数分母

    NSE = 1 - Q_diff1 / Q_diff2

    # # 修正中文乱码问题，提供字体支持即可
    # import matplotlib as mpl
    # mpl.rcParams['font.sans-serif'] = ['KaiTi']
    # mpl.rcParams['font.serif'] = ['KaiTi']
    #
    #
    # # 评估径流模拟效果：模型流域出口断面流量及模拟得到的流域出口断面流量
    # # 绘制相关图
    axis = list(range(1, nStep + 1))
    # plt.figure()
    # plt.plot(axis, Q, '--', label='模拟径流量')
    # plt.plot(axis, Qobs_mm, 'y-', label='观测径流量',alpha=0.7)
    # plt.title('GR4J模型模拟效果图, NSE=' + str(NSE))
    # plt.xlabel('时间（天）')
    # plt.ylabel('流量（mm/d）')
    # plt.legend()
    # plt.show()

    # import plotly.graph_objects as go
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=axis, y=Q, mode='lines', name='模拟径流量'))
    # fig.add_trace(go.Scatter(x=axis, y=Qobs_mm, mode='lines', name='观测径流量'
    #                               , line=dict(color='yellow', width=2)))
    # fig.update_layout(title='GR4J模型模拟效果图, NSE=' + str(NSE),
    #                     xaxis_title='时间（天）', yaxis_title='流量（mm/d）')
    # fig.show()

    #使用plotly绘制堆叠柱状图,适当美化柱状图显示
    import plotly.graph_objects as go

    # 创建折线图
    fig = go.Figure()

    # 添加模拟径流量数据
    fig.add_trace(go.Scatter(
        x=axis ,
        y=Q ,
        mode='lines' ,
        name='模拟径流量' ,
        line=dict(color='rgba(31, 119, 180, 0.8)' , width=2) ,
        hovertemplate='%{y}' ,
        opacity=0.7
    ))

    # 添加观测径流量数据
    fig.add_trace(go.Scatter(
        x=axis ,
        y=Qobs_mm ,
        mode='lines' ,
        name='观测径流量' ,
        line=dict(color='rgba(255, 165, 0, 0.8)' , width=2) ,
        hovertemplate='%{y}' ,
        opacity=0.7
    ))

    # 设置图表标题和轴标签
    fig.update_layout(
        title=dict(
            text=f'<b>GR4J模型模拟效果图, NSE={NSE}</b>' ,
            font=dict(size=20),
            x=0.5
        ) ,
        xaxis=dict(
            title='时间（天）' ,
            titlefont=dict(size=14) ,
            tickfont=dict(size=12) ,
            showgrid=True ,  # 显示网格线
            zeroline=False  # 不显示x轴上的零线
        ) ,
        yaxis=dict(
            title='流量（mm/d）' ,
            titlefont=dict(size=14) ,
            tickfont=dict(size=12) ,
            showgrid=True ,  # 显示网格线
            zeroline=False  # 不显示y轴上的零线
        ) ,
        legend=dict(
            x=0.01 , y=0.99 ,
            bgcolor='rgba(255, 255, 255, 0.5)' ,  # 设置图例背景透明度
            bordercolor='Black' ,
            borderwidth=1
        ) ,
        plot_bgcolor='rgba(240, 240, 240, 0.95)'  # 设置绘图背景颜色
    )

    # 美化图表显示
    fig.update_traces(
        hoverinfo='x+y' ,  # 设置悬停信息
    )

    # 显示图表
    fig.show()

    return NSE

