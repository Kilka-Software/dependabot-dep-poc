How To Contribute
=================

Initial setup
-------------


Workflow
--------

Code
----

- Obey `PEP 8`_ and `PEP 257`_.
  We use the ``"""``\ -on-separate-lines style for docstrings:

  .. code-block:: python

     def func(x):
         """
         Do something.

         :param str x: A very important parameter.

         :rtype: str
         """
- We use isort_ to sort our imports, and we follow the Black_ code style with a line length of 90 characters.
  As long as you run our full tox suite before committing, or install our pre-commit_ hooks (ideally you'll do both -- see below "Local Development Environment"), you won't have to spend any time on formatting your code at all.
  If you don't, CI will catch it for you -- but that seems like a waste of your time!


Tests
-----

- Write your asserts as ``expected == actual`` to line them up nicely:

  .. code-block:: python

     x = f()

     assert 42 == x.some_attribute
     assert "foo" == x._a_private_attribute

- To run the test suite, all you need is a recent tox_.
  It will ensure the test suite runs with all dependencies against all supported Python versions just as it will in our CI.
  If you lack some Python versions, you can can always limit the environments like ``tox -e py38,py39`` (in that case you may want to look into pyenv_, which makes it very easy to install many different Python versions in parallel).
- Write `good test docstrings`_.


Documentation
-------------

- Use `semantic newlines`_ in reStructuredText_ files (files ending in ``.rst``):

  .. code-block:: rst

     This is a sentence.
     This is another sentence.

- If you start a new section, add two blank lines before and one blank line after the header, except if two headers follow immediately after each other:

  .. code-block:: rst

     Last line of previous section.


     Header of New Top Section
     -------------------------

     Header of New Section
     ^^^^^^^^^^^^^^^^^^^^^

     First line of new section.



Changelog
^^^^^^^^^

If your change is noteworthy, there needs to be a changelog entry.

To avoid merge conflicts, we use the towncrier_ package to manage our changelog.
``towncrier`` uses independent files for each pull request -- so called *news fragments* -- instead of one monolithic changelog file.
On release, those news fragments are compiled into our ``CHANGELOG.rst``.

You don't need to install ``towncrier`` yourself, you just have to abide by a few simple rules:

- For each pull request, add a new file into ``changelog.d`` with a filename adhering to the ``pr#.(change|deprecation|breaking).rst`` schema:
  For example, ``changelog.d/42.change.rst`` for a non-breaking change that is proposed in pull request #42.
- As with other docs, please use `semantic newlines`_ within news fragments.
- Wrap symbols like modules, functions, or classes into double backticks so they are rendered in a ``monospace font``.
- Wrap arguments into asterisks like in docstrings: *these* or *attributes*.
- If you mention functions or other callables, add parentheses at the end of their names: ``jsr_core.func()`` or ``jsr_core.Class.method()``.
  This makes the changelog a lot more readable.
- Prefer simple past tense or constructions with "now".
  For example:

  + Added ``jsr_core.api.func()``.
  + ``jsr_core.func()`` now doesn't crash anymore when passed the *foobar* argument.
- If you want to reference multiple issues, copy the news fragment to another filename.
  ``towncrier`` will merge all news fragments with identical contents into one entry with multiple links to the respective pull requests.

Example entries:

  .. code-block:: rst

     Added ``jsr_core.api.func()``.
     At long last.

or:

  .. code-block:: rst

     ``jsr_core.func()`` now doesn't crash anymore when passed the *foobar* argument.
     The bug really *was* nasty.

----

``tox -e changelog`` will render the current changelog to the terminal if you have any doubts.


Local Development Environment
-----------------------------

You can (and should) run our test suite using tox_.
However, you’ll probably want a more traditional environment as well.
First, set up the virtual environment and install the dependencies using pipenv_:

.. code-block:: bash

    $ pipenv install --dev

At this point,

.. code-block:: bash

   $ python -m pytest

should work and pass, as should:

.. code-block:: bash

   $ cd docs
   $ make html

The built documentation can then be found in ``docs/_build/html/``.

To avoid committing code that violates our style guide, we strongly advise you to install pre-commit_ [#f1]_ hooks:

.. code-block:: bash

   $ pre-commit install

You can also run them anytime (as our tox does) using:

.. code-block:: bash

   $ pre-commit run --all-files


.. [#f1] pre-commit should have been installed into your virtualenv automatically when you ran ``pipenv install --dev`` above. If pre-commit is missing, it may be that you need to re-run ``pipenv install --dev``.



.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/
.. _`PEP 257`: https://www.python.org/dev/peps/pep-0257/
.. _`good test docstrings`: https://jml.io/pages/test-docstrings.html
.. _tox: https://tox.readthedocs.io/
.. _pyenv: https://github.com/pyenv/pyenv
.. _pipenv: https://github.com/pypa/pipenv
.. _reStructuredText: https://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html
.. _semantic newlines: https://rhodesmill.org/brandon/2012/one-sentence-per-line/
.. _towncrier: https://pypi.org/project/towncrier
.. _black: https://github.com/psf/black
.. _pre-commit: https://pre-commit.com/
.. _isort: https://github.com/PyCQA/isort
