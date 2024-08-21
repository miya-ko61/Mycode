为了在每次循环中打印出所有 `1x1` 传递函数对象的状态，我们可以在 `for` 循环内使用 `disp` 函数来显示 `Z1`, `Z2`, `Z3`, `GH`, `GHZs_total` 等传递函数的内容。你可以将以下代码添加到现有代码中以打印这些对象的状态。

### 修改后的代码示例：

```matlab
% 清除工作区和命令行
clc;
clear;

% 读取 Excel 表格数据
disp('正在读取数据...');
data = readtable('data.xlsx');

% 提取前10个频率、增益和相位数据
num_points = 10;
frequency = data.Frequency_Hz(1:num_points);
gain_magnitude = data.Trace_1_Gain_Magnitude_dB(1:num_points);
gain_phase = data.Trace_2_Gain_Phase(1:num_points);

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

% 初始化传递函数对象
GHZs_total = tf(0);  % 初始化为空的传递函数对象

% 创建进度条
h = waitbar(0, '正在计算传递函数...');

% 计算前10个频率点的传递函数并在每个循环中打印出状态
for i = 1:num_points
    GH = (1 - Gaef(i)*Z3/(Z1 + Z3)) / (Zin + Z3 + (Z1*Z3)/(Z1 + Z3));
    Zs = s*L + s^2*Cs*L/(Rs1 + Rs2);
    
    % 打印当前传递函数状态
    disp(['循环第 ', num2str(i), ' 次:']);
    disp('Z1:'); disp(Z1);
    disp('Z2:'); disp(Z2);
    disp('Z3:'); disp(Z3);
    disp('GH:'); disp(GH);
    disp('GHZs_total (累加前):'); disp(GHZs_total);

    % 将当前频率下的传递函数累加到总传递函数
    GHZs_total = GHZs_total + (GH + Zs);
    
    % 打印累加后的 GHZs_total
    disp('GHZs_total (累加后):'); disp(GHZs_total);
    
    % 更新进度条
    waitbar(i / num_points, h);
end

% 关闭进度条
close(h);

% 波德图绘制
P = bodeoptions;  % 获取波德图选项
P.FreqUnits = 'Hz';  % 设置频率单位为Hz
bodeplot(GHZs_total, P);  % 绘制波德图
grid on;  % 显示网格
```

### 说明：

1. **循环内打印状态**：
   - 每次循环中，在计算和累加传递函数之前和之后，我们使用 `disp` 函数打印出 `Z1`, `Z2`, `Z3`, `GH`, 以及 `GHZs_total` 的当前状态。这样，你可以看到每个传递函数对象在每次循环中的变化。

2. **打印前后状态**：
   - 特别注意在 `GHZs_total` 累加前和累加后的状态，这样你可以直观地了解传递函数如何随着每个数据点逐步变化和累积。

3. **只处理前10个数据点**：
   - 为了更方便调试和观察，只处理前 10 个数据点，并在每次循环中打印相关信息。

### 运行效果：
当你运行这个脚本时，MATLAB 命令窗口会显示每次循环的详细信息，包括每个传递函数在累加前后的状态。这将帮助你更好地理解 MATLAB 中传递函数对象的动态行为，以及它们如何在循环中随着数据点变化而逐步构建。
