#!/bin/bash
cd /Users/keplerdomurat-sousa/Desktop/electron_cascade_tests/run_zone/
rm ./*

/Applications/topas/bin/topas ../phasespace_HGM_run.topas

for i in {0..28}; do
	echo "$i iteration"
	python3 ../secondary_electron_bodge.py
	/Applications/topas/bin/topas ../load_phasespace_HGM.topas
done


