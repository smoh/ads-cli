"""ADS related variables"""
from prompt_toolkit.completion import WordCompleter

__all__ = ["ALL_VIEWABLE_FIELDS", "ads_query_completer"]

#TODO: This is not complete.
ALL_VIEWABLE_FIELDS = [
    "abstract",
    "ack",
    "aff",
    "alternate_bibcode",
    "alternate_title",
    "arxiv_class",
    "author",
    "author_count",
    "author_norm",
    "bibcode",
    "bibgroup",
    "bibstem",
    "citation",
    "citation_count",
    "cite_read_boost",
    "classic_factor",
    "copyright",
    "data",
    "date",
    "doctype",
    "doi",
    "first_author",
    "identifier",
    "keyword",
    "page",
    "read_count",
    "voluem",
    "year",
]

ads_query_completer = WordCompleter(
    [
        "author:",
        "first_author:",
        "year:",
        "property:",
        "title:",
        "bibcode:",
        "identifier:",
        "doi:",
    ],
    ignore_case=True,
)
