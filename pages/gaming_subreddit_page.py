from pages.base_page import BasePage
import time

class GamingSubredditPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.posts_selector = ".thing:not(.stickied):not(.promoted)"
        self.post_title_selector = ".title a.title"
        self.upvote_button = ".arrow.up"
        self.downvote_button = ".arrow.down"
        self.current_post = None
        
    def find_second_non_pinned_non_ad_post(self):
        # Wait for posts to load
        self.page.wait_for_selector(self.posts_selector, timeout=15000)
        time.sleep(2)
        
        # Get all valid posts (not pinned, not ads)
        posts = self.page.locator(self.posts_selector).all()
        
        if len(posts) < 2:
            raise Exception("Not enough valid posts found")
            
        # Get the second valid post
        self.current_post = posts[1]
        return self.current_post
        
    def get_post_title(self):
        if not self.current_post:
            raise Exception("No current post selected")
            
        title_element = self.current_post.locator(self.post_title_selector)
        return title_element.text_content().strip()
        
    def vote_on_post_based_on_nintendo_content(self):
        if not self.current_post:
            self.find_second_non_pinned_non_ad_post()
            
        title = self.get_post_title()
        print(f"Post title: {title}")
        
        if "nintendo" in title.lower():
            print("Title contains 'Nintendo' - voting up")
            self.vote_up()
        else:
            print("Title does not contain 'Nintendo' - voting down")
            self.vote_down()
            
    def vote_up(self):
        upvote_btn = self.current_post.locator(self.upvote_button)
        upvote_btn.click()
        time.sleep(1)
        
    def vote_down(self):
        downvote_btn = self.current_post.locator(self.downvote_button)
        downvote_btn.click()
        time.sleep(1)