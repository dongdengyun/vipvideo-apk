#!/bin/bash

echo "========================================"
echo "VIP追剧神器 - WSL自动打包脚本"
echo "========================================"
echo ""

cd /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本 || exit 1

echo "[1/6] 更新系统包..."
sudo apt-get update -y

echo ""
echo "[2/6] 安装必要的依赖..."
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

echo ""
echo "[3/6] 升级pip..."
python3 -m pip install --upgrade pip setuptools wheel

echo ""
echo "[4/6] 安装Python依赖..."
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

echo ""
echo "[5/6] 初始化Buildozer (首次运行会下载Android SDK/NDK，需要较长时间)..."
buildozer android init

echo ""
echo "[6/6] 开始打包APK..."
echo "注意: 首次打包需要下载Android SDK、NDK等工具，可能需要1-2小时"
echo ""

read -p "按Enter键开始打包，或Ctrl+C取消..."

buildozer android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ 打包成功！"
    echo "========================================"
    echo ""
    echo "APK文件位置: bin/"
    ls -lh bin/*.apk 2>/dev/null || echo "未找到APK文件"
    echo ""
    echo "将APK文件复制到Windows:"
    cp bin/*.apk /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本/ 2>/dev/null && echo "✓ 已复制到项目目录" || echo "复制失败，请手动复制"
    echo ""
else
    echo ""
    echo "========================================"
    echo "✗ 打包失败"
    echo "========================================"
    echo ""
    echo "请检查错误信息并重试"
    echo ""
fi

read -p "按Enter键退出..."
