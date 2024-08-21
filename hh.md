从错误信息来看，问题出在 `bodeplot` 函数的使用上。MATLAB 中的 `bodeplot` 函数通常用于绘制传递函数对象（`tf`）的波德图，而在这个上下文中，我们已经将计算结果存储在数值数组 `GHZs_total` 中，因此无法直接使用 `bodeplot` 来绘制。

### 修改代码以使用 `semilogx` 绘制波德图

我们可以使用 `semilogx` 函数来绘制以对数频率为横轴的幅度和相位图。以下是如何修改代码以绘制波德图：

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

### 关键改动说明：

1. **使用 `semilogx` 绘制图形**：
   - 我们用 `semilogx` 函数来绘制波德图，它允许在对数频率轴上绘制线性数据。
   - 绘制幅度响应时，使用 `20 * log10(abs(GHZs_total))` 将幅度转换为 dB。
   - 绘制相位响应时，使用 `angle(GHZs_total) * (180 / pi)` 将相位转换为角度。

2. **保持传递函数的频率依赖性**：
   - 通过计算每个频率点上的复数 `GHZs_total`，可以准确绘制出波德图的幅度和相位响应。

### 总结：

通过这些调整，程序现在能够正确计算并绘制电路的波德图，反映了电路在不同频率下的响应特性。如果你再次运行这个代码，你应该可以看到每个频率点上计算出的波德图，它准确地表示了电路的幅度和相位响应。
