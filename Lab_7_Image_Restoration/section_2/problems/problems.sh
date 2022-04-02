#!/bin/bash

cd ../src
make clean
make

cd ../problems
mkdir 'output'
echo "Running Weighted Median Filter"
../bin/section_2 ../../../images-restoration/img14bl.tif
mv section_2_filtered.tif output
echo ""
