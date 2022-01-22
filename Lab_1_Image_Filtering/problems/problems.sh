#!/bin/bash

cd ../src
make clean
make

cd ../problems
mkdir 'output'
echo "Running FIR Low Pass Filter"
../bin/FIR_LP_4 img03.tif
mv color_filtered.tif output
echo ""
python3 python_FIR_LP.py


echo "Running FIR Sharpeing Filter"
declare -a lambda=(0.2 0.8 1.5 5)
for i in "${lambda[@]}"; do
	echo "Lambda = "$i
	../bin/FIR_Sharp_3 imgblur.tif $i;
	mv sharpened_image_$i.tif output;
done
echo ""
python3 python_plot.py

echo "Running IIR Filter"
../bin/IIR_3 img03.tif
mv IIR_filtered.tif output
echo ""
python3 python_IIR_filter.py

