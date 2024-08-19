是的，您可以通过 PowerShell 命令行直接安装 Node.js。以下是使用 PowerShell 安装 Node.js 的步骤：

1. **打开 PowerShell**：
   在 Windows 上，您可以按 `Win + X` 然后选择“Windows PowerShell”来打开 PowerShell 窗口。

2. **安装 Node.js**：
   您可以使用包管理工具 Chocolatey 来安装 Node.js。首先，您需要确保已安装 Chocolatey。若尚未安装，可以使用以下命令安装 Chocolatey：

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

3. **通过 Chocolatey 安装 Node.js**：
   Chocolatey 安装好后，可以使用以下命令来安装 Node.js：

   ```powershell
   choco install nodejs
   ```

   这将安装最新版本的 Node.js 及其附带的 npm（Node Package Manager）。

4. **验证安装**：
   安装完成后，您可以通过以下命令验证 Node.js 和 npm 是否安装成功：

   ```powershell
   node -v
   npm -v
   ```

   这两个命令分别会返回您安装的 Node.js 和 npm 的版本号。

通过这些步骤，您可以直接在 PowerShell 中安装 Node.js。如果您不想使用 Chocolatey，也可以从 [Node.js 官方网站](https://nodejs.org/) 下载并安装。
