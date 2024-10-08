import pandas as pd
import itertools

# 定义因子及其水平
factors = {
    "离焦量": [-1, 0, 1],
    "焊接功率": [2700, 3100, 3500],
    "焊接速度": [70, 100, 130]
}

# 创建全因子实验设计
factorial_design = list(itertools.product(*factors.values()))

# 转换为DataFrame并重复每个实验三次
df = pd.DataFrame(factorial_design, columns=factors.keys())

# 生成实验次序列，确保每个实验组合依次执行三次
experiment_orders = []
for i in range(len(df)):
    experiment_orders.extend([i*3 + 1, i*3 + 2, i*3 + 3])

# 重复实验组合并添加实验次序列
df_repeated = pd.concat([df]*3, ignore_index=True)
df_repeated["实验次序"] = experiment_orders

# 添加评判指标列，但不填入数据
df_repeated["拉力"] = pd.NA
df_repeated["溶深"] = pd.NA
df_repeated["溶宽"] = pd.NA

# 保存为CSV文件
df_repeated.to_csv("/mnt/data/doe_experiment_design.csv", index=False)

print("实验设计已生成并保存为 'doe_experiment_design.csv'")
print("实验设计数据包含以下列:")
print(df_repeated.columns.tolist())
print("实验设计前几行数据:")
print(df_repeated.head())
