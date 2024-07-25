import pandas as pd
import itertools

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

# 保存为CSV文件
df.to_csv("doe_experiment_design.csv", index=False)
