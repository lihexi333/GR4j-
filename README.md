# GR4j-
![Static Badge](https://img.shields.io/badge/Python-3.12-green)
![Static Badge](https://img.shields.io/badge/conda-24.1.2-orange)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/lihexi333/GR4j-/main)





这是水文与软件工程小组的GR4j模型作业

##  模型介绍
GR4j模型是一种用于模拟和预测水文过程的模型。它基于四阶Runge-Kutta方法，是一种经典的数值方法，用于求解常微分方程。GR4j模型是一种广泛使用的模型，被广泛应用于水文学、气象学等领域。  
在此项目中，我们使用**GR4j模型**来模拟和预测水文过程。同时使用**贝叶斯调参**技术来优化模型的四个输入参数。

## 项目结构
```
GR4j-
├── GR4j模型                 # 模型文件夹
│   ├── data                # 数据文件夹
│   │   ├── demo_124002A
│   │   ....
│   │   └── demo_919005A 
│   ├── environment.yaml    # 环境配置文件
│   ├── evaluate.py   
│   ├── mytools.py   
│   ├── run.py              # 运行
│   └── simulate.py   
├── .gitignore              # Git忽略文件
├── README.md               # README说明文件
├── 大作业报告               
├── 实践课程2-水文模型         # 课程资料文件夹
├── 小组作业数据
└── 运行结果
```
## 使用说明

### 1.克隆仓库并进入文件夹
```
git clone https://github.com/lihexi333/GR4j-.git
cd GR4j-/GR4j模型
```
### 2.环境配置
```
conda env create -f environment.yml
conda activate Python3.12
```
### 3.运行模型
在当前文件夹`GR4j模型`下`data`文件夹，放入包含`inputData.txt`数据文件和`others.txt`参数文件的所有数据文件夹
```
python run.py
```
### 4.查看结果
- 运行完成后会弹出plotly绘图页面  
- 在模型文件夹下生成`GR4J_Parameter.xlsx`表格，包含得到的十组数据最优参数
- 在模型文件夹会生成`结果图表`文件夹存储所有运行结果图  
- 同时在`data`文件夹中每个数据文件夹下会生成两个文件：
  - `GR4J_opt_log.xlsx`  贝叶斯调参日志表格
  - `GR4J_Parameter_best.txt`  模型最优参数

## 贡献者

<a href="https://github.com/lihexi333/GR4j-/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=lihexi333/GR4j-" />
</a>
