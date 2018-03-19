[program:book_seller]
command=/home/vagrant/.virtualenvs/book_seller/bin/gunicorn book_seller.wsgi:application --reload
directory=/vagrant/book_seller/
user=vagrant
autostart=true
autorestart=true
redirect_stderr=true

[program:justbookcrawler]
command=/home/vagrant/.virtualenvs/book_seller/bin/scrapyd
directory=/vagrant/justbookcrawler
user=/vagrant
autostart=true
autorestart=true
redirect_stderr=true


* sudo supervisorctl start book_seller
* sudo supervisorctl start justbookcrawler
* tail -f /tmp/book_seller.log

OS requirements
Ubuntu/Debian

Package requirements
    sudo apt-get install python3 python3-dev python-pip sqlite3 supervisor

Virtualenv
    sudo -H pip install virtualenvwrapper
    mkdir ~/.virtualenvs
    echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    bash
    mkvirtualenv <project_name> --python=/usr/bin/python3
    workon book_seller

pip requirements
    * Install pip requirements

Scrapy
    * Deploy scrapy project

Supervisor conf
    * Install supervisor conf


sudo apt-get lsscrapyd-deploy

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

Interface
* Dexrption and features

Admin
* URL
* Login and password
* Quick presentation

Quality
* Prospector
* pip install flake8 prospector
* flake8 --exclude "justbookcrawler/build/"
* prospector -F