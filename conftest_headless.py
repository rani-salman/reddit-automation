# conftest_headless.py - Headless configuration for CI/CD
import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # Check if running in CI environment
        is_ci = os.getenv('CI', 'false').lower() == 'true'
        is_headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        
        # Use headless mode in CI, headed mode locally
        headless_mode = is_ci or is_headless
        slow_mo = 1000 if is_ci else 2000
        
        print(f"🎭 Browser mode: {'Headless' if headless_mode else 'Headed'}")
        print(f"⚡ Slow motion: {slow_mo}ms")
        
        browser = p.firefox.launch(
            headless=headless_mode,
            slow_mo=slow_mo,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ] if is_ci else []
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function") 
def page(browser, request):
    # Generate test name for logging
    test_name = request.node.name.replace("::", "_").replace(" ", "_")
    
    # Check CI environment
    is_ci = os.getenv('CI', 'false').lower() == 'true'
    
    # Create context (no video recording in CI to save resources)
    if is_ci:
        print("🔧 CI Mode: Skipping video recording to optimize performance")
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            viewport={'width': 1920, 'height': 1080}
        )
    else:
        # Local mode with video recording
        videos_dir = "videos"
        os.makedirs(videos_dir, exist_ok=True)
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            record_video_dir=videos_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
    
    page = context.new_page()
    
    # Enhanced stealth for CI environment
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
    """)
    
    yield page
    
    # Handle cleanup
    try:
        if not is_ci and page.video:
            # Handle video in local mode
            video_path = page.video.path()
            print(f"📹 Video saved: {video_path}")
    except Exception as e:
        print(f"⚠️ Video handling error: {e}")
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
    
    if username == 'your_username_here' or password == 'your_password_here':
        print("⚠️ Warning: Using placeholder credentials")
        print("💡 Set REDDIT_USERNAME and REDDIT_PASSWORD environment variables")
    
    return {
        'username': username,
        'password': password
    }