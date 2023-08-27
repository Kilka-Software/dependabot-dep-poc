Overview
========

``jsr_core`` provides the core business logic and data access for the JaSure Insurance Platform.
All of JaSure's backend services, workers and APIs use ``jsr_core`` to perform any business logic or access any data.

To begin using ``jsr_core``, you should start by getting a correctly configured instance of :class:`jsr_core.core.Core`.
The easiest way to do this is to use :ref:`one of the supplied shortcut methods <core-shortcuts>` in the root module.


.. _core-shortcuts:

Core Shortcut Factories
-----------------------

These are shortcut functions provided to quickly create a :class:`jsr_core.core.Core` instance for the appropriate use-case.

.. autofunction:: jsr_core.create_for_development

.. autofunction:: jsr_core.create_for_testing

.. autofunction:: jsr_core.create_with_ssm

.. autofunction:: jsr_core.create_for_appsync
