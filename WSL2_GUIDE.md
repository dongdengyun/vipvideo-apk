# WSL2打包指南

## 当前状态

✅ **WSL2安装已启动**

系统正在安装WSL2虚拟机平台，这可能需要几分钟时间。

## 重要提示

**安装完成后，必须重启电脑才能继续！**

## 完整的WSL2打包流程

### 第一步：完成WSL2安装

1. 等待当前安装完成（虚拟机平台安装）
2. **重启电脑**（必须！）
3. 重启后，系统会自动完成Ubuntu安装
4. 首次启动Ubuntu时，需要设置用户名和密码

### 第二步：配置Ubuntu环境

重启并完成Ubuntu安装后，打开PowerShell或命令提示符，运行：

```bash
# 进入WSL2环境
wsl
```

在Ubuntu中运行以下命令：

```bash
# 更新系统包
sudo apt-get update && sudo apt-get upgrade -y

# 安装必要的依赖
sudo apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    python3 \
    python3-dev \
    python3-pip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    automake \
    zip \
    unzip \
    libltdl-dev \
    libx11-dev \
    x11proto-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev

# 升级pip
python3 -m pip install --upgrade pip setuptools wheel

# 安装Python依赖
python3 -m pip install \
    kivy \
    kivy-deps.angle \
    kivy-deps.glew \
    kivy-deps.sdl2 \
    pyjnius \
    buildozer \
    beautifulsoup4 \
    requests \
    cython
```

### 第三步：进入项目目录

```bash
# 进入Windows项目目录（在WSL2中）
cd /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本
```

### 第四步：运行打包脚本

```bash
# 运行自动打包脚本
bash build_in_wsl.sh
```

或者手动执行：

```bash
# 初始化Buildozer（首次运行）
buildozer android init

# 开始打包APK（首次运行需要1-2小时）
buildozer android debug
```

### 第五步：获取APK

打包完成后，APK文件位于：
```
bin/
└── vipvideo-1.0.0-arm64-v8a-debug.apk
```

将APK文件复制到Windows：
```bash
cp bin/*.apk /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本/
```

## 快速命令参考

### 从Windows进入WSL2
```bash
wsl
```

### 从WSL2返回Windows
```bash
exit
```

### 在WSL2中运行Windows命令
```bash
# 例如：打开Windows文件管理器
explorer.exe .
```

### 在Windows中运行WSL2命令
```bash
# 例如：在WSL2中运行打包脚本
wsl bash -c "cd /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本 && ./build_in_wsl.sh"
```

## 常见问题

### Q1: 重启后如何知道Ubuntu安装完成？

**A:** 打开PowerShell，运行：
```bash
wsl --list --verbose
```
如果看到Ubuntu列表，说明安装完成。

### Q2: 首次启动Ubuntu需要做什么？

**A:**
1. 系统会提示创建用户账户
2. 输入用户名（建议：user）
3. 输入密码（需要输入两次，不会显示）
4. 完成后就可以使用Ubuntu了

### Q3: 如何在WSL2中访问Windows文件？

**A:** Windows文件系统挂载在 `/mnt/` 下：
```
C:盘 -> /mnt/c/
D:盘 -> /mnt/d/
```

你的项目目录：
```
/mnt/c/Users/Administrator/Desktop/电影 - 副本
```

### Q4: 打包需要多长时间？

**A:**
- **首次打包**：1-2小时（需要下载Android SDK、NDK等）
- **后续打包**：10-20分钟（使用缓存）

### Q5: 打包失败怎么办？

**A:** 检查以下几点：
1. 网络连接是否正常
2. 磁盘空间是否充足（至少10GB）
3. Python版本是否为3.7+
4. 查看详细错误信息：
```bash
buildozer android debug --verbose
```

### Q6: 如何清理缓存重新打包？

**A:**
```bash
# 清理Buildozer缓存
buildozer android clean

# 删除整个构建目录
rm -rf .buildozer
```

### Q7: 如何查看打包进度？

**A:** 打包过程中会显示详细进度，包括：
- 下载进度条
- 编译进度
- 打包进度

### Q8: 如何减小APK体积？

**A:** 编辑 `buildozer.spec` 文件：
```
android.archs = arm64-v8a  # 只包含64位架构
```

## 性能优化建议

### 1. 使用SSD存储
将WSL2和项目文件放在SSD上可以显著提升速度。

### 2. 增加WSL2内存
编辑 `%UserProfile%\.wslconfig` 文件：
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

### 3. 使用代理加速下载
在 `buildozer.spec` 中配置：
```
# 如果需要使用代理
# export http_proxy=http://proxy.example.com:8080
# export https_proxy=http://proxy.example.com:8080
```

## 故障排除

### 问题1：WSL2启动失败

**解决方案：**
```bash
# 重启WSL2
wsl --shutdown
wsl
```

### 问题2：权限错误

**解决方案：**
```bash
# 修复文件权限
sudo chown -R $USER:$USER /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本
```

### 问题3：网络连接问题

**解决方案：**
```bash
# 重启网络服务
sudo service networking restart
```

### 问题4：磁盘空间不足

**解决方案：**
```bash
# 清理APT缓存
sudo apt-get clean
sudo apt-get autoremove

# 清理pip缓存
pip cache purge
```

## 下一步

完成WSL2安装和重启后：

1. **打开PowerShell**
2. **运行**：`wsl`
3. **按照第二步配置Ubuntu环境**
4. **运行打包脚本**

祝你打包顺利！🎉
