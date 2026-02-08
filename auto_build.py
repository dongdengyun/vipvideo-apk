import sys
import os
import subprocess

def print_header(text):
    print("=" * 50)
    print(text)
    print("=" * 50)
    print()

def print_step(step_num, total_steps, text):
    print(f"[{step_num}/{total_steps}] {text}")

def run_command(cmd, description):
    print(f"  Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.returncode == 0
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False

def main():
    print_header("VIP Video Player - Auto Build Tool")
    
    print_step(1, 5, "Checking Python environment...")
    result = run_command("python --version", "Python version check")
    if not result:
        print("  Error: Python not found")
        input("Press Enter to exit...")
        sys.exit(1)
    print("  Python environment OK")
    print()
    
    print_step(2, 5, "Installing dependencies...")
    print("  Running: pip install -r requirements.txt")
    os.system("pip install -r requirements.txt")
    print("  Dependencies check completed")
    print()
    
    print_step(3, 5, "Checking Java environment...")
    result = run_command("java -version", "Java version check")
    if not result:
        print("  Warning: Java not found")
        print("  Java is required for Android build")
        print("  Please install JDK 8 or higher")
        print()
    else:
        print("  Java environment OK")
    print()
    
    print_step(4, 5, "Checking build environment...")
    print()
    print("  Buildozer requires a Linux environment to build APK")
    print("  Available options:")
    print()
    print("  1. WSL2 (Windows Subsystem for Linux) - Recommended")
    print("  2. Docker container")
    print("  3. GitHub Actions (online build)")
    print("  4. Virtual machine with Linux")
    print()
    
    has_wsl = run_command("wsl --list --verbose", "WSL check")
    has_docker = run_command("docker --version", "Docker check")
    
    if has_wsl:
        print("  [OK] WSL detected")
    else:
        print("  [X] WSL not installed")
    
    if has_docker:
        print("  [OK] Docker detected")
    else:
        print("  [X] Docker not installed")
    print()
    
    print_step(5, 5, "Build options")
    print()
    print("  Choose build method:")
    print()
    print("  1. Use WSL2 (if available)")
    print("  2. Use Docker (if available)")
    print("  3. Manual build instructions")
    print("  4. Exit")
    print()
    
    try:
        choice = input("  Enter your choice (1-4): ").strip()
        
        if choice == "1" and has_wsl:
            print()
            print("  Starting WSL build...")
            print("  This will take 1-2 hours on first run")
            print("  (downloading Android SDK, NDK, etc.)")
            print()
            os.system("wsl bash -c \"cd /mnt/c/Users/Administrator/Desktop/电影\\ -\\ 副本 && ./build_in_wsl.sh\"")
            
        elif choice == "2" and has_docker:
            print()
            print("  Starting Docker build...")
            print("  Building Docker image...")
            os.system("docker build -t buildozer .")
            print()
            print("  Building APK...")
            os.system("docker run --rm -v %cd%:/app buildozer")
            
        elif choice == "3":
            print()
            print_header("Manual Build Instructions")
            print()
            print("Option 1: Install WSL2 and build")
            print("  1. Run: wsl --install")
            print("  2. Restart computer")
            print("  3. Run: bash build_in_wsl.sh")
            print()
            print("Option 2: Use Docker")
            print("  1. Install Docker Desktop")
            print("  2. Run: docker build -t buildozer .")
            print("  3. Run: docker run --rm -v %cd%:/app buildozer")
            print()
            print("Option 3: Use GitHub Actions")
            print("  1. Push code to GitHub")
            print("  2. Enable GitHub Actions")
            print("  3. Download APK from Actions page")
            print()
            print("Option 4: Use Linux VM")
            print("  1. Install Ubuntu in VM")
            print("  2. Install Buildozer")
            print("  3. Run: buildozer android debug")
            print()
            
        elif choice == "4":
            print()
            print("  Exiting...")
            sys.exit(0)
            
        else:
            print()
            print("  Invalid choice or environment not available")
            print("  Please install WSL2 or Docker first")
            print()
            print("  To install WSL2: wsl --install")
            print("  To install Docker: https://www.docker.com/products/docker-desktop")
            
    except KeyboardInterrupt:
        print()
        print("  Build cancelled by user")
    
    print()
    print_header("Build Process Summary")
    print()
    print("  APK file will be located in: bin/")
    print()
    print("  If build failed, check the error messages above")
    print("  Common issues:")
    print("    - Network connection problems")
    print("    - Insufficient disk space")
    print("    - Missing dependencies")
    print()
    print("  Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()
