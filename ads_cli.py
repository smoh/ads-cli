#!/usr/bin/env python
"""
Command-line interface to astrophysics data system
"""
import re
import logging
import urllib

# import ads.sandbox as ads
import ads
import click

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

p = re.compile("http[?s]://ui.adsabs.harvard.edu/abs/(.*)/")


def find_bibcode(s):
    """Find ADS bibcode from string
    """
    if not s.startswith("http"):
        return s
    else:
        m = p.findall(s)
        if len(m) != 1:
            raise ValueError(f"cannot extract bibcode from url={s}")
        return urllib.parse.unquote(m[0])


@click.group()
def cli():
    pass


@cli.command()
@click.option("--query", "-q", prompt="Query")
def search(query):
    """Search ADS
    """
    logger.debug(f"query: {query}")
    # q = ads.SearchQuery(q=query, rows=10)
    # for i, a in enumerate(q, 1):
    #     click.echo(f"{i:2d} {a.title[0][:85]}")
    # print(q.response.get_ratelimits())


@cli.command()
@click.option(
    "--format", default="bibtex", show_default=True, type=click.Choice(["bibtex"])
)
@click.argument("bibcodes", nargs=-1, required=True)
def export(format, bibcodes):
    """
    Export article citation

    NOTE: If a bibcode contains `&` e.g., "2017A&A...608A.116C",
    either `&` needs to be escaped as in
    
    $ads-cli export 2017A\&A...608A.116C
    
    or put in quotes

    $ads-cli export "2017A&A...608A.116C"

    because in bash, `&` means put process in the background.
    """
    bibcodes = list(map(find_bibcode, bibcodes))
    logger.debug(f"bibcodes: {bibcodes}")

    q = ads.ExportQuery(bibcodes, format=format)
    # print(q())
    # logger.debug(f"Rate limit: f{q.response.get_ratelimits()}")


@cli.command()
def download(bibcode):
    pass


if __name__ == "__main__":
    cli()
