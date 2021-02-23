#!/bin/bash

echo "Ingesting sample data"

SHARED_DIR=$1
DATA_DIR=$2

if [ -f "$SHARED_DIR/configs/variables" ]; then
  . "$SHARED_DIR"/configs/variables
fi

cd "$DRUPAL_HOME" || exit

drush -u 1  islandora_batch_scan_preprocess \
   --type=directory \
   --scan_target=$DATA_DIR/newspapers \
   --content_models=islandora:newspaperCModel \
   --parent=islandora:newspaper_collection \
   --namespace=newspapers \
   --output_set_id
drush -v -u 1 islandora_batch_ingest

for i in `ls $DATA_DIR/ | sed 's/^newspapers.*//'`:
do
  echo $i
  drush -u 1  islandora_newspaper_batch_preprocess \
    --type=directory \
    --scan_target=$DATA_DIR/$i \
    --parent=newspapers:1 \
    --namespace=$i  \
    --do_not_generate_ocr \
    --do_not_generate_hocr \
    --output_set_id
done

drush -u 1 islandora_batch_ingest