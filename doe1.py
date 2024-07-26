import pandas as pd
import itertools
import numpy as np

# 定义因子及其水平
factors = {
    "离焦量": [-1, 0, 1],
    "焊接功率": [2700, 3100, 3500],
    "焊接速度": [70, 100, 130],
    "辅助气体清洁度": [1, 2, 3],
    "辅助护坡间隙": [0.1, 0.2, 0.3]
}

# 创建全因子实验设计
factorial_design = list(itertools.product(*factors.values()))

# 转换为DataFrame
df = pd.DataFrame(factorial_design, columns=factors.keys())

# 重复每个实验三次
df_repeated = pd.concat([df] * 3, ignore_index=True)

# 添加随机顺序列
df_repeated["运行顺序"] = np.random.permutation(len(df_repeated)) + 1

# 方法添加判断列，但不填入数据
df_repeated["因子A"] = np.nan
df_repeated["因子B"] = np.nan
df_repeated["因子C"] = np.nan

# 筛选所需列
df_filtered = df_repeated[["离焦量", "焊接功率", "焊接速度", "运行顺序"]]

# 保存为CSV文件
df_filtered.to_csv("/mnt/data/doe_experiment_design_filtered.csv", index=False)

print("筛选后的实验设计已生成并保存为 'doe_experiment_design_filtered.csv'")
print("实验设计数据包含以下列:")
print(df_filtered.columns.tolist())
print("筛选后的实验设计前几行数据:")
print(df_filtered.head())
