========
Dependabot Depandacy Tester POC
========

Summary
-------

This is a library that we are going to use to test depandabot by including it in our POC to test the Github Dependabot.

Development
-----------

Initial setup of development environment:

.. code-block:: bash

    $ pipenv install --dev


Install the git pre-commit hooks:

.. code-block:: bash

    $ pipenv run pre-commit install

Releasing
---------

Creates a new tag on Github everytime there is a ush to main. Thet is the sole purpose of this project. To Create new tags that can be detected by dependabot in the dependabot-impl-poc project, that implements the dependabot
