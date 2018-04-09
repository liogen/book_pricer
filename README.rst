.. image:: https://travis-ci.org/liogen/book_pricer.svg?branch=develop
    :target: https://travis-ci.org/liogen/book_pricer

.. image:: https://coveralls.io/repos/github/liogen/book_pricer/badge.svg?branch=develop
    :target: https://coveralls.io/github/liogen/book_pricer?branch=develop

.. image:: https://codeclimate.com/github/liogen/book_pricer/badges/gpa.svg
    :target: https://codeclimate.com/github/liogen/book_pricer
    :alt: Code Climate

BookPricer
==========

Book pricer is the best app to define your used books price.

Goals of this project
---------------------

This project focuses on providing an intuitive and complete tools that help you to define your used books price using data available on the https://www.justbooks.fr/ price comparator.

Quick presentation
------------------

User interface
~~~~~~~~~~~~~~

In this application, you just have to enter your book's ISBN and you will get a price distribution of the news and used offers available on the Web. The last step for you is to pick up the correct price according to the price distribution and sell on your preferred website.

TODO: add pictures

Admin presentation
~~~~~~~~~~~~~~~~~~

To see the datamodel and the data in DB, go to localhost:8080/admin (book_seller / book_seller_Admin).

TODO: add pictures

Installation guide
------------------

This project is only available on Ubuntu/Debian. Tested on Ubuntu 16.04.

Packages installation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ sudo apt-get install python3 python3-dev python-pip sqlite3 supervisor

Virtualenv creation
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ sudo -H pip install virtualenvwrapper
    $ mkdir ~/.virtualenvs
    $ echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
    $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    $ bash
    $ mkvirtualenv book_seller --python=/usr/bin/python3
    $ workon book_seller

Pip requirements installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ pip install -r requirements.txt

Django configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd book_seller
    $ python manage.py migrate --settings=book_seller.settings.prod
    $ python manage.py createsuperuser (book_seller / book_seller_Admin)

Scrapy configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd ..
    $ pip install python-scrapyd-api scrapyd 'git+https://github.com/scrapy/scrapyd-client.git@1.1.0dev'
    $ cd justbookcrawler
    $ scrapyd-deploy -l
    $ scrapyd-deploy default -p justbookcrawler

Supervisor configuration and run
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ sudo cp supervisor/* /etc/supervisor.conf.d/
    $ sudo reread
    $ sudo add book_seller
    $ sudo add justbookcrawler
    $ sudo supervisorctl start book_seller
    $ sudo supervisorctl start justbookcrawler
    $ tail -f /tmp/book_seller.log

Contribute
----------

This project is distributed under the MIT licence.

To test the quality, run this commands :

.. code-block:: bash

    $ pip install flake8 prospector django_nose behave_django coverage
    $ flake8 --exclude "justbookcrawler/build/"
    $ prospector -F
    $ coverage run --source='.' manage.py behave --settings=book_seller.settings.test && coverage report -m

To fix a bug, open an issue in github and submit a pull request.

Todo
----

* Integrate project on travis
* Integrate project on coveralls
* Correct code climate error
* Fix crawler problem
* Write Readme

