# step_definitions/reddit_steps.py
import pytest
from pytest_bdd import given, when, then, scenario
from pages.reddit_page import RedditPage
from pages.login_page import LoginPage
from pages.gaming_subreddit_page import GamingSubredditPage

@scenario('../features/reddit_automation.feature', 'Vote on gaming subreddit posts based on Nintendo content')
def test_reddit_automation():
    pass

@given('I am on old reddit homepage')
def navigate_to_reddit(page):
    print("Step: Navigating to old Reddit homepage")
    reddit_page = RedditPage(page)
    reddit_page.navigate_to_homepage()
    print("✓ Successfully navigated to old Reddit")

@when('I login to Reddit')
def login_to_reddit(page, reddit_credentials):
    print("Step: Logging into Reddit")
    login_page = LoginPage(page)
    login_page.perform_login(reddit_credentials['username'], reddit_credentials['password'])
    print("✓ Login process completed")

@when('I navigate to the gaming subreddit')
def navigate_to_gaming_subreddit(page):
    print("Step: Navigating to gaming subreddit")
    reddit_page = RedditPage(page)
    reddit_page.navigate_to_gaming_subreddit()
    print("✓ Navigated to gaming subreddit")

@when('I find the second non-pinned, non-ad post')
def find_second_valid_post(page):
    print("Step: Finding second valid post")
    gaming_page = GamingSubredditPage(page)
    gaming_page.find_second_non_pinned_non_ad_post()
    print("✓ Found second valid post")

@then('I should vote thumbs up if the title contains "Nintendo"')
def vote_based_on_nintendo_content(page):
    print("Step: Voting on post based on Nintendo content")
    gaming_page = GamingSubredditPage(page)
    gaming_page.vote_on_post_based_on_nintendo_content()
    print("✓ Voting completed")

@then('I should vote thumbs down if the title does not contain "Nintendo"')
def vote_down_if_no_nintendo(page):
    print("✓ Vote down logic included in Nintendo check")

@then('Or I should vote thumbs down if the title does not contain "Nintendo"')
def vote_down_or_step(page):
    print("✓ Or step - Vote down logic included in Nintendo check")

@then('I logout from Reddit')
def logout_from_reddit(page):
    print("Step: Logging out from Reddit")
    reddit_page = RedditPage(page)
    reddit_page.logout()
    print("✓ Logged out successfully")