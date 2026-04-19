unhinged-units 🍌
=================

    Because sometimes you just need to know how many bananas a blue whale is.

**unhinged-units** is a Python unit conversion library (forked from Pint_)
that ships with fun units alongside Pint's full scientific unit system.

Quick Start
-----------

.. code-block:: bash

    $ pip install unhinged-units

.. code-block:: python

    >>> from unhinged_units import Q_
    >>> Q_(1, "blue_whale").to("golden_retriever")
    <Quantity(4724.41..., 'golden_retriever')>
    >>> Q_(1, "marathon").to("banana_length")
    <Quantity(46816.47..., 'banana_length')>
    >>> Q_(60, "mile/hour").to("banana_length/second")
    <Quantity(150.9..., 'banana_length / second')>

Because Pint does the math, compound units and dimensional analysis just
work. Every valid Pint operation works unchanged — we only *add* units;
we never modify or remove Pint's existing definitions.

Featured Units
--------------

A taste of what ships in the catalog:

=============================  ==========================================
Unit                           Roughly
=============================  ==========================================
``banana_length``              17.78 cm (the universal scale reference)
``football_field``             91.44 m
``eiffel_tower``               330 m
``blue_whale``                 150,000 kg
``golden_retriever``           31.75 kg
``mass_of_sun``                1.989e30 kg
``tiktok``                     30 seconds
``meeting_that_could_have_been_an_email``  1 hour
``usain_bolt``                 10.44 m/s
``big_mac``                    563 kcal
``t_rex_bite``                 57,000 N
``library_of_congress``        ~10 TB
=============================  ==========================================

See ``pint/unhinged_en.txt`` for the full list.

Comparison Mode
---------------

.. code-block:: python

    >>> from unhinged_units import compare, Q_
    >>> compare(Q_(10, "km"))
    10 kilometer is approximately:
      109.4 football_field
      56266.6 banana_length
      30.3 eiffel_tower

Full Pint Compatibility
-----------------------

Everything Pint_ can do, unhinged-units can do — plus bananas. NumPy,
Pandas (via pint-pandas), custom definitions, and
the rest of the Pint API all work unchanged.

Why?
----

Why not? 

Adding Your Own Units
---------------------

New units are defined in ``pint/unhinged_en.txt`` as plain-text lines
referencing Pint's base units, e.g.::

    corgi_length = 0.305 * meter  # Source: wikipedia/Pembroke_Welsh_Corgi

Add a unit, add a test in ``unhinged_units/tests/``, open a PR.

License
-------

BSD (same as Pint). Go nuts. Measure nuts. In whatever units you want.

Built on Pint
-------------

unhinged-units is a fork of the excellent Pint_ library. Full Pint docs
apply. Upstream attribution is preserved in ``AUTHORS`` and ``LICENSE``.

.. _Pint: https://github.com/hgrecco/pint
