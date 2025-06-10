Feature: Reddit Gaming Subreddit Automation
  As a test automation engineer
  I want to automate Reddit interactions
  So that I can vote on gaming posts based on Nintendo content

  Scenario: Vote on gaming subreddit posts based on Nintendo content
    Given I am on old reddit homepage
    When I login to Reddit
    And I navigate to the gaming subreddit
    And I find the second non-pinned, non-ad post
    Then I should vote thumbs up if the title contains "Nintendo"
    Or I should vote thumbs down if the title does not contain "Nintendo"
    And I logout from Reddit