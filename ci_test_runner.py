# ci_test_runner.py - Optimized test runner for CI/CD environments
import pytest
import sys
import os
from datetime import datetime

def run_ci_tests():
    """Run tests optimized for CI/CD environment"""
    # Add current directory to Python path
    sys.path.append(os.getcwd())
    
    # Detect CI environment
    is_ci = os.getenv('CI', 'false').lower() == 'true'
    
    print("🚀 Reddit Automation Test - CI Mode")
    print("=" * 50)
    print(f"🌍 Environment: {'CI/CD Pipeline' if is_ci else 'Local Development'}")
    print(f"🎭 Browser Mode: {'Headless' if is_ci else 'Headed'}")
    print(f"📹 Video Recording: {'Disabled (CI)' if is_ci else 'Enabled (Local)'}")
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configure pytest arguments for CI
    pytest_args = [
        'step_definitions/reddit_steps.py',
        '-v',
        '--tb=short',
        '--strict-markers',
        '--disable-warnings'
    ]
    
    # Add CI-specific optimizations
    if is_ci:
        pytest_args.extend([
            '--no-header',
            '--no-summary',
            '-q'  # Quiet output for CI logs
        ])
        
        # Override conftest for CI
        if os.path.exists('conftest_headless.py'):
            # Temporarily rename conftest files
            if os.path.exists('conftest.py'):
                os.rename('conftest.py', 'conftest_local.py.bak')
            os.rename('conftest_headless.py', 'conftest.py')
    
    try:
        # Run the tests
        print("\n🧪 Executing Reddit Automation Test...")
        exit_code = pytest.main(pytest_args)
        
        # Report results
        if exit_code == 0:
            print("\n" + "=" * 50)
            print("✅ REDDIT AUTOMATION TEST PASSED!")
            print("🎯 Successfully automated:")
            print("   • Reddit login/logout")
            print("   • Gaming subreddit navigation") 
            print("   • Smart post detection (non-pinned, non-ads)")
            print("   • Nintendo content analysis and voting")
            print(f"⏱️  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if is_ci:
                # Set GitHub Actions output
                print("::notice title=Test Success::Reddit automation test completed successfully")
                
        else:
            print("\n" + "=" * 50)
            print("❌ REDDIT AUTOMATION TEST FAILED!")
            print("📋 Check the error logs above for details")
            
            if is_ci:
                print("::error title=Test Failure::Reddit automation test failed")
    
    finally:
        # Restore conftest files if in CI
        if is_ci:
            try:
                if os.path.exists('conftest.py'):
                    os.rename('conftest.py', 'conftest_headless.py')
                if os.path.exists('conftest_local.py.bak'):
                    os.rename('conftest_local.py.bak', 'conftest.py')
            except:
                pass
    
    return exit_code

if __name__ == "__main__":
    exit_code = run_ci_tests()
    sys.exit(exit_code)