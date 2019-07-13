#!/usr/bin/env python
"""
Command-line interface to astrophysics data system
"""
import re
import logging
import urllib
from string import Template

# import ads.sandbox as ads
import ads
import click
import sys
from prompt_toolkit import PromptSession

from ads_variables import ALL_VIEWABLE_FIELDS, ads_query_completer

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
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


DEFAULT_FIELDS = ["id", "author", "first_author", "bibcode", "year", "title"]
p = re.compile("http[?s]://ui.adsabs.harvard.edu/abs/(.*)/")


def get_name(ctx, param, value):
    if not value and not click.get_text_stream("stdin").isatty():
        return click.get_text_stream("stdin").read().split()
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
@click.option(
    "--debug/--no-debug", default=False, help="debug will not actually send queries"
)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    ctx.obj["debug"] = debug


@cli.command()
@click.option("--query", "-q", type=str)
@click.option("-n", default=10, type=int, help="number of entries to get (MAX: 2000)")
@click.option("--fstring", "-f", type=str, help="format string")
@click.option(
    "--field",
    "-fl",
    type=str,
    help="comma-separated fields to get.\n"
    "Exmaples: -fl ack,aff\n"
    f"Default fields: {DEFAULT_FIELDS}",
)
@click.pass_context
def search(ctx, query, n, fstring, field):
    """Search ADS with a query

    \b
    Query string can be given either as option:
        ads search -q 'author:"huchra, j." year:2000-2005'
        (Note that the entire query must be wrapped in ''.)
    or you will be promprted to input interactively with autocompletion.
    Use meta-Enter to finish.
    """
    if ctx.obj["debug"]:
        logger.setLevel(logging.DEBUG)
    MAX_ROWS = 2000
    if n > 2000:
        raise NotImplementedError()
    rows = n

    # TODO:combine all fields in fstring and field to fl param
    if field is None:
        field = DEFAULT_FIELDS
    else:
        field = field.split(",")
        if not set(field) < set(ALL_VIEWABLE_FIELDS):
            raise click.BadParameter(
                f"invalid fields found:{set(field)-set(ALL_VIEWABLE_FIELDS)}"
            )

    if query is None:
        # https://github.com/prompt-toolkit/python-prompt-toolkit/issues/502
        if not sys.stdin.isatty():
            query = sys.stdin.read()
        else:
            if not sys.stdout.isatty():
                raise click.UsageError(
                    "You are redirecting output; in this case you need to"
                    "specify the query."
                )
            else:
                session = PromptSession(
                    # lexer=PygmentsLexer(SqlLexer),
                    completer=ads_query_completer
                )
            query = session.prompt("Query: ", multiline=True)
    query = query.replace("\n", " ").strip()
    assert query, ValueError("Must input some query!")
    logger.debug(f"query: {query} n:{n}")

    q = ads.SearchQuery(q=query, rows=n, fl=field)
    # if len(list(q)) == 0:
    #     click.echo("Your search returned nothing.")

    if fstring:
        logger.debug(f"fstring: {fstring}")
        t = Template(fstring)
        for i, a in enumerate(q):
            d = {name: getattr(a, name) for name in field}
            try:
                click.echo(t.substitute(**d))
            except KeyError:
                raise click.UsageError(
                    "output string contains fields not queried;"
                    "make sure all necessary fields are specified in --field."
                    "We do not lazy-load attributes by default."
                )
    else:
        # from adsapp import app
        # app.run()
        for i, a in enumerate(q, 1):
            click.echo(f"{i:2d} ", nl=False)
            click.secho(f"{a.title[0][:85]}", fg="blue")
            click.echo(f"   {a.first_author} {a.year} {a.bibcode}")

    logger.debug(f"Rate limit: {q.response.get_ratelimits()}")


@cli.command(help="NOT IMPLEMENTED")
@click.argument("authors", type=str)
@click.argument("year", type=str)
def lucky(authors, year):
    """Do "lucky" search on ADS

    Supported syntax:
        huchra bahcall 1999-2005 galaxy
        "huchra, j." bahcall 1999 galaxy
        "huchra, j." bahcall 1999
    """
    # yearstr =
    # q = ads.SearchQuery(author=author, year=year, abs=abs)
    # logger.debug(f"authors: {authors} year: {year}")
    raise NotImplementedError


@cli.command()
@click.option(
    "--format",
    "-f",
    default="bibtex",
    show_default=True,
    type=click.Choice(supported_export_formats),
)
@click.argument("bibcodes", nargs=-1, callback=get_name)
@click.pass_context
def export(ctx, format, bibcodes):
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
    if ctx.obj["debug"]:
        logger.setLevel(logging.DEBUG)
    # TODO: This is breaking up string if one item given from stdin.
    bibcodes = list(map(find_bibcode, bibcodes))
    logger.debug(f"bibcodes: {bibcodes}")
    if len(bibcodes) == 0:
        raise click.UsageError("At least one bibcode must be specified.")

    if not ctx.obj["debug"]:
        q = ads.ExportQuery(bibcodes, format=format)
        click.echo(q())


@cli.command(help="NOT IMPLEMENTED")
@click.argument("bibcode", nargs=-1, callback=get_name)
def download(bibcode):
    # TODO
    pass


if __name__ == "__main__":
    cli()
