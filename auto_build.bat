@echo off
chcp 65001 >nul
echo ========================================
echo VIP Video Player - Auto Build Tool
echo ========================================
echo.

echo [1/5] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found, please install Python 3.7+
    pause
    exit /b 1
)
echo Python environment OK
echo.

echo [2/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Warning: Dependency installation may have issues, but continuing...
)
echo Dependencies check completed
echo.

echo [3/5] Checking Java environment...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo Java JDK not found
    echo.
    echo Please choose installation method:
    echo 1. Download and install JDK automatically (recommended)
    echo 2. Install manually and continue
    echo 3. Skip Java check (may cause build failure)
    echo.
    set /p choice="Please enter option (1/2/3): "
    
    if "%choice%"=="1" (
        echo Downloading JDK...
        powershell -Command "Invoke-WebRequest -Uri 'https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_windows-x64_bin.zip' -OutFile 'jdk.zip'"
        echo Extracting JDK...
        powershell -Command "Expand-Archive -Path 'jdk.zip' -DestinationPath '.'"
        set JAVA_HOME=%cd%\jdk-11.0.2
        set PATH=%PATH%;%JAVA_HOME%\bin
        echo JDK installation completed
    ) else if "%choice%"=="2" (
        echo Please install JDK manually and press any key to continue...
        pause
    ) else if "%choice%"=="3" (
        echo Skipping Java check...
    )
) else (
    echo Java environment OK
)
echo.

echo [4/5] Checking build environment...
echo.
echo Buildozer requires one of the following environments:
echo.
echo 1. Linux environment (recommended)
echo    - Ubuntu 20.04 or higher
echo    - WSL2 (Windows Subsystem for Linux)
echo    - Docker container
echo.
echo 2. Windows environment (requires additional configuration)
echo    - Need to manually install Android SDK, NDK
echo    - Complex configuration, not recommended
echo.
echo Checking available environments...
echo.

wsl --list --verbose >nul 2>&1
if %errorlevel% equ 0 (
    echo WSL environment detected
    echo.
    echo Use WSL environment for packaging? (Y/N)
    set /p use_wsl="Please choose: "
    if /i "%use_wsl%"=="Y" (
        echo.
        echo Switching to WSL environment...
        wsl bash -c "cd /mnt/c/Users/Administrator/Desktop/电影\ -\ 副本 && ./build_in_wsl.sh"
        pause
        exit /b 0
    )
)

docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Docker environment detected
    echo.
    echo Use Docker environment for packaging? (Y/N)
    set /p use_docker="Please choose: "
    if /i "%use_docker%"=="Y" (
        echo.
        echo Building Docker image...
        docker build -t buildozer .
        echo.
        echo Packaging APK...
        docker run --rm -v %cd%:/app buildozer android debug
        pause
        exit /b 0
    )
)

echo.
echo No suitable build environment found
echo.
echo ========================================
echo Recommended solutions:
echo ========================================
echo.
echo Solution 1: Install WSL2 (recommended)
echo   1. Run in PowerShell: wsl --install
echo   2. Restart computer
echo   3. Run this script again
echo.
echo Solution 2: Use online build service
echo   1. Visit https://github.com/kivy/buildozer
echo   2. Use GitHub Actions for automatic packaging
echo.
echo Solution 3: Use virtual machine
echo   1. Download Ubuntu VM image
echo   2. Install Buildozer
echo   3. Execute build command
echo.
echo ========================================
echo.
echo Press any key to exit...
pause >nul
