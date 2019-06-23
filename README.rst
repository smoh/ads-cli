ads_cli
=======

.. .. image:: https://img.shields.io/pypi/v/ads-cli.svg
..     :target: https://pypi.python.org/pypi/ads-cli
..     :alt: Latest PyPI version

.. .. image:: https://travis-ci.org/borntyping/cookiecutter-pypackage-minimal.png
..    :target: https://travis-ci.org/borntyping/cookiecutter-pypackage-minimal
..    :alt: Latest Travis CI build status

Command-line interface to ADS

Usage
-----
.. code-block:: bash

    ads export 2014AJ....147..124M 2012ApJ...759....6E '2013A&A...558A..33'
    
    ads search -n 10 -q 'author:"^huchra, j."'

    ads search    # you will be prompted.
    Query: [put query here and hit <META-ENTER>]

Installation
------------

.. code-block:: sh

  pip [-e] git+https://github.com/smoh/ads-cli#egg=ads-cli

Requirements
^^^^^^^^^^^^

Authors
-------

`ads_cli` was written by `Semyeong Oh <semyeong.oh@gmail.com>`_.
