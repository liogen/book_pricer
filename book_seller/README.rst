Command
-------

* python manage.py startapp just_book
* scrapy crawl justbook
* pip install python-scrapyd-api
* pip install scrapyd
* pip install 'git+https://github.com/scrapy/scrapyd-client.git@1.1.0dev'
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
    * If user click on find a book by isbn, you should scroll to the book list section and display a loading message during
    retrieving of book information :
        * If information are stored in DB or not update to date (less than two days), display only this book with a link to
         get more information
        * If information are not stored in DB and up-to-date, display a loading while crawler complete is job
        * Display error message if needed
            * no book title in DB mean that the book does not exist
            * no offer in DB mean that we can not find the book
* Book price comparison
    * Create chart that display price of a book
    * Display optimal price to sell a book
* Retrieve book information
    * Scrap website to retrieve book title, author, editor, description, rating
    * Add condition of the book that you want to sell
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



