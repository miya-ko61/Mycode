import pandas as pd
import itertools
import numpy as np

# 定义因子及其水平
factors = {
    "离焦量": [-1, 0, 1],
    "焊接功率": [2700, 3100, 3500],
    "焊接速度": [70, 100, 130],
    "焊接间隙": [0.1, 0.2, 0.3],
    "铜排表面清洁度": [1, 2, 3],
    "铜排焊接间隙": [0.1, 0.2, 0.3]
}

# 创建全因子实验设计
factorial_design = list(itertools.product(*factors.values()))

# 转换为DataFrame
df = pd.DataFrame(factorial_design, columns=factors.keys())

# 添加随机顺序列
df['运行顺序'] = np.random.permutation(len(df)) + 1

# 添加评判指标列，但不填入数据
df['拉力'] = np.nan
df['熔深'] = np.nan
df['熔宽'] = np.nan

# 保存为CSV文件
df.to_csv("doe_experiment_design.csv", index=False)

print("实验设计已生成并保存为 'doe_experiment_design.csv'")
print("实验设计包含以下列：")
print(df.columns.tolist())
print("\n前5行数据预览：")
print(df.head())
