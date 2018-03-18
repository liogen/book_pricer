Command
-------

* python manage.py startapp just_book
* scrapy crawl justbook
* pip install python-scrapyd-api
* pip install scrapyd
* pip install 'git+https://github.com/scrapy/scrapyd-client.git@1.1.0dev'
* pip install django 1.10
* scrapyd
* scrapyd-deploy -l
* scrapyd-deploy default -p justbookcrawler
* pip install django-livereload-server

* Scrapyd: Start a scrapy script asynchronously in django view
    * http://stackoverflow.com/questions/26921879/starting-scrapy-from-a-django-view
    * http://scrapyd.readthedocs.io/en/latest/
    * https://pypi.python.org/pypi/python-scrapyd-api
* ScrapyItem: Store scrapy item in DB
    * http://marcela-campo.blogspot.fr/2015/03/scraping-website-using-scrapy-and-django.html
    * http://stackoverflow.com/questions/19068308/access-django-models-with-scrapy-defining-path-to-django-project

Todo:
-----

* Find a book
    * Write what is? page
        * Add a band with information about the site, number of books, number of offer collected, average price for a book
* Book price comparison
    * Create chart that display price of a book
    * Display optimal price to sell a book
* Write ads to sell book
    * With all information collected, create a ads to sell the book
    * Add 3 information photo to illustrate the book
* Create a page with all registered book
    * Display a list of all registered books

* Code cleaning and test
    * Install django-bower and install dependencies using it
    * Try to use only web component if relevant or django include
    * Try to minify code (html, css, js)
    * Pass prospector code on python
    * Add setup.py to install code
    * Deploy on raspberry pi (git clone + python install setup.py)
    * Find a free DNS provider
    * Add nginx to project installation
    * Create a snap if relevant
    * Deploy on github



