# VIP追剧神器 - 快速打包指南

## 当前状态

✓ **已完成：**
- Kivy应用开发完成
- Buildozer配置文件已创建
- Python依赖已安装
- 自动打包工具已创建

✗ **需要配置：**
- Linux打包环境（WSL2/Docker/虚拟机）
- Java JDK（用于Android构建）

## 快速开始（3步完成打包）

### 方案1：使用WSL2（推荐）

```bash
# 1. 安装WSL2（只需运行一次）
wsl --install

# 2. 重启电脑后，运行自动打包脚本
python auto_build.py
# 选择选项 3 查看手动说明，然后按照说明操作

# 3. 或直接在WSL中运行
bash build_in_wsl.sh
```

### 方案2：使用Docker

```bash
# 1. 安装Docker Desktop
# 下载地址：https://www.docker.com/products/docker-desktop

# 2. 运行自动打包脚本
python auto_build.py
# 选择选项 2 使用Docker打包

# 3. 或手动运行
docker build -t buildozer .
docker run --rm -v %cd%:/app buildozer
```

### 方案3：使用GitHub Actions（最简单）

1. 将项目推送到GitHub
2. 在GitHub仓库中启用Actions
3. 自动触发打包流程
4. 从Actions页面下载APK

详细配置见：[.github/workflows/build-apk.yml](.github/workflows/build-apk.yml)

## 详细步骤说明

### 第一步：检查环境

```bash
python check_environment.py
```

这会检查：
- Python版本
- 必要的Python包
- Java环境
- 项目文件完整性
- 可用的打包环境

### 第二步：安装依赖

```bash
pip install -r requirements.txt
```

已安装的包：
- kivy >= 2.1.0
- kivy-deps.angle >= 0.3.2
- kivy-deps.glew >= 0.3.1
- kivy-deps.sdl2 >= 0.4.5
- pyjnius >= 1.4.2
- beautifulsoup4 >= 4.11.1
- requests >= 2.28.0
- buildozer >= 1.5.0

### 第三步：选择打包方式

#### 方式A：自动打包脚本

```bash
python auto_build.py
```

脚本会：
1. 检查Python环境
2. 安装依赖
3. 检查Java环境
4. 检测可用的打包环境
5. 引导完成打包

#### 方式B：手动打包

**在WSL2中：**
```bash
bash build_in_wsl.sh
```

**在Docker中：**
```bash
docker build -t buildozer .
docker run --rm -v %cd%:/app buildozer
```

**在Linux中：**
```bash
buildozer android debug
```

### 第四步：获取APK

打包完成后，APK文件位于：
```
bin/
└── vipvideo-1.0.0-arm64-v8a-debug.apk
```

## 常见问题

### Q1: 首次打包需要多长时间？

**A:** 首次打包需要1-2小时，因为需要下载：
- Android SDK（约1GB）
- Android NDK（约1GB）
- 其他构建工具

后续打包会使用缓存，速度会快很多（约10-20分钟）。

### Q2: 打包失败怎么办？

**A:** 检查以下几点：
1. 网络连接是否正常
2. 磁盘空间是否充足（至少10GB）
3. Python版本是否为3.7+
4. Java JDK是否已安装

查看详细错误信息：
```bash
buildozer android debug --verbose
```

### Q3: 如何减小APK体积？

**A:** 在[buildozer.spec](buildozer.spec)中修改：
```
android.archs = arm64-v8a  # 只包含64位架构
```

### Q4: 如何打包发布版本？

**A:** 运行：
```bash
buildozer android release
```

### Q5: WSL2安装失败怎么办？

**A:** 检查：
1. Windows版本是否支持（需要Windows 10 2004或更高）
2. 虚拟化是否在BIOS中启用
3. 是否有管理员权限

## 项目文件说明

```
电影 - 副本/
├── main.py                 # Kivy主应用文件
├── vipvideo.kv            # Kivy界面布局文件
├── buildozer.spec         # Buildozer打包配置文件
├── AndroidManifest.xml    # Android权限配置
├── requirements.txt       # Python依赖包
├── video_history.json     # 播放历史记录
├── 爬虫vip电影.py         # 原始Tkinter版本
├── auto_build.bat         # Windows自动打包脚本
├── auto_build.py          # Python自动打包脚本
├── build_in_wsl.sh        # WSL打包脚本
├── Dockerfile             # Docker打包配置
├── check_environment.py   # 环境检查工具
└── .github/
    └── workflows/
        └── build-apk.yml  # GitHub Actions自动打包配置
```

## 下一步操作

1. **测试应用**（可选）
   ```bash
   python main.py
   ```

2. **选择打包方式**
   - 最简单：GitHub Actions
   - 推荐：WSL2
   - 高级：Docker

3. **开始打包**
   ```bash
   python auto_build.py
   ```

4. **安装APK**
   - 将APK传输到Android设备
   - 允许安装未知来源应用
   - 安装并测试

## 技术支持

如遇问题，请：
1. 查看[README.md](README.md)获取详细文档
2. 运行`python check_environment.py`检查环境
3. 查看Buildozer官方文档：https://buildozer.readthedocs.io/

## 许可证

本项目仅供学习使用。
