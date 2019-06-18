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
ch = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

supported_export_formats = [
    "bibtex",
    "bibtexabs",
    "ads",
    "endnote",
    "proctie",
    "ris",
    "refworks",
    "rss",
    "medlars",
    "dcxml",
    "refxml",
    "refabsxml",
    "aastex",
    "icarus",
    "mnras",
    "soph",
    "votable",
    # "custom"   # TODO: requires additional parameter
]
# monkey-patch class attribute
ads.ExportQuery.FORMATS = supported_export_formats


p = re.compile("http[?s]://ui.adsabs.harvard.edu/abs/(.*)/")


def get_name(ctx, param, value):
    if not value and not click.get_text_stream("stdin").isatty():
        return click.get_text_stream("stdin").read().strip()
    else:
        return value


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
    q = ads.SearchQuery(q=query, rows=10)
    for i, a in enumerate(q, 1):
        click.echo(f"{i:2d} ", nl=False)
        click.secho(f"{a.title[0][:85]}", fg="blue")
        click.echo(f"   {a.first_author} {a.year} {a.bibcode}")
    logger.debug(f"Rate limit: {q.response.get_ratelimits()}")

    while True:
        ix = click.prompt("Please enter article number", type=int)
        if (ix >= 1) & (ix <= 10):
            break
    bibcode = q.articles[ix - 1].bibcode
    click.echo(bibcode)

    # click.prompt("Actions?", type=click.Choice(('e','d')))


@cli.command()
@click.option(
    "--format",
    "-f",
    default="bibtex",
    show_default=True,
    type=click.Choice(supported_export_formats),
)
@click.argument("bibcodes", nargs=-1, callback=get_name)
def export(format, bibcodes):
    """
    Export article(s) to the specified format.

    - Export one article to bibtex:

        ads export 2005IAUS..216..170H
    
    - Export multiple articles to bibtex:

        ads export 2005IAUS..216..170H '2017A&A...608A.116C'
    
    NOTE: If a bibcode contains `&` e.g., "2017A&A...608A.116C",
    either `&` needs to be escaped as in
    
        ads export 2017A\&A...608A.116C
    
    or put in quotes

        ads export "2017A&A...608A.116C"

    because in bash, `&` means put process in the background.
    """
    # TODO: This is breaking up string if one item given from stdin.
    bibcodes = list(map(find_bibcode, bibcodes))
    logger.debug(f"bibcodes: {bibcodes}")

    # q = ads.ExportQuery(bibcodes, format=format)
    # print(q())
    # logger.debug(f"Rate limit: {q.response.get_ratelimits()}")


@cli.command()
def download(bibcode):
    pass


if __name__ == "__main__":
    cli()
