import json
from colorama import Fore, Back, Style

import sys


# take index and file name
idx, fn = sys.argv[1:]
with open(fn) as f:
    d = json.load(f)

p = d["docs"][int(idx)]
print(Style.BRIGHT + Fore.BLUE + "TITLE: " + Fore.WHITE + p["title"][0])
print(Style.BRIGHT + Fore.BLUE + "AUTHOR: " + Fore.WHITE + p["first_author"])
print(Style.BRIGHT + Fore.BLUE + "YEAR: " + Fore.WHITE + p["year"])
print(Style.BRIGHT + Fore.BLUE + "BIBCODE: " + Fore.WHITE + p["bibcode"])
print(Style.BRIGHT + Fore.BLUE + "ABSTRACT:")
print(Style.RESET_ALL + Fore.BLACK + str(p.pop("abstract", "N/A")))
