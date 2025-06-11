import pytest
from playwright.sync_api import sync_playwright
import os
import allure
from datetime import datetime
import shutil

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        headless_mode = False
        slow_mo = 2000
        
        print(f"🎭 Browser mode: {'Headless (CI)' if headless_mode else 'Headed (Local)'}")
        print(f"⚡ Slow motion: {slow_mo}ms")
        print(f"🌍 Environment variables: CI={os.getenv('CI')}, GITHUB_ACTIONS={os.getenv('GITHUB_ACTIONS')}")
        
        launch_options = {
            'headless': headless_mode,
            'slow_mo': slow_mo
        }
        

        
        browser = p.firefox.launch(**launch_options)
        yield browser
        browser.close()

@pytest.fixture(scope="function") 
def page(browser, request):
    test_name = request.node.name.replace("::", "_").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    

    

    print("🎥 Local Mode: Video recording enabled")
    videos_dir = "videos"
    os.makedirs(videos_dir, exist_ok=True)
    
    video_filename = f"{test_name}_{timestamp}.webm"
    
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        record_video_dir=videos_dir,
        record_video_size={"width": 1920, "height": 1080}
    )
    
    page = context.new_page()
    
    page.add_init_script("""
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Mock plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // Mock languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        
        // Mock chrome object
        window.chrome = {
            runtime: {}
        };
        
        // Remove automation indicators
        delete window.navigator.__proto__.webdriver;
    """)
    
    
    allure.attach(
        f"Browser: Firefox\nMode: {'Headed'}\nViewport: 1920x1080\nVideo Recording: {'Enabled'}",
        name="Test Environment",
        attachment_type=allure.attachment_type.TEXT
    )
    
    yield page
    
    try:
        if  page.video:
            video_path = page.video.path()
            if video_path and os.path.exists(video_path):
                final_video_path = os.path.join("videos", f"{test_name}_{timestamp}.webm")
                try:
                    shutil.move(video_path, final_video_path)
                    print(f"📹 Video saved: {final_video_path}")
                    
                    try:
                        with open(final_video_path, "rb") as video_file:
                            allure.attach(
                                video_file.read(),
                                name=f"Test Execution Video - {test_name}",
                                attachment_type=allure.attachment_type.WEBM
                            )
                    except:
                        pass  
                except Exception as e:
                    print(f"⚠️ Video handling error: {e}")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")
    finally:
        try:
            context.close()
        except:
            pass

@pytest.fixture
def reddit_credentials():
    """Load Reddit credentials from environment variables"""
    username = os.getenv('REDDIT_USERNAME', 'Competitive-Break279')
    password = os.getenv('REDDIT_PASSWORD', 'Rani.salman1')
    
    if username == 'your_username_here' or password == 'your_password_here':
        print("⚠️ Warning: Using placeholder credentials")
        print("💡 Set REDDIT_USERNAME and REDDIT_PASSWORD environment variables")
        print(f"🔍 Current REDDIT_USERNAME: {username}")
    else:
        print(f"✅ Credentials loaded for user: {username}")
    
    return {
        'username': username,
        'password': password
    }

def pytest_configure(config):
    """Add environment info to Allure report"""
    if hasattr(config, '_allure_configure'):
        return  # Already configured
    
    config._allure_configure = True
    
    
    env_properties = f"""
Browser=Firefox
Platform={'Windows (Local)'}
Python.Version={os.sys.version.split()[0]}
Test.Framework=Pytest + BDD + Playwright
Execution.Mode={'Headed (Local)'}
Video.Recording={'Enabled (Local)'}
Test.Type=UI Automation
Application=Reddit
Test.Suite=Gaming Subreddit Automation
Environment={'Local Development'}
"""
    
    os.makedirs('allure-results', exist_ok=True)
    with open('allure-results/environment.properties', 'w') as f:
        f.write(env_properties.strip())