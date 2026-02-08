#!/bin/bash

echo "========================================"
echo "VIP Video Player - WSL2 Auto Setup"
echo "========================================"
echo ""

PROJECT_DIR="/mnt/c/Users/Administrator/Desktop/电影 - 副本"

echo "[1/8] Updating system packages..."
sudo apt-get update -y
if [ $? -ne 0 ]; then
    echo "Error: Failed to update packages"
    exit 1
fi
echo "✓ System packages updated"
echo ""

echo "[2/8] Installing system dependencies..."
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

if [ $? -ne 0 ]; then
    echo "Error: Failed to install system dependencies"
    exit 1
fi
echo "✓ System dependencies installed"
echo ""

echo "[3/8] Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "Error: Failed to upgrade pip"
    exit 1
fi
echo "✓ pip upgraded"
echo ""

echo "[4/8] Installing Python dependencies..."
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

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"
echo ""

echo "[5/8] Changing to project directory..."
cd "$PROJECT_DIR" || {
    echo "Error: Failed to change to project directory"
    exit 1
}
echo "✓ Changed to project directory"
echo ""

echo "[6/8] Initializing Buildozer (this may take a while)..."
buildozer android init
echo "✓ Buildozer initialized"
echo ""

echo "[7/8] Starting APK build..."
echo "This will take 1-2 hours on first run"
echo "(downloading Android SDK, NDK, etc.)"
echo ""
read -p "Press Enter to start building, or Ctrl+C to cancel..."

buildozer android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Build Successful!"
    echo "========================================"
    echo ""
    echo "APK file location: bin/"
    ls -lh bin/*.apk 2>/dev/null || echo "APK file not found"
    echo ""
    echo "Copying APK to Windows..."
    cp bin/*.apk "$PROJECT_DIR/" 2>/dev/null && echo "✓ APK copied to project directory" || echo "Copy failed, please copy manually"
    echo ""
    echo "Build completed successfully!"
else
    echo ""
    echo "========================================"
    echo "✗ Build Failed"
    echo "========================================"
    echo ""
    echo "Please check the error messages above"
    echo "Common issues:"
    echo "  - Network connection problems"
    echo "  - Insufficient disk space"
    echo "  - Missing dependencies"
    echo ""
    echo "To rebuild with verbose output:"
    echo "  buildozer android debug --verbose"
fi

echo ""
echo "Press Enter to exit..."
read
