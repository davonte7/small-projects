#!/bin/bash

DIRECTORY=$1

find $1 -type f -name "*.py" | while read script; do
echo "$script";
echo Removing Unused Imports;
python -m autoflake --in-place --remove-all-unused-imports $script;

echo Finding All Imports;
python extractor.py $script;
done

python reducer.py

echo imports written to found_imports.txt
