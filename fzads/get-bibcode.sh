#!/bin/bash
idx=$1
jqstr=".docs[${idx}] | .bibcode"
# jqstr=".docs[${idx}]"
jq -r ".docs[${idx}] | .bibcode" $2
# echo $idx