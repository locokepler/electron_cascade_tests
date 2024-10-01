#!/bin/bash
# cd ~/electron_cascade_tests
make secondaries
if [ ! -d "run_zone" ]; then
	mkdir run_zone
fi
cd run_zone/
pwd
rm ../run_zone/* # just a little protection so it can't accidentally delete the parent directory's contents
# ask me why I set it up this way lol
rm ../$2
cp ../$1 ./
mv $1 full_HGM.phsp

for i in {0..20}; do
	echo "$i iteration"
	../secondaries full_HGM timings output backplane.phsp ../$2
	# retVal=$?
	# if [$retVal -ne 0]; then
	# 	exit $retVal
	# fi
	# rm backplane.phsp backplane.header
	/Applications/topas/bin/topas ../load_phasespace_HGM.topas
	# retVal=$?
	# if [$retVal -ne 0]; then
	# 	exit $retVal
	# fi

done


