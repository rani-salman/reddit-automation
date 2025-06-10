import pytest
from playwright.sync_api import sync_playwright
import os
import allure
from datetime import datetime
import shutil

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # Enhanced CI detection
        is_ci = (
            os.getenv('CI', '').lower() == 'true' or
            os.getenv('GITHUB_ACTIONS', '').lower() == 'true' or
            os.getenv('HEADLESS', '').lower() == 'true' or
            'CI' in os.environ
        )
        
        # Force headless in CI environments
        headless_mode = is_ci
        slow_mo = 1000 if is_ci else 2000
        
        print(f"🎭 Browser mode: {'Headless (CI)' if headless_mode else 'Headed (Local)'}")
        print(f"⚡ Slow motion: {slow_mo}ms")
        print(f"🔍 CI detected: {is_ci}")
        print(f"🌍 Environment variables: CI={os.getenv('CI')}, GITHUB_ACTIONS={os.getenv('GITHUB_ACTIONS')}")
        
        # Launch browser with appropriate settings
        launch_options = {
            'headless': headless_mode,
            'slow_mo': slow_mo
        }
        
        # Add CI-specific options
        if is_ci:
            launch_options.update({
                'args': [
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding'
                ]
            })
        
        browser = p.firefox.launch(**launch_options)
        yield browser
        browser.close()

@pytest.fixture(scope="function") 
def page(browser, request):
    # Generate test name for logging
    test_name = request.node.name.replace("::", "_").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Enhanced CI detection
    is_ci = (
        os.getenv('CI', '').lower() == 'true' or
        os.getenv('GITHUB_ACTIONS', '').lower() == 'true' or
        os.getenv('HEADLESS', '').lower() == 'true' or
        'CI' in os.environ
    )
    
    # Create context based on environment
    if is_ci:
        print("🔧 CI Mode: Optimized configuration for headless execution")
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            viewport={'width': 1920, 'height': 1080},
            # Disable images and other resources to speed up CI
            java_script_enabled=True,
            ignore_https_errors=True
        )
    else:
        # Local mode with video recording
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
    
    # Enhanced stealth configuration
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
    
    # Add environment info to Allure (only if not in CI to avoid clutter)
    if not is_ci:
        allure.attach(
            f"Browser: Firefox\nMode: {'Headless' if is_ci else 'Headed'}\nViewport: 1920x1080\nVideo Recording: {'Disabled' if is_ci else 'Enabled'}",
            name="Test Environment",
            attachment_type=allure.attachment_type.TEXT
        )
    
    yield page
    
    # Handle cleanup
    try:
        if not is_ci and page.video:
            # Handle video in local mode only
            video_path = page.video.path()
            if video_path and os.path.exists(video_path):
                final_video_path = os.path.join("videos", f"{test_name}_{timestamp}.webm")
                try:
                    shutil.move(video_path, final_video_path)
                    print(f"📹 Video saved: {final_video_path}")
                    
                    # Attach to Allure if available
                    try:
                        with open(final_video_path, "rb") as video_file:
                            allure.attach(
                                video_file.read(),
                                name=f"Test Execution Video - {test_name}",
                                attachment_type=allure.attachment_type.WEBM
                            )
                    except:
                        pass  # Allure might not be available in all runs
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
    username = os.getenv('REDDIT_USERNAME', 'your_username_here')
    password = os.getenv('REDDIT_PASSWORD', 'your_password_here')
    
    # Enhanced credential validation
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

# Enhanced environment configuration for Allure
def pytest_configure(config):
    """Add environment info to Allure report"""
    if hasattr(config, '_allure_configure'):
        return  # Already configured
    
    config._allure_configure = True
    
    # Detect environment
    is_ci = (
        os.getenv('CI', '').lower() == 'true' or
        os.getenv('GITHUB_ACTIONS', '').lower() == 'true'
    )
    
    # Create environment.properties for Allure
    env_properties = f"""
Browser=Firefox
Platform={'Linux (CI)' if is_ci else 'Windows (Local)'}
Python.Version={os.sys.version.split()[0]}
Test.Framework=Pytest + BDD + Playwright
Execution.Mode={'Headless (CI)' if is_ci else 'Headed (Local)'}
Video.Recording={'Disabled (CI)' if is_ci else 'Enabled (Local)'}
Test.Type=UI Automation
Application=Reddit
Test.Suite=Gaming Subreddit Automation
Environment={'CI/CD Pipeline' if is_ci else 'Local Development'}
"""
    
    # Write environment file for Allure
    os.makedirs('allure-results', exist_ok=True)
    with open('allure-results/environment.properties', 'w') as f:
        f.write(env_properties.strip())