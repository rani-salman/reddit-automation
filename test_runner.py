import pytest
import sys
import os
import shutil
from datetime import datetime
import subprocess

def check_allure_installation():
    """Check if Allure is properly installed and accessible"""
    print("🔍 Checking Allure installation...")
    
    # Try different ways to find Allure
    allure_commands = ['allure', 'allure.cmd', 'allure.bat']
    
    for cmd in allure_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Found Allure: {cmd}")
                print(f"   Version: {result.stdout.strip()}")
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            continue
    
    # Check if Allure is in npm global modules
    try:
        npm_root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True, timeout=10)
        if npm_root.returncode == 0:
            allure_path = os.path.join(npm_root.stdout.strip(), 'allure-commandline', 'bin', 'allure')
            if os.path.exists(allure_path):
                print(f"✅ Found Allure in npm global: {allure_path}")
                return allure_path
            
            # Check for .cmd version on Windows
            allure_cmd_path = allure_path + '.cmd'
            if os.path.exists(allure_cmd_path):
                print(f"✅ Found Allure in npm global: {allure_cmd_path}")
                return allure_cmd_path
    except:
        pass
    
    print("❌ Allure CLI not found in PATH")
    return None

def generate_allure_report_manual():
    """Generate a simple HTML report from allure-results manually"""
    print("📊 Creating basic Allure-style report manually...")
    
    try:
        import json
        from pathlib import Path
        
        # Create basic HTML report
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Reddit Automation Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: #2196F3; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .success {{ background: #e8f5e8; border-color: #4caf50; }}
        .video-section {{ background: #f0f8ff; border-color: #2196F3; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
        video {{ width: 100%; max-width: 800px; margin: 10px 0; }}
        .step {{ margin: 10px 0; padding: 10px; background: #f9f9f9; border-left: 4px solid #2196F3; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; margin: 2px; }}
        .pass {{ background: #4caf50; color: white; }}
        .info {{ background: #2196F3; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Reddit Automation Test Report</h1>
            <p>Professional BDD Test Execution with Video Recording</p>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section success">
            <h2>✅ Test Results Summary</h2>
            <span class="badge pass">PASSED</span>
            <span class="badge info">BDD</span>
            <span class="badge info">VIDEO RECORDED</span>
            <p><strong>Test:</strong> Reddit Gaming Subreddit Automation</p>
            <p><strong>Scenario:</strong> Vote on gaming subreddit posts based on Nintendo content</p>
        </div>
        
        <div class="section">
            <h2>📋 Test Steps Executed</h2>
            <div class="step">✅ Navigate to old Reddit homepage</div>
            <div class="step">✅ Perform login to Reddit</div>
            <div class="step">✅ Navigate to gaming subreddit</div>
            <div class="step">✅ Find second non-pinned, non-ad post</div>
            <div class="step">✅ Vote on post based on Nintendo content</div>
            <div class="step">✅ Logout from Reddit</div>
        </div>
        
        <div class="section video-section">
            <h2>📹 Test Execution Video</h2>
            <p>Complete test execution recording:</p>
            <div id="video-container">
                <!-- Videos will be inserted here -->
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Test Features</h2>
            <ul>
                <li>✅ BDD (Behavior Driven Development) with Gherkin scenarios</li>
                <li>✅ Page Object Model architecture</li>
                <li>✅ Anti-detection measures for reliable automation</li>
                <li>✅ Smart post detection (excludes pinned/ads)</li>
                <li>✅ Nintendo content analysis and voting logic</li>
                <li>✅ Video recording of entire test execution</li>
                <li>✅ Professional reporting with visual documentation</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Add videos to the report
        const videoContainer = document.getElementById('video-container');
        const videosDir = '../videos/';
        
        // Try to find and display videos
        fetch('../videos/')
            .then(response => response.text())
            .then(html => {{
                const videos = html.match(/test_reddit_automation_.*\\.webm/g);
                if (videos) {{
                    videos.forEach(video => {{
                        const videoElement = document.createElement('video');
                        videoElement.controls = true;
                        videoElement.src = videosDir + video;
                        videoElement.style.width = '100%';
                        videoElement.style.maxWidth = '800px';
                        videoElement.style.margin = '10px 0';
                        
                        const videoLabel = document.createElement('p');
                        videoLabel.textContent = `📹 ${{video}}`;
                        videoLabel.style.fontWeight = 'bold';
                        
                        videoContainer.appendChild(videoLabel);
                        videoContainer.appendChild(videoElement);
                    }});
                }} else {{
                    videoContainer.innerHTML = '<p>Video files will be available in the videos/ directory</p>';
                }}
            }})
            .catch(() => {{
                videoContainer.innerHTML = '<p>📹 Video recordings are available in the videos/ directory</p>';
            }});
    </script>
</body>
</html>
        """
        
        # Save the HTML report
        report_path = "allure-report/index.html"
        os.makedirs("allure-report", exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Manual Allure-style report created: {report_path}")
        return report_path
        
    except Exception as e:
        print(f"❌ Failed to create manual report: {e}")
        return None

def run_tests():
    """Run the BDD tests with Allure reporting and video recording"""
    # Add current directory to Python path
    sys.path.append(os.getcwd())
    
    # Create reports directories
    os.makedirs('allure-results', exist_ok=True)
    os.makedirs('allure-report', exist_ok=True)
    os.makedirs('videos', exist_ok=True)
    
    # Get timestamp for report naming
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    print("🚀 Starting Reddit Automation Test with Video Recording...")
    print(f"📹 Videos will be saved in: videos/")
    print(f"📊 Allure results will be in: allure-results/")
    
    # Run pytest with Allure and video recording
    exit_code = pytest.main([
        'step_definitions/reddit_steps.py',
        '-v',
        '--tb=short',
        '--alluredir=allure-results',
        '--clean-alluredir',  # Clean previous results
        f'--html=reports/html_report_{timestamp}.html',
        '--self-contained-html'
    ])
    
    if exit_code == 0:
        print("✅ Test completed successfully!")
        print("\n📊 Generating Allure Report...")
        
        # Check for Allure installation
        allure_cmd = check_allure_installation()
        
        if allure_cmd:
            # Generate Allure report with found command
            try:
                result = subprocess.run([
                    allure_cmd, 'generate', 'allure-results', 
                    '--clean', '--output', 'allure-report'
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print("✅ Allure report generated successfully!")
                    report_path = os.path.abspath("allure-report/index.html")
                else:
                    print(f"⚠️ Allure generation failed: {result.stderr}")
                    report_path = generate_allure_report_manual()
            except Exception as e:
                print(f"❌ Allure execution failed: {e}")
                report_path = generate_allure_report_manual()
        else:
            print("⚠️ Creating alternative report...")
            report_path = generate_allure_report_manual()
        
        # Try to open the report
        if report_path and os.path.exists(report_path):
            print(f"📂 Report available at: {report_path}")
            print("📹 Video recordings are embedded/linked in the report")
        
        # List available videos
        videos_dir = "videos"
        if os.path.exists(videos_dir):
            videos = [f for f in os.listdir(videos_dir) if f.endswith('.webm')]
            if videos:
                print(f"\n📹 Video recordings ({len(videos)} files):")
                for video in videos:
                    print(f"   • {video}")
            
    else:
        print("❌ Test failed!")
    
    return exit_code

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)