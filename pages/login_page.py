# pages/login_page.py - Updated with correct selectors
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Updated selectors based on the actual HTML structure
        self.username_field = "#login-username"
        self.password_field = "#login-password" 
        self.login_button = "button[type='submit']"
        
    def perform_login(self, username, password):
        """Simple login process with correct selectors"""
        print("Starting login process...")
        
        # Step 1: Click the login link on old Reddit
        print("Clicking login link...")
        login_link = self.page.locator("a.login-required.login-link")
        
        if login_link.count() > 0:
            login_link.click()
            print("Login link clicked")
        else:
            print("Exact login link not found, trying any login link...")
            self.page.locator("a[href*='login']").first.click()
        
        # Step 2: Wait for new Reddit login page
        print("Waiting for new Reddit login page...")
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=15000)
            time.sleep(3)
            print(f"Current URL: {self.page.url}")
        except Exception as e:
            print(f"Wait error: {e}")
        
        # Step 3: Wait for login form to be ready
        print("Waiting for login form...")
        try:
            self.page.wait_for_selector("#login-username", timeout=10000)
            print("Login form found")
        except Exception as e:
            print(f"Login form wait error: {e}")
        
        # Step 4: Fill username using the custom element
        print("Filling username...")
        try:
            # Try the main selector first
            username_element = self.page.locator("#login-username")
            if username_element.count() > 0:
                username_element.click()  # Click to focus
                time.sleep(0.5)
                username_element.fill(username)
                print("Username filled successfully")
            else:
                print("Username field not found")
        except Exception as e:
            print(f"Username fill error: {e}")
            # Try alternative - look for input inside the custom element
            try:
                self.page.locator("#login-username input").fill(username)
                print("Username filled with alternative selector")
            except Exception as e2:
                print(f"Alternative username fill also failed: {e2}")
        
        time.sleep(1)
        
        # Step 5: Fill password using the custom element
        print("Filling password...")
        try:
            # Try the main selector first
            password_element = self.page.locator("#login-password")
            if password_element.count() > 0:
                password_element.click()  # Click to focus
                time.sleep(0.5)
                password_element.fill(password)
                print("Password filled successfully")
            else:
                print("Password field not found")
        except Exception as e:
            print(f"Password fill error: {e}")
            # Try alternative - look for input inside the custom element
            try:
                self.page.locator("#login-password input").fill(password)
                print("Password filled with alternative selector")
            except Exception as e2:
                print(f"Alternative password fill also failed: {e2}")
        
        time.sleep(1)
        
        # Step 6: Look for and click submit button
        print("Looking for submit button...")
        try:
            # Try different submit button selectors
            submit_selectors = [
                "button[type='submit']",
                "button:has-text('Log In')",
                "button:has-text('Continue')",
                ".auth-flow-modal button",
                "faceplate-button[type='submit']"
            ]
            
            submitted = False
            for selector in submit_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        print(f"Found submit button with selector: {selector}")
                        self.page.locator(selector).first.click()
                        submitted = True
                        break
                except:
                    continue
            
            if not submitted:
                print("No submit button found - form might auto-submit")
            else:
                print("Submit button clicked")
                
            # Wait for submission
            self.page.wait_for_load_state("domcontentloaded", timeout=20000)
            time.sleep(3)
            print(f"After login URL: {self.page.url}")
            
        except Exception as e:
            print(f"Submit error: {e}")
        
        print("Login process completed")