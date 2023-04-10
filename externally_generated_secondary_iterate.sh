#!/bin/bash
cd /Users/keplerdomurat-sousa/Desktop/electron_cascade_tests
make secondaries
cd /Users/keplerdomurat-sousa/Desktop/electron_cascade_tests/run_zone/
rm ./*
rm ../$2
cp ../$1 ./
mv $1 full_HGM.phsp

for i in {0..28}; do
	echo "$i iteration"
	../secondaries full_HGM timings output backplane.phsp ../$2
	/Applications/topas/bin/topas ../load_phasespace_HGM.topas
done


