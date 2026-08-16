# ClawGod 卸载与恢复指南

> 适用于 ClawGod v2.1.220 / Windows 环境

## 一、概述

ClawGod 安装时做了以下改动：

| 改动 | 位置 |
|------|------|
| 备份原始 claude.exe | `%USERPROFILE%\.local\bin\claude.orig.exe` |
| 创建 ClawGod 启动器 | `%USERPROFILE%\.local\bin\claude.cmd` |
| 创建补丁目录 | `%USERPROFILE%\.clawgod\`（约 20 MB） |
| 添加到用户 PATH | `%USERPROFILE%\.local\bin` |
| 修改 VSCode 设置 | `%APPDATA%\Code\User\settings.json` → `claude.path` |
| 安装 Bun 运行时 | `%USERPROFILE%\.bun\`（如未安装） |

卸载时按需决定是否保留 Bun（其他项目可能用到）。

---

## 二、卸载步骤

### 步骤 1：恢复原始 claude.exe

打开 **PowerShell** 或 **CMD**：

```powershell
cd $env:USERPROFILE\.local\bin

# 删除 ClawGod 启动器
del claude.cmd

# 恢复原始 claude.exe
ren claude.orig.exe claude.exe
```

### 步骤 2：删除 ClawGod 目录

```powershell
rmdir /s /q $env:USERPROFILE\.clawgod
```

### 步骤 3：恢复 NPM 全局安装的 claude

ClawGod 安装前，系统中有一个 npm 全局安装的 `claude`，路径在：
- `%APPDATA%\npm\claude`
- `%APPDATA%\npm\claude.cmd`
- `%APPDATA%\npm\claude.ps1`

也可能在：
- `d:\npm_global\claude`
- `d:\npm_global\claude.cmd`
- `d:\npm_global\claude.ps1`

重新安装：

```powershell
npm install -g @anthropic-ai/claude-code
```

### 步骤 4：删除 VSCode 中的 ClawGod 路径配置

VSCode 的 `settings.json` 中有一行 `claude.path` 指向 ClawGod。去掉它：

文件位置：`%APPDATA%\Code\User\settings.json`

**手动删除：**

`Ctrl+,` → 搜索 `claude.path` → 点击左侧 × 删除该配置。

**或者直接编辑文件：** 删除这一行：

```json
"claude.path": "C:\\Users\\shuai\\.local\\bin\\claude.cmd",
```

然后 `Ctrl+Shift+P` → `Developer: Reload Window`，VSCode 扩展恢复使用内置原版。

### 步骤 5：（可选）清理 PATH

ClawGod 安装时在用户 PATH 中添加了 `%USERPROFILE%\.local\bin`。如果该目录下没有其他需要的工具，可以从 PATH 中移除：

1. `Win + R` → `sysdm.cpl` → 高级 → 环境变量
2. 在 **用户变量** 中找到 `Path`
3. 删除 `%USERPROFILE%\.local\bin` 这一条
4. 确定保存

### 步骤 6：重启终端

```powershell
# 验证恢复
claude --version
```

应该显示原始 Claude Code 版本号，且 logo 为橙色（不是 ClawGod 的绿色）。

---

## 三、一键卸载脚本

将以下内容保存为 `uninstall-clawgod.ps1`，以 **管理员身份** 在 PowerShell 中运行：

```powershell
$ErrorActionPreference = "Stop"
$localBin = "$env:USERPROFILE\.local\bin"
$clawgodDir = "$env:USERPROFILE\.clawgod"

Write-Host "=== ClawGod 卸载脚本 ===" -ForegroundColor Yellow

# 1. 恢复 claude.exe
if (Test-Path "$localBin\claude.orig.exe") {
    Remove-Item "$localBin\claude.cmd" -Force -ErrorAction SilentlyContinue
    Rename-Item "$localBin\claude.orig.exe" "$localBin\claude.exe"
    Write-Host "[OK] 恢复 claude.exe" -ForegroundColor Green
} else {
    Write-Host "[!!] 未找到 claude.orig.exe 备份" -ForegroundColor Red
}

# 2. 删除 ClawGod 目录
if (Test-Path $clawgodDir) {
    Remove-Item -Recurse -Force $clawgodDir
    Write-Host "[OK] 删除 .clawgod" -ForegroundColor Green
}

# 3. 重装 npm claude
Write-Host "[..] 重装 @anthropic-ai/claude-code ..."
npm install -g @anthropic-ai/claude-code

# 4. 删除 VSCode claude.path 配置
$vsSettings = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $vsSettings) {
    $content = Get-Content $vsSettings -Raw | ForEach-Object { $_ -replace '"claude\.path":\s*"C:\\Users\\shuai\\.local\\bin\\claude\.cmd",?\s*', '' }
    Set-Content $vsSettings -Value $content
    Write-Host "[OK] 删除 VSCode claude.path 配置" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 卸载完成 ===" -ForegroundColor Green
Write-Host "重启终端后运行 claude --version 验证"
Write-Host "VSCode 中请 Ctrl+Shift+P → Reload Window"
```

---

## 五、（可选）完全卸载 Bun

```powershell
# 删除 Bun 二进制
rmdir /s /q $env:USERPROFILE\.bun

# 从 PATH 中移除 %USERPROFILE%\.bun\bin
# 同上：系统属性 → 环境变量 → Path → 删除对应条目
```

---

## 六、各组件路径速查

| 组件 | 路径 |
|------|------|
| ClawGod 补丁目录 | `C:\Users\shuai\.clawgod\` |
| ClawGod 启动器 | `C:\Users\shuai\.local\bin\claude.cmd` |
| VSCode claude.path | `C:\Users\shuai\AppData\Roaming\Code\User\settings.json` → `"claude.path"` 条目 |
| 原始 claude.exe | `C:\Users\shuai\.local\bin\claude.orig.exe` |
| NPM claude | `C:\Users\shuai\AppData\Roaming\npm\claude.cmd` |
| NPM claude（备用位置） | `d:\npm_global\claude.cmd` |
| Bun | `C:\Users\shuai\.bun\bin\bun.exe` |
| ripgrep | `%LOCALAPPDATA%\Microsoft\WinGet\Packages\BurntSushi.ripgrep.MSVC_*\rg.exe` |
