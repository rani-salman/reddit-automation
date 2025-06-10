from playwright.sync_api import Page
import time

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
    def wait_for_element(self, selector, timeout=10000):
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def click_element(self, selector):
        element = self.wait_for_element(selector)
        element.click()
        
    def fill_input(self, selector, text):
        element = self.wait_for_element(selector)
        element.fill(text)
        
    def get_text(self, selector):
        element = self.wait_for_element(selector)
        return element.text_content()
