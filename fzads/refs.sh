tmp=$(mktemp)
echo $tmp
ads search -fl first_author,title,abstract,year,bibcode --json -q $1 > $tmp && ./fzads $tmp