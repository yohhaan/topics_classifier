#!/bin/bash

html_taxonomy=$1
tsv_taxonomy=$2

tmp_taxonomy=taxonomy.tmp

if [ ! -f $tsv_taxonomy ]
then
    #extract with sed and replace formatting
    sed -nr "s/.*<td>(.*)<\/td>/\1/p" $html_taxonomy > $tmp_taxonomy
    sed -i -e "s/amp;//g" -e "s/&#39;/\'/g" $tmp_taxonomy
    paste -d '\t' - - < $tmp_taxonomy > $tsv_taxonomy
    rm $tmp_taxonomy
fi
