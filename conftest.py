import pytest
from playwright.sync_api import sync_playwright
import os
import allure
from datetime import datetime
import shutil

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # Use Firefox with video recording enabled
        browser = p.firefox.launch(
            headless=False, 
            slow_mo=2000
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser, request):
    # Generate video filename with test name and timestamp
    test_name = request.node.name.replace("::", "_").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_filename = f"{test_name}_{timestamp}.webm"
    
    # Create videos directory if it doesn't exist
    videos_dir = "videos"
    os.makedirs(videos_dir, exist_ok=True)
    
    # Create context with video recording
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        record_video_dir=videos_dir,
        record_video_size={"width": 1920, "height": 1080}
    )
    
    page = context.new_page()
    
    # Simple stealth - just remove webdriver
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
    """)
    
    # Add environment info to Allure
    allure.attach(
        f"Browser: Firefox\nViewport: 1920x1080\nUser Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0\nVideo Recording: Enabled\nVideo File: {video_filename}",
        name="Test Environment",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield page
    
    # After test completes, handle video
    try:
        video_path = page.video.path() if page.video else None
        context.close()
        
        # Rename and attach video to Allure report
        if video_path and os.path.exists(video_path):
            final_video_path = os.path.join(videos_dir, video_filename)
            try:
                # Move video to final location
                shutil.move(video_path, final_video_path)
                
                # Attach video to Allure report
                with open(final_video_path, "rb") as video_file:
                    allure.attach(
                        video_file.read(),
                        name=f"Test Execution Video - {test_name}",
                        attachment_type=allure.attachment_type.WEBM
                    )
                
                print(f"✅ Video saved and attached: {final_video_path}")
                
            except Exception as e:
                print(f"Error handling video: {e}")
                
                # Try to attach original video if move failed
                if os.path.exists(video_path):
                    try:
                        with open(video_path, "rb") as video_file:
                            allure.attach(
                                video_file.read(),
                                name=f"Test Execution Video - {test_name}",
                                attachment_type=allure.attachment_type.WEBM
                            )
                    except:
                        pass
        else:
            print("⚠ No video path available")
            
    except Exception as e:
        print(f"Error in video handling: {e}")
        try:
            context.close()
        except:
            pass

@pytest.fixture
def reddit_credentials():
    return {
        'username': os.getenv('REDDIT_USERNAME', 'Competitive-Break279'),
        'password': os.getenv('REDDIT_PASSWORD', 'Rani.salman1')
    }

# Add environment information to Allure
def pytest_configure(config):
    """Add environment info to Allure report"""
    if hasattr(config, '_allure_configure'):
        return  # Already configured
    
    config._allure_configure = True
    
    # Create environment.properties for Allure
    env_properties = f"""
Browser=Firefox
Platform=Windows
Python.Version={os.sys.version}
Test.Framework=Pytest + BDD
Video.Recording=Enabled
Video.Resolution=1920x1080
Test.Type=UI Automation
Application=Reddit
Test.Suite=Gaming Subreddit Automation
"""
    
    # Write environment file for Allure
    os.makedirs('allure-results', exist_ok=True)
    with open('allure-results/environment.properties', 'w') as f:
        f.write(env_properties.strip())

# Add test categorization
def pytest_runtest_setup(item):
    """Add test categories and labels"""
    if hasattr(allure, 'dynamic'):
        # Add labels based on test
        if 'reddit' in item.name.lower():
            allure.dynamic.label('component', 'Reddit')
            allure.dynamic.label('suite', 'Reddit Automation')
            
        if 'gaming' in str(item.function.__doc__).lower():
            allure.dynamic.label('feature', 'Gaming Subreddit')
            
        if 'automation' in item.name.lower():
            allure.dynamic.label('testType', 'UI Automation')
            allure.dynamic.label('layer', 'UI')
