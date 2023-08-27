===========================================
``jsr_core``\ : JaSure's Insurance Platform
===========================================

Release v\ |release| (:doc:`What's new? <changes>`).

``jsr_core`` is the core business logic layer of the JaSure Insurance Platform.


Getting Started
===============

``jsr_core`` is supplied as an installable universal Python package obtained either via a vendored wheel or via an interal PyPi server:

.. code-block:: console

    $ pip install jsr_core


Most usage of ``jsr_core`` should be via the supplied APIs using a properly configured :class:`jsr_core.core.Core` instance, but direct access to the underlying schema is also possible.

For local development a shortcut factory method is supplied:

.. code-block:: python

    import jsr_core
    from jsr_core.api import people

    core = jsr_core.create_for_development(config={})

    # Load a person:
    person = people.Person.get(core.s, "<person uuid>")


If you just need to use ``jsr-core`` the following next steps are for you:

- Review the :doc:`usage instructions <overview>`.
- Look over the :doc:`Key Concepts <concepts>` in the JaSure Insurance Platform.

For developers of ``jsr_core``:

- Read the :doc:`guide to getting started developing <contributing>`


Full Table of Contents
======================

.. toctree::
    :maxdepth: 2

    overview
    concepts
    contributing
    structure
    api
    changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
