# pages/reddit_page.py
from pages.base_page import BasePage
import time

class RedditPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.gaming_subreddit_link = "a[href='/r/gaming']"
        # Updated logout selectors
        self.logout_link = "a[href='javascript:void(0)'][onclick*='submit()']:has-text('logout')"
        self.login_button_verify = "a.login-required.login-link"
        
    def navigate_to_homepage(self):
        """Navigate to old Reddit homepage - that's it!"""
        print("Navigating to old.reddit.com...")
        self.page.goto("https://old.reddit.com", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        print("Successfully loaded old Reddit")
        
    def navigate_to_gaming_subreddit(self):
        """Navigate to gaming subreddit"""
        print("Navigating to gaming subreddit...")
        self.page.goto("https://old.reddit.com/r/gaming", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)
        print("Navigated to gaming subreddit")
        
    def logout(self):
        """Proper logout by clicking the correct logout element and verifying success"""
        print("Starting logout process...")
        
        # First, make sure we're on old Reddit
        if "old.reddit.com" not in self.page.url:
            print("Not on old Reddit, navigating there first...")
            self.page.goto("https://old.reddit.com", wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
        
        try:
            # Look for the specific logout link you mentioned
            print("Looking for logout link...")
            
            # Try multiple selectors for the logout link
            logout_selectors = [
                "a[href='javascript:void(0)'][onclick*='submit()']:has-text('logout')",
                "a[onclick*='submit()']:has-text('logout')",
                "a:has-text('logout')[href='javascript:void(0)']",
                "a:has-text('logout')"
            ]
            
            logout_clicked = False
            for selector in logout_selectors:
                try:
                    logout_elements = self.page.locator(selector)
                    if logout_elements.count() > 0:
                        print(f"Found logout link with selector: {selector}")
                        logout_elements.first.click()
                        logout_clicked = True
                        print("Logout link clicked")
                        break
                except Exception as e:
                    print(f"Selector {selector} failed: {e}")
                    continue
            
            if not logout_clicked:
                print("Could not find logout link, trying fallback...")
                # Fallback: try direct navigation to logout
                self.page.goto("https://old.reddit.com/logout", wait_until="domcontentloaded", timeout=30000)
            
            # Wait for logout to process
            print("Waiting for logout to complete...")
            time.sleep(3)
            
            # Verify logout was successful by checking for login button
            print("Verifying logout success...")
            self.verify_logout_success()
            
        except Exception as e:
            print(f"Logout error: {e}")
            # Try fallback logout
            try:
                self.page.goto("https://old.reddit.com/logout", wait_until="domcontentloaded", timeout=30000)
                time.sleep(2)
                self.verify_logout_success()
            except Exception as e2:
                print(f"Fallback logout also failed: {e2}")
    
    def verify_logout_success(self):
        """Verify logout was successful by checking for the login button"""
        try:
            # Navigate to old Reddit home to check login status
            print("Checking logout status on old Reddit homepage...")
            self.page.goto("https://old.reddit.com", wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            
            # Look for the login button that indicates we're logged out
            login_button = self.page.locator("a.login-required.login-link")
            
            if login_button.count() > 0:
                print("✓ Logout successful - Login button is visible")
                return True
            else:
                print("⚠ Logout may have failed - Login button not found")
                
                # Try alternative login button selectors
                alternative_selectors = [
                    "a[href*='login']",
                    "a:has-text('Log in')",
                    "a:has-text('login')"
                ]
                
                for selector in alternative_selectors:
                    if self.page.locator(selector).count() > 0:
                        print(f"✓ Logout successful - Found login button with {selector}")
                        return True
                
                print("⚠ Could not verify logout - no login button found")
                return False
                
        except Exception as e:
            print(f"Error verifying logout: {e}")
            return False