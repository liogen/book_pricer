Feature: Backup command
    As a end-user,
    I want to retrieve price distribution of a book,
    in order to define the best price of my book

    @wipa
    Scenario: 1.Price crawl
        When I ask for an ISBN book to crawl
        Then I should see the book in DB
