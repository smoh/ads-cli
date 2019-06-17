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

p = re.compile("http[?s]://ui.adsabs.harvard.edu/abs/(.*)/")


def find_bibcode(s):
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
    print('"' in query)
    print(query)
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
    logger.info("bibcodes:", bibcodes)
    print(bibcodes)

    bibcodes = list(map(find_bibcode, bibcodes))
    print(bibcodes)

    # q = ads.ExportQuery(bibcodes, format=format)
    # print(q())

    # logger.info(q.response.get_ratelimits())
    # print(q.response.get_ratelimits())


@cli.command()
def download(bibcode):
    pass


if __name__ == "__main__":
    cli()
