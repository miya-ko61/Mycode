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
