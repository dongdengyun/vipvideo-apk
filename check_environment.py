import sys
import os

print("========================================")
print("VIP追剧神器 - 环境检查工具")
print("========================================")
print()

errors = []
warnings = []

print("[1/6] 检查Python版本...")
python_version = sys.version_info
if python_version.major == 3 and python_version.minor >= 7:
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    errors.append(f"Python版本过低: {python_version.major}.{python_version.minor}.{python_version.micro} (需要3.7+)")
print()

print("[2/6] 检查必要的Python包...")
required_packages = [
    'kivy',
    'beautifulsoup4',
    'requests',
    'buildozer'
]

for package in required_packages:
    try:
        __import__(package)
        print(f"✓ {package}")
    except ImportError:
        errors.append(f"缺少包: {package}")
        print(f"✗ {package}")
print()

print("[3/6] 检查Java环境...")
try:
    import subprocess
    result = subprocess.run(['java', '-version'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Java环境正常")
    else:
        warnings.append("Java未安装或配置不正确")
        print("✗ Java环境异常")
except FileNotFoundError:
    warnings.append("Java未安装")
    print("✗ Java未安装")
print()

print("[4/6] 检查项目文件...")
required_files = [
    'main.py',
    'vipvideo.kv',
    'buildozer.spec',
    'requirements.txt'
]

for file in required_files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        errors.append(f"缺少文件: {file}")
        print(f"✗ {file}")
print()

print("[5/6] 检查打包环境...")
has_wsl = False
has_docker = False

try:
    result = subprocess.run(['wsl', '--list', '--verbose'], capture_output=True, text=True)
    if result.returncode == 0:
        has_wsl = True
        print("✓ WSL环境可用")
    else:
        print("✗ WSL环境不可用")
except FileNotFoundError:
    print("✗ WSL未安装")

try:
    result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        has_docker = True
        print("✓ Docker环境可用")
    else:
        print("✗ Docker环境不可用")
except FileNotFoundError:
    print("✗ Docker未安装")
print()

print("[6/6] 检查Kivy应用...")
try:
    from kivy.app import App
    print("✓ Kivy可以导入")
    
    try:
        exec(open('main.py').read())
        print("✓ 主应用文件语法正确")
    except Exception as e:
        warnings.append(f"主应用文件可能有问题: {str(e)[:50]}")
        print(f"⚠ 主应用文件: {str(e)[:50]}")
except ImportError as e:
    errors.append(f"Kivy导入失败: {str(e)}")
    print(f"✗ Kivy导入失败")
print()

print("========================================")
print("检查结果汇总")
print("========================================")
print()

if errors:
    print(f"发现 {len(errors)} 个错误:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    print()

if warnings:
    print(f"发现 {len(warnings)} 个警告:")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")
    print()

if not errors and not warnings:
    print("✓ 所有检查通过！")
    print()
    print("下一步操作:")
    print("  1. 运行应用: python main.py")
    print("  2. 自动打包: auto_build.bat")
    print("  3. 使用WSL: ./build_in_wsl.sh")
    print("  4. 使用Docker: docker build -t buildozer . && docker run --rm -v %cd%:/app buildozer")
elif not errors:
    print("✓ 没有严重错误，可以继续")
    print()
    print("建议操作:")
    print("  1. 解决警告问题以获得最佳体验")
    print("  2. 运行应用测试: python main.py")
else:
    print("✗ 发现严重错误，需要先解决")
    print()
    print("建议操作:")
    print("  1. 安装缺失的Python包: pip install -r requirements.txt")
    print("  2. 检查项目文件是否完整")
    print("  3. 确保Python版本符合要求")

print()
print("按Enter键退出...")
input()
