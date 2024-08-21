下面是一个完整的 MATLAB 脚本示例，它假设文件 `data.xlsx` 存放在当前文件夹中，读取其中的数据，并根据每个频率点动态计算 `Gaef`，然后绘制相应的波德图。

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

% 创建s变量
s = tf('s');

% 定义常量（假设这些值不变）
Cinj = 4700e-12;
Rinj5 = 5;
RINJ = 5e7;

C11 = 8.2e-9;
R3 = 49.9;
R5 = 1e3;

C12 = 4.7e-9;
R4 = 698;
R6 = 200;

L = 1e-7;
Rs1 = 1000;
Rs2 = 500;
Cs = 1e-7;

% 计算输入阻抗Zin
Zin = (RINJ/(s*Cinj))/(RINJ+1/(s*Cinj));

% 计算 Z1
Z1 = ((R3+1/(s*C11))*R5)/(R3+1/(s*C11)+R5);

% 计算 Z3
Z3 = (R4*(s*C12))/(R4+1/(s*C12));

% 初始化波德图选项
P = bodeoptions;
P.FreqUnits = 'Hz';

% 遍历每个频率点，计算 Gaef，绘制波德图
for i = 1:length(frequency)
    % 将 dB 转换为线性值
    selected_gain = 10^(gain_magnitude(i)/20);
    % 将相位角度转换为弧度
    selected_phase = deg2rad(gain_phase(i));
    
    % 计算 Gaef
    Gaef = selected_gain * cos(selected_phase);
    
    % 计算 GH 和 Zs
    GH = (1 - Gaef*Z2/(Z1+Z2))/(Zin+Z3+(Z1*Z2/(Z1+Z2)));
    Zs = s*L + s^2*Cs + (Rs1*Rs2)/(Rs1+Rs2);
    GHZs = GH + Zs;
    
    % 绘制波德图
    bodeplot(GHZs, P);
    hold on; % 保持当前图，继续绘制下一组数据
end

% 显示网格
grid on;
```

### 脚本说明：

1. **数据读取**：
   - 使用 `readtable('data.xlsx')` 读取 Excel 文件中的数据，并提取相应列的值。

2. **变量定义**：
   - 将各个电阻、电容、以及电感的常量定义为固定值。
   - 使用 `tf('s')` 创建拉普拉斯变换变量 `s`。

3. **遍历每个频率点**：
   - 对于每个频率点，从表格中提取增益和相位值，并计算对应的 `Gaef`。
   - 计算 `GH` 和 `Zs`，然后结合得到 `GHZs`。
   - 使用 `bodeplot` 绘制波德图，每次循环都将结果叠加在同一张图上。

4. **绘制波德图**：
   - `hold on;` 用于保持绘图窗口打开，以便在每个频率点绘制完波德图后，继续绘制下一个频率点的结果。

5. **最后**：
   - 脚本在处理每个频率点时都会更新并叠加波德图，因此你可以在一张图上看到整个频率范围内的系统响应。

确保你的 Excel 文件 `data.xlsx` 的列名与脚本中的变量名称相对应。如果列名不同，你需要相应地调整变量的提取部分。如果你有其他问题或需要进一步调整脚本，请告知。

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

% 定义常量（假设这些值不变）
Cinj = 4700e-12;
RINJ = 5e7;
C11 = 8.2e-9;
R3 = 49.9;
R5 = 1e3;
C12 = 4.7e-9;
R4 = 698;
R6 = 200;
L = 1e-7;
Rs1 = 1000;
Rs2 = 500;
Cs = 1e-7;

% 计算输入阻抗Zin
Zin = (RINJ/(s*Cinj))/(RINJ+1/(s*Cinj));

% 计算 Z1
Z1 = ((R3+1/(s*C11))*R5)/(R3+1/(s*C11)+R5);

% 计算 Z3
Z3 = (R4*(s*C12))/(R4+1/(s*C12));

% 初始化总传递函数
GHZs_total = 0;

% 计算每个频率点的传递函数并累加
for i = 1:length(frequency)
    % 计算 GH 和 Zs
    GH = (1 - Gaef(i)*Z3/(Z1+Z3))/(Zin+Z3+(Z1*Z3/(Z1+Z3)));
    Zs = s*L + s^2*Cs + (Rs1*Rs2)/(Rs1+Rs2);
    GHZs = GH + Zs;

    % 累加每个频率点的结果
    GHZs_total = GHZs_total + GHZs;
end

% 波德图绘制
P = bodeoptions;
P.FreqUnits = 'Hz';
bodeplot(GHZs_total, P);
grid on;
