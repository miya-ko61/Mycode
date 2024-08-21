在你提供的这段代码中，主要的问题依然是传递函数 `GH` 和 `GHZs_total` 没有在每个频率点上独立计算和评估，因此你在循环中累加的实际上是符号性的表达式，而不是在每个频率点上计算得到的具体数值。这会导致波德图绘制时可能不反映各个频率点的实际响应。

为了确保每个频率点的传递函数被正确评估并累加，需要在循环中对 `Z1`、`Z2`、`Z3`、`GH` 等传递函数对象在具体的频率下进行评估，并将其数值化后再进行累加。

### 改进后的代码

下面的代码对你原有代码进行了一些修改，确保在每个频率点上对传递函数进行数值化评估，并正确累加这些结果。

```matlab
% 清除工作区和命令行
clc;
clear;

% 读取 Excel 表格数据
disp('正在读取数据...');
data = readtable('data.xlsx');

% 提取频率、增益和相位数据
frequency = data.Frequency_Hz;  % 假设表格中的列名为 'Frequency_Hz'
gain_magnitude = data.Trace_1_Gain_Magnitude_dB;  % 假设表格中的列名为 'Trace_1_Gain_Magnitude_dB'
gain_phase = data.Trace_2_Gain_Phase;  % 假设表格中的列名为 'Trace_2_Gain_Phase'

% 将dB转换为线性值并计算Gaef
Gaef = 10.^(gain_magnitude/20) .* cos(deg2rad(gain_phase));

% 定义电路元件参数
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

% 初始化传递函数结果
GHZs_total = zeros(1, num_points);

% 创建进度条
h = waitbar(0, '正在计算传递函数...');

% 计算每个频率点的传递函数并累加
num_points = length(frequency);
for i = 1:num_points
    omega = 2 * pi * frequency(i);  % 计算角频率
    s = 1j * omega;  % 创建当前频率下的复频率变量
    
    % 计算各频率点下的阻抗
    Zin = RINJ/(1 + s*RINJ*Cinj);
    Z1 = (R3 + 1/(s*C11))*R5 / (R3 + R5 + 1/(s*C11));
    Z2 = R6 + 1/(s*C13);
    Z3 = R4/(1 + s*R4*C12);
    Zs = s*L + s^2*Cs*L/(Rs1 + Rs2);
    
    % 计算当前频率下的 GH 和总传递函数
    GH = (1 - Gaef(i)*Z3/(Z1 + Z3)) / (Zin + Z3 + (Z1*Z3)/(Z1 + Z3));
    
    % 将当前频率点的结果累加到总结果中
    GHZs_total(i) = GH + Zs;

    % 更新进度条
    waitbar(i / num_points, h);
end

% 关闭进度条
close(h);

% 绘制波德图
P = bodeoptions;  % 获取波德图选项
P.FreqUnits = 'Hz';  % 设置频率单位为Hz
bodeplot(frequency, GHZs_total, P);  % 绘制波德图
grid on;  % 显示网格
```

### 关键改动说明：

1. **频率点的独立评估**：
   - 在每个频率点上，使用当前的 `s`（复频率变量）计算 `Z1`、`Z2`、`Z3` 等的数值。这样，传递函数在每个频率点上是独立的，并且是基于具体频率的数据。

2. **累加到数值数组**：
   - `GHZs_total` 被定义为一个数组，用于存储每个频率点上的计算结果，而不是使用 `tf` 对象来累加符号表达式。

3. **绘制波德图**：
   - 在波德图绘制时，`bodeplot` 函数直接使用了 `frequency` 和 `GHZs_total` 的数值形式，而不是符号表达式。

### 总结：

通过这次调整，程序在每个频率点上计算具体的传递函数值，并将这些结果累加到一个数值数组中。这样做可以确保每个频率点的传递函数计算是独立且正确的，最终生成的波德图能够准确地反映电路的频率响应。如果你运行这个改进后的代码，应该会看到每个频率点上的传递函数响应，并且波德图能够反映出实际的频率响应特性。
