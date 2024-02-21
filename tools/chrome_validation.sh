#!/bin/sh

# Edit version - type of classification here
model_version=chrome4
classification_type=topics-api
top=1000

# Variables
crux_top_domains=chrome_validation.domains
crux_classified_path=chrome_validation_chrome4.tsv


# Check if domains extracted
if [ ! -f $crux_top_domains ]
then
    crux_csv_path=crux_current.csv
    # Download CrUX top list
    wget -q -O $crux_csv_path.gz https://github.com/zakird/crux-top-lists/raw/main/data/global/current.csv.gz
    gzip -cdk $crux_csv_path.gz > $crux_csv_path

    sed -nr "s/https?:\/\/(.*),.*/\1/p" $crux_csv_path > $crux_top_domains.tmp
    shuf -n $top $crux_top_domains.tmp > $crux_top_domains

    rm $crux_top_domains.tmp $crux_csv_path.gz $crux_csv_path
fi

if [ ! -f $crux_classified_path ]
then
    #Header
    echo "domain\ttopic" > $crux_classified_path
    #Parallel inference
    parallel -X --bar -N 50 -a $crux_top_domains -I @@ "python3 ../classify.py -mv $model_version -ct $classification_type -i @@ >> $crux_classified_path"
fi