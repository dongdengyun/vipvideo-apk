# WSL2打包 - 完整操作指南

## 📋 当前状态

✅ **WSL2安装已启动**
- 虚拟机平台正在安装中
- 系统会自动完成后续安装

## ⚠️ 重要提醒

**安装完成后，必须重启电脑！**

## 🚀 快速开始（3步完成）

### 第1步：等待安装完成并重启

1. 等待WSL2安装完成（可能需要5-10分钟）
2. **重启电脑**（必须！）
3. 重启后，系统会自动完成Ubuntu安装
4. 首次启动Ubuntu时，设置用户名和密码

### 第2步：运行自动设置脚本

重启后，双击运行：

```
run_wsl2_setup.bat
```

这个脚本会自动完成所有配置和打包！

### 第3步：等待打包完成

- 配置环境：15-30分钟
- 首次打包：1-2小时（下载SDK/NDK）
- 后续打包：10-20分钟

## 📝 详细步骤说明

### 步骤1：完成WSL2安装

#### 检查安装状态

在PowerShell中运行：
```bash
wsl --status
```

如果显示WSL2状态，说明安装完成。

#### 重启电脑

**必须重启才能继续！**

重启后，系统会自动：
1. 完成WSL2功能安装
2. 安装Ubuntu
3. 首次启动时提示设置用户账户

#### 设置Ubuntu账户

首次启动Ubuntu时：
1. 输入用户名（建议：`user`）
2. 输入密码（需要输入两次，不会显示）
3. 完成设置

### 步骤2：运行自动设置脚本

#### 方式A：双击运行（推荐）

双击运行 `run_wsl2_setup.bat`

这个脚本会自动：
1. 检查WSL2和Ubuntu状态
2. 复制设置脚本到WSL2
3. 运行自动配置
4. 执行APK打包

#### 方式B：手动运行

如果自动脚本失败，可以手动执行：

```bash
# 1. 进入WSL2
wsl

# 2. 进入项目目录
cd /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本

# 3. 运行设置脚本
bash wsl2_auto_setup.sh
```

### 步骤3：等待打包完成

#### 打包过程

自动设置脚本会执行以下操作：

1. **更新系统包**（5-10分钟）
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **安装系统依赖**（10-15分钟）
   - 构建工具（build-essential, cmake等）
   - 多媒体库（ffmpeg, gstreamer等）
   - Python和Java（python3, openjdk-17-jdk等）

3. **安装Python依赖**（5-10分钟）
   ```bash
   pip install kivy buildozer beautifulsoup4 requests
   ```

4. **初始化Buildozer**（2-5分钟）
   ```bash
   buildozer android init
   ```

5. **打包APK**（1-2小时，首次运行）
   - 下载Android SDK（约1GB）
   - 下载Android NDK（约1GB）
   - 编译应用
   - 生成APK

#### 打包进度监控

打包过程中会显示：
- 下载进度条
- 编译进度
- 打包进度

#### 完成标志

看到以下信息表示成功：
```
========================================
✓ Build Successful!
========================================

APK file location: bin/
```

### 步骤4：获取APK

#### APK位置

打包完成后，APK文件位于：
```
bin/
└── vipvideo-1.0.0-arm64-v8a-debug.apk
```

#### 复制到Windows

自动脚本会尝试复制APK到项目目录，如果失败可以手动复制：

```bash
# 在WSL2中
cp bin/*.apk /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本/
```

或者在Windows中直接访问：
```
\\wsl$\Ubuntu\home\用户名\项目目录\bin\
```

## 🔧 故障排除

### 问题1：WSL2安装失败

**症状：** 运行 `wsl --install` 后没有反应或报错

**解决方案：**
```bash
# 检查Windows版本
winver

# 确保Windows版本为2004或更高
# 如果不是，更新Windows
```

### 问题2：Ubuntu安装卡住

**症状：** 重启后Ubuntu没有自动安装

**解决方案：**
```bash
# 手动触发安装
wsl --install -d Ubuntu

# 等待安装完成
# 然后重启
```

### 问题3：无法进入WSL2

**症状：** 运行 `wsl` 命令报错

**解决方案：**
```bash
# 重启WSL2服务
wsl --shutdown
wsl
```

### 问题4：打包失败

**症状：** 打包过程中出现错误

**解决方案：**

1. 检查网络连接：
```bash
ping google.com
```

2. 检查磁盘空间：
```bash
df -h
# 确保至少有10GB可用空间
```

3. 查看详细错误：
```bash
buildozer android debug --verbose
```

4. 清理缓存重试：
```bash
buildozer android clean
buildozer android debug
```

### 问题5：权限错误

**症状：** 运行脚本时提示权限不足

**解决方案：**
```bash
# 给脚本添加执行权限
chmod +x wsl2_auto_setup.sh

# 使用sudo运行
sudo bash wsl2_auto_setup.sh
```

### 问题6：网络下载慢

**症状：** 下载SDK/NDK速度很慢

**解决方案：**

1. 使用国内镜像（如果在中国）：
编辑 `~/.buildozer/android/platform/android-21/` 下的配置文件

2. 配置代理：
```bash
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080
```

## 📊 性能优化

### 1. 增加WSL2内存

创建或编辑 `%UserProfile%\.wslconfig` 文件：
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

然后重启WSL2：
```bash
wsl --shutdown
wsl
```

### 2. 使用SSD存储

将WSL2和项目文件放在SSD上可以显著提升速度。

### 3. 减小APK体积

编辑 `buildozer.spec` 文件：
```
android.archs = arm64-v8a  # 只包含64位架构
```

## 🎯 快速命令参考

### WSL2常用命令

```bash
# 进入WSL2
wsl

# 退出WSL2
exit

# 重启WSL2
wsl --shutdown

# 查看WSL2状态
wsl --status

# 查看已安装的发行版
wsl --list --verbose

# 从Windows运行WSL2命令
wsl bash -c "命令"
```

### Ubuntu常用命令

```bash
# 更新系统
sudo apt-get update && sudo apt-get upgrade -y

# 安装包
sudo apt-get install 包名

# 查看磁盘空间
df -h

# 查看进程
top

# 查看日志
journalctl -f
```

### Buildozer常用命令

```bash
# 初始化
buildozer android init

# 打包调试版本
buildozer android debug

# 打包发布版本
buildozer android release

# 清理构建
buildozer android clean

# 详细输出
buildozer android debug --verbose

# 更新依赖
buildozer android update
```

## 📚 相关文档

- [WSL2官方文档](https://docs.microsoft.com/zh-cn/windows/wsl/)
- [Buildozer官方文档](https://buildozer.readthedocs.io/)
- [Kivy官方文档](https://kivy.org/doc/stable/)
- [项目README](README.md)
- [快速开始指南](QUICKSTART.md)

## 💡 提示和技巧

1. **首次打包时间长是正常的**
   - 需要下载Android SDK和NDK
   - 后续打包会快很多

2. **保持网络稳定**
   - 打包过程需要持续的网络连接
   - 断网可能导致打包失败

3. **定期更新**
   - 定期运行 `sudo apt-get update`
   - 定期更新Python包

4. **备份APK**
   - 打包成功后立即备份APK
   - 避免重复打包

5. **使用日志**
   - 保存打包日志以便调试
   - 使用 `--verbose` 选项获取详细信息

## ✅ 检查清单

在开始打包前，确保：

- [ ] WSL2已安装并正常运行
- [ ] Ubuntu已安装并配置完成
- [ ] 网络连接稳定
- [ ] 磁盘空间充足（至少10GB）
- [ ] 已阅读本文档
- [ ] 已准备好等待1-2小时（首次打包）

## 🎉 开始打包

重启电脑后，双击运行：

```
run_wsl2_setup.bat
```

祝你打包顺利！
