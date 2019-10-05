import json
from colorama import Fore, Back, Style

import sys

# take file name of json data
fn = sys.argv[1]
with open(fn) as f:
    d = json.load(f)


def print_line(idx, paper):
    s = (
        Style.DIM
        + "{:4d}".format(idx)
        + Style.RESET_ALL
        + "›{}".format(paper.pop("first_author", ""))
        + Fore.BLUE
        + " {}".format(paper.pop("year", "????"))
        + Style.RESET_ALL
        + " {}".format(paper["title"][0])
    )
    print(s)


for i, p in enumerate(d["docs"]):
    print_line(i, p)
