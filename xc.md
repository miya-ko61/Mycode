在电路分析中，累加不同频率点的传递函数通常是不必要的或不恰当的做法，尤其是当你希望绘制波德图来分析电路在不同频率下的响应时。传递函数的累加往往会扭曲最终结果，导致生成的波德图不再反映真实的电路行为。

### 1. **为什么不需要累加？**

在频率响应分析中，每个频率点的传递函数（或者增益）应该独立计算并直接用于绘制波德图，而不是累加起来。累加的做法可能是误解了多频率点计算的目的。事实上：

- **传递函数是频率的函数**：每个频率点都有其对应的传递函数值，这些值是独立的，用于表示电路在该特定频率下的行为。
- **波德图展示的是各个频率点的独立响应**：波德图的目的就是展示在每个频率点，系统（或电路）的增益和相位如何变化。如果累加不同频率的传递函数，结果将无法准确表示任何单一频率下的系统行为。

### 2. **应当如何处理？**

正确的做法是在每个频率点计算出该频率对应的传递函数值，然后将这些值直接用于绘制波德图，而不是累加这些值。以下是修改后的代码，去掉累加操作：

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
GHZs_total = zeros(1, length(frequency));

% 创建进度条
h = waitbar(0, '正在计算传递函数...');

% 计算每个频率点的传递函数（不累加）
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
    
    % 计算当前频率下的 GH 和传递函数
    GHZs_total(i) = (1 - Gaef(i)*Z3/(Z1 + Z3)) / (Zin + Z3 + (Z1*Z3)/(Z1 + Z3)) + Zs;

    % 更新进度条
    waitbar(i / num_points, h);
end

% 关闭进度条
close(h);

% 绘制波德图
magnitude = 20 * log10(abs(GHZs_total));  % 幅度，转换为dB
phase = angle(GHZs_total) * (180 / pi);   % 相位，转换为角度

figure;
subplot(2,1,1);
semilogx(frequency, magnitude);
xlabel('Frequency (Hz)');
ylabel('Magnitude (dB)');
title('Bode Plot - Magnitude');
grid on;

subplot(2,1,2);
semilogx(frequency, phase);
xlabel('Frequency (Hz)');
ylabel('Phase (degrees)');
title('Bode Plot - Phase');
grid on;
```

### 关键改动说明

- **去除累加**：在原来的代码中，`GHZs_total` 被不断累加，这会导致不同频率点的传递函数叠加在一起，这并不反映实际的频率响应。在修改后的代码中，`GHZs_total(i)` 直接存储当前频率点的计算结果，而不是累加其他频率点的结果。
  
- **独立计算每个频率点**：这样，每个频率点的传递函数 `GHZs_total(i)` 反映了电路在该频率下的真实行为。

### 总结

通过去除累加操作，代码将准确计算并展示电路在每个频率点的响应。这样绘制出的波德图将正确反映电路的频率响应特性。如果你运行这个修改后的代码，你应该可以得到一个反映电路实际行为的波德图。
