# troubleshoot_allure.py - Diagnose and fix Allure installation issues
import subprocess
import sys
import os
import shutil

def run_command(cmd, description=""):
    """Run a command and return result info"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip(),
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Command timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def check_node_npm():
    """Check Node.js and npm installation"""
    print("🔍 Checking Node.js and npm...")
    
    node_result = run_command("node --version")
    npm_result = run_command("npm --version")
    
    if node_result['success']:
        print(f"✅ Node.js: {node_result['stdout']}")
    else:
        print("❌ Node.js not found or not working")
        print("   Install from: https://nodejs.org/")
        return False
    
    if npm_result['success']:
        print(f"✅ npm: {npm_result['stdout']}")
    else:
        print("❌ npm not found or not working")
        return False
    
    return True

def check_allure_installation():
    """Check various ways Allure might be installed"""
    print("\n🔍 Checking Allure installation...")
    
    # Check direct allure command
    allure_result = run_command("allure --version")
    if allure_result['success']:
        print(f"✅ Allure CLI: {allure_result['stdout']}")
        return 'allure'
    
    # Check allure.cmd on Windows
    allure_cmd_result = run_command("allure.cmd --version")
    if allure_cmd_result['success']:
        print(f"✅ Allure CLI (Windows): {allure_cmd_result['stdout']}")
        return 'allure.cmd'
    
    # Check npm global installation
    npm_list_result = run_command("npm list -g allure-commandline")
    if npm_list_result['success'] and 'allure-commandline' in npm_list_result['stdout']:
        print("✅ Allure found in npm global packages")
        
        # Try to find the exact path
        npm_root_result = run_command("npm root -g")
        if npm_root_result['success']:
            npm_root = npm_root_result['stdout']
            allure_paths = [
                os.path.join(npm_root, 'allure-commandline', 'bin', 'allure'),
                os.path.join(npm_root, 'allure-commandline', 'bin', 'allure.cmd'),
                os.path.join(npm_root, '.bin', 'allure'),
                os.path.join(npm_root, '.bin', 'allure.cmd')
            ]
            
            for path in allure_paths:
                if os.path.exists(path):
                    print(f"✅ Found Allure at: {path}")
                    return path
    
    print("❌ Allure CLI not found")
    return None

def fix_allure_installation():
    """Try to install or fix Allure"""
    print("\n🔧 Attempting to install/fix Allure...")
    
    # Try npm install
    print("Installing allure-commandline via npm...")
    install_result = run_command("npm install -g allure-commandline")
    
    if install_result['success']:
        print("✅ npm install completed")
        
        # Verify installation
        allure_cmd = check_allure_installation()
        if allure_cmd:
            print(f"✅ Allure successfully installed: {allure_cmd}")
            return allure_cmd
        else:
            print("⚠️ Installation completed but Allure still not accessible")
    else:
        print(f"❌ npm install failed: {install_result.get('stderr', 'Unknown error')}")
    
    # Try alternative: npx
    print("\n🔧 Trying npx as alternative...")
    npx_result = run_command("npx allure-commandline --version")
    if npx_result['success']:
        print(f"✅ Allure accessible via npx: {npx_result['stdout']}")
        return 'npx allure-commandline'
    
    return None

def create_allure_wrapper():
    """Create a wrapper script for Allure"""
    print("\n🔧 Creating Allure wrapper script...")
    
    # Check if we can use npx
    npx_result = run_command("npx allure-commandline --version")
    if npx_result['success']:
        wrapper_content = '''@echo off
npx allure-commandline %*
'''
        with open('allure_wrapper.cmd', 'w') as f:
            f.write(wrapper_content)
        
        print("✅ Created allure_wrapper.cmd - use this instead of 'allure'")
        return os.path.abspath('allure_wrapper.cmd')
    
    return None

def generate_manual_report():
    """Generate report manually without Allure CLI"""
    print("\n📊 Generating manual report without Allure CLI...")
    
    try:
        # Enhanced manual report generator
        from test_runner import generate_allure_report_manual
        report_path = generate_allure_report_manual()
        
        if report_path:
            print(f"✅ Manual report created: {report_path}")
            
            # Try to open it
            try:
                import webbrowser
                webbrowser.open(f"file://{os.path.abspath(report_path)}")
                print("🌐 Opening report in browser...")
            except:
                print("💡 Manually open the report in your browser")
            
            return True
    except Exception as e:
        print(f"❌ Manual report generation failed: {e}")
    
    return False

def main():
    """Main troubleshooting function"""
    print("🔧 Allure Installation Troubleshooter")
    print("=" * 50)
    
    # Step 1: Check prerequisites
    if not check_node_npm():
        print("\n❌ Node.js/npm required but not found")
        print("💡 Install Node.js from: https://nodejs.org/")
        return
    
    # Step 2: Check current Allure installation
    allure_cmd = check_allure_installation()
    
    if allure_cmd:
        print(f"\n✅ Allure is working: {allure_cmd}")
        print("🎯 You can now run: python test_runner.py")
        return
    
    # Step 3: Try to fix installation
    allure_cmd = fix_allure_installation()
    
    if allure_cmd:
        print(f"\n✅ Allure fixed: {allure_cmd}")
        print("🎯 You can now run: python test_runner.py")
        return
    
    # Step 4: Try wrapper approach
    wrapper = create_allure_wrapper()
    if wrapper:
        print(f"\n✅ Allure wrapper created: {wrapper}")
        print("🎯 Modify test_runner.py to use the wrapper")
        return
    
    # Step 5: Manual report fallback
    print("\n⚠️ Allure CLI installation failed")
    print("💡 The enhanced test_runner.py will automatically create a manual report")
    print("🎯 Run: python test_runner.py")
    print("   The test will work and create a beautiful report even without Allure CLI")

if __name__ == "__main__":
    main()