#!/bin/bash
jq -C -r '.docs[] | [.title[0], .first_author] | @csv' $1 | nl -w 3 -v 0|\
fzf -m --ansi --reverse --border \
  --header="this is header line" \
  --preview="echo {} | cut -f 1 | xargs -I{} python preview.py {} $1" --preview-window=down:50%:wrap\
  --bind "ctrl-o:execute-silent[echo {}|cut -f1 | xargs -I{} ./get-bibcode.sh {} $1| xargs ads open]"\
  --bind "ctrl-i:execute-silent[echo {}|cut -f1 | xargs -I{} ./get-bibcode.sh {} $1| xargs ads open --pdf]"\
  --bind "f7:cancel+execute! echo {} | cut -f1 | xargs -I{} ./get-bibcode.sh {} $1| xargs -I{} echo references\(bibcode:{}\) | xargs ./refs.sh!"

