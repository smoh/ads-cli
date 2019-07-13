ads_cli
=======

Command-line interface to [astrophysics data system](https://ui.adsabs.harvard.edu/).

Usage
-----

There are two commands: `ads` and `adscli`.

For `ads`, check out its `--help` documentation.

```sh
# export multiple papers to bibtex
# other export formats can be specified as -f <format>
ads export 2014AJ....147..124M 2012ApJ...759....6E '2013A&A...558A..33'

# by default returns 10 entries to stdout
ads search -q 'author:"^huchra, j."'

# If not query is given, you will be prompted.
ads search    # you will be prompted.
Query: [put query here and hit <META-ENTER>]
```

`adscli` launches a terminal app.

![](demo.gif)


Key bindings:

|    cursor     | key |                  what it does                   |
|:-------------:|:---:|:-----------------------------------------------:|
| in search bar | C-s |                    Do search                    |
| in search bar | C-j | When cursor is in search bar, go to first entry |
| in item list  | j,k |            Go to next/previous entry            |
| in item list  | h,l |            Go to previous/next page             |
| in item list  |  o  |               Open article in ADS               |
| in item list  |  p  |      Open publisher PDF file for the entry      |
| in item list  |  e  |          Open arxiv PDF for the entry           |

To go back to search, go to top entry and hit `k`.

Installation
------------
```sh
pip [-e] git+https://github.com/smoh/ads-cli#egg=ads-cli
```

### Requirements

- [Andy Casey's ADS python](https://github.com/andycasey/ads)
- [click](https://click.palletsprojects.com/en/7.x/) probably v7.0 and up
- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/stable/index.html) probably v2 but not v3.
