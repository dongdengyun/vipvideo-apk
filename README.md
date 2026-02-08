# VIP追剧神器 - Kivy Android应用

这是一个使用Kivy框架开发的VIP视频播放器Android应用，支持通过视频解析接口播放VIP视频。

## 功能特性

- 支持多个视频平台（爱奇艺、腾讯视频、优酷、哔哩哔哩）
- 多种画质选择（高清、超清、4K、蓝光、原画）
- 播放历史记录管理
- 浏览器播放和内置播放器两种模式
- 移动端优化的界面设计

## 项目结构

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
├── build_in_wsl.sh        # WSL打包脚本
├── Dockerfile             # Docker打包配置
├── check_environment.py   # 环境检查工具
└── .github/
    └── workflows/
        └── build-apk.yml  # GitHub Actions自动打包配置
```

## 环境要求

### Windows开发环境

1. Python 3.7+
2. Buildozer
3. Java Development Kit (JDK) 8或更高版本
4. Android SDK
5. Android NDK

### Linux开发环境（推荐用于打包）

Buildozer在Linux环境下运行最佳，建议使用以下环境之一：
- Ubuntu 20.04或更高版本
- Docker容器
- WSL2 (Windows Subsystem for Linux)

## 安装依赖

### 安装Python依赖

```bash
pip install -r requirements.txt
```

### 自动环境检查

运行环境检查工具，自动检测所有必需的依赖和环境：

```bash
python check_environment.py
```

## 自动打包工具

### 方式一：Windows自动打包脚本（推荐）

双击运行或在命令行执行：

```bash
auto_build.bat
```

该脚本会自动：
1. 检查Python环境
2. 安装所有依赖
3. 检查Java环境（可选自动安装）
4. 检测可用的打包环境（WSL/Docker）
5. 引导完成打包

### 方式二：使用WSL2（推荐）

1. 安装WSL2（如果尚未安装）：
```bash
wsl --install
```

2. 重启电脑后，运行WSL打包脚本：
```bash
bash build_in_wsl.sh
```

### 方式三：使用Docker

1. 安装Docker Desktop
2. 运行Docker打包：
```bash
docker build -t buildozer .
docker run --rm -v %cd%:/app buildozer
```

### 方式四：GitHub Actions自动打包

1. 将项目推送到GitHub
2. 在GitHub仓库中启用Actions
3. 自动触发打包流程
4. 从Actions页面下载生成的APK

## 开发和测试
### 安装Buildozer

```bash
pip install buildozer
```

## 开发和测试

### 在Windows上运行Kivy应用

```bash
python main.py
```

### 在Linux上运行Kivy应用

```bash
python3 main.py
```

## 打包成APK

### 快速开始（推荐）

运行自动打包脚本，它会自动检测环境并选择最佳的打包方式：

```bash
auto_build.bat
```

### 手动打包选项

如果需要手动控制打包过程，可以选择以下方式：

#### 选项1：使用Buildozer

```bash
buildozer android debug
```

#### 选项2：使用WSL2

```bash
bash build_in_wsl.sh
```

#### 选项3：使用Docker

```bash
docker build -t buildozer .
docker run --rm -v %cd%:/app buildozer
```

#### 选项4：使用GitHub Actions

1. 将项目推送到GitHub
2. 创建新的Release或推送代码
3. 等待Actions完成
4. 从Actions页面下载APK

### 首次打包说明

首次运行打包命令时，Buildozer会自动下载以下工具：
- Android SDK（约1GB）
- Android NDK（约1GB）
- 其他构建工具

下载过程可能需要1-2小时，具体取决于网络速度。后续打包会使用缓存，速度会快很多。

### APK文件位置

打包完成后，APK文件位于：
```
bin/
└── vipvideo-1.0.0-arm64-v8a-debug.apk
```

### 发布版本

如需打包发布版本（无调试信息）：

```bash
buildozer android release
```

## Android权限说明

应用需要以下权限：
- `INTERNET`: 访问网络
- `ACCESS_NETWORK_STATE`: 检查网络状态
- `WRITE_EXTERNAL_STORAGE`: 写入外部存储（保存历史记录）
- `READ_EXTERNAL_STORAGE`: 读取外部存储

## 常见问题

### 1. Buildozer打包失败

**问题**: 缺少依赖或环境配置错误

**解决方案**:
- 确保已安装JDK、Android SDK、NDK
- 检查环境变量是否正确设置
- 查看Buildozer日志获取详细错误信息

### 2. APK安装失败

**问题**: 应用无法安装或运行时崩溃

**解决方案**:
- 检查Android API版本是否兼容
- 确认所有必需的权限已添加
- 使用`adb logcat`查看运行时日志

### 3. 网络请求失败

**问题**: 无法获取视频信息或播放视频

**解决方案**:
- 确保设备有网络连接
- 检查视频解析接口是否可用
- 添加网络超时处理

### 4. 历史记录无法保存

**问题**: 播放历史记录丢失

**解决方案**:
- 检查存储权限是否已授予
- 确认应用有写入外部存储的权限
- 检查文件路径是否正确

## 性能优化建议

1. **减小APK体积**
   - 只包含必要的架构（arm64-v8a或armeabi-v7a）
   - 移除不必要的依赖
   - 使用ProGuard混淆和优化

2. **提升应用性能**
   - 优化网络请求
   - 使用缓存机制
   - 异步加载历史记录

3. **改善用户体验**
   - 添加加载动画
   - 优化界面响应速度
   - 支持深色模式

## 注意事项

1. 本应用仅供学习使用，请勿用于商业用途
2. 视频解析接口可能随时失效，需要及时更新
3. 请遵守相关平台的服务条款和版权法律
4. 建议定期更新依赖包以修复安全漏洞

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本视频播放功能
- 添加历史记录管理
- 支持多种画质选择
