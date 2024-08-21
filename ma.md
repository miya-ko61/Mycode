根据您的要求，这里是完整的优化后的MATLAB程序，用于从Excel文件读取数据，计算并绘制Bode图：

```matlab
% 清除工作区和命令行
clc;
clear;

% 读取 Excel 表格数据
data = readtable('data.xlsx');

% 提取频率、增益和相位数据
frequency = data.Frequency_Hz;  % 假设表格中的列名为 'Frequency_Hz'
gain_magnitude = data.Trace_1_Gain_Magnitude_dB;  % 假设表格中的列名为 'Trace_1_Gain_Magnitude_dB'
gain_phase = data.Trace_2_Gain_Phase;  % 假设表格中的列名为 'Trace_2_Gain_Phase'

% 将dB转换为线性值并计算Gaef
Gaef = 10.^(gain_magnitude/20) .* cos(deg2rad(gain_phase));

% 创建s变量
s = tf('s');

% 定义常量
Cinj = 4700e-12;  % 注入电容
RINJ = 5e7;       % 注入电阻
C11 = 8.2e-9;     % 电容C11
R3 = 49.9;        % 电阻R3
R5 = 1e3;         % 电阻R5
C12 = 4.7e-9;     % 电容C12
R4 = 698;         % 电阻R4
R6 = 200;         % 电阻R6
L = 1e-7;         % 电感L
Rs1 = 1000;       % 电阻Rs1
Rs2 = 500;        % 电阻Rs2
Cs = 1e-7;        % 电容Cs
C13 = 47e-9;      % 电容C13

% 计算各电阻和电容的复阻抗
Zin = RINJ/(1 + s*RINJ*Cinj);  % 输入阻抗
Z1 = (R3 + 1/(s*C11))*R5 / (R3 + R5 + 1/(s*C11));  % Z1的计算
Z2 = R6 + 1/(s*C13);  % Z2的计算
Z3 = R4/(1 + s*R4*C12);  % Z3的计算

% 初始化传递函数数组
GHZs = zeros(1, length(frequency));  % 使用数组存储每个频率点的传递函数值

% 计算每个频率点的传递函数
for i = 1:length(frequency)
    GH = (1 - Gaef(i)*Z3/(Z1 + Z3)) / (Zin + Z3 + (Z1*Z3)/(Z1 + Z3));
    Zs = s*L + s^2*Cs*L/(Rs1 + Rs2);
    GHZs(i) = GH + Zs;  % 为每个频率点计算传递函数
end

% 波德图绘制
P = bodeoptions;  % 获取波德图选项
P.FreqUnits = 'Hz';  % 设置频率单位为Hz
bodeplot(tf(GHZs), P);  % 绘制波德图，注意这里需要将GHZs转换为传递函数对象
grid on;  % 显示网格
```

这个程序首先从Excel文件中读取数据，计算各个频率点的增益和相位转换值，然后通过电路模型计算每个频率的传递函数，最后绘制波德图。确保您的Excel文件路径和列名与代码中的设置相匹配，且MATLAB环境已正确配置以支持这些操作。如果有任何问题或需要进一步的帮助，请告知。
