#!/bin/bash

cd ../src
make clean
make

cd ../problems
mkdir 'output'

echo "Running connected_components_single_pixel.c"
for T in {1..3}; do
	../bin/connected_components_single_pixel img22gd2.tif $T 255;
	mv connected_components.tif ./output/connected_components_$T.tif;
done


echo "Running connected_components.c"
for T in {1..3}; do
	../bin/connected_components img22gd2.tif $T 1;
	mv segmentation.tif ./output/segmentation_$T.tif;
	#Plot the segmented image
	python3 python_plot.py -T $T;
done
