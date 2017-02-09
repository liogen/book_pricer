Command
-------

* python manage.py startapp just_book
* scrapy crawl justbook

* Scrapyd: Start a scrapy script asynchronously in django view
    * http://stackoverflow.com/questions/26921879/starting-scrapy-from-a-django-view
    * http://scrapyd.readthedocs.io/en/latest/
* ScrapyItem: Store scrapy item in DB
    * http://marcela-campo.blogspot.fr/2015/03/scraping-website-using-scrapy-and-django.html

Todo:
-----

* Create a view that launch scrapy script
    * Create a django app
    * Create an html view with a button
    * Launch current scrapy script
* Scrap justbook.fr
    * Study scrapy
    * Scrap justbook.fr to retrieve book info and price
    * Add a parameter to scrapy to target a specific ISBN
* Store scrapy data in DB
    * Store scrapy data in DB
* Find a book
    * Create a form that retrieve information to crawl justbook.fr
    * Add loading and error message
* Book price comparison
    * Create chart that display price of a book
    * Display optimal price to sell a book
* Retrieve book information
    * Scrap website to retrieve book title, author, editor, description, rating
    * Add state of the book
* Write ads to sell book
    * With all information collected, create a ads to sell the book
    * Add 3 information photo to illustrate the book
* Create a page with all registered book
    * Display a list of all registered books