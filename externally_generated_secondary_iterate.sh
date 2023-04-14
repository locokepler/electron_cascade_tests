#!/bin/bash
# cd ~/electron_cascade_tests
make secondaries
cd run_zone/
rm ./*
rm ../$2
cp ../$1 ./
mv $1 full_HGM.phsp

for i in {0..60}; do
	echo "$i iteration"
	../secondaries full_HGM timings output backplane.phsp ../$2
	retVal=$?
	if [$retVal -ne 0]; then
		exit $retVal
	fi
	# rm backplane.phsp backplane.header
	~/topas/bin/topas ../load_phasespace_HGM.topas
	retVal=$?
	if [$retVal -ne 0]; then
		exit $retVal
	fi

done


