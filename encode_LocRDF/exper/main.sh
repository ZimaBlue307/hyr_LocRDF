#!/bin/bash

if [ $# -eq 1 ];
then
    echo "num: $1"
else
	echo "错误"
    exit
fi

cd ..

cd data/uba1.7
echo ". run.sh ${1};"
. run.sh ${1} > /dev/null
cd ../..

cd src/util/format
echo "python change.py"
python change.py

cd ../..
echo "python main.py --dataset lubm${1}"
python main.py --dataset lubm${1}
cd ..

cd csv
sleep 1
echo "nebula-importer --config a_config.yaml"
nebula-importer --config a_config.yaml > ../exper/log/lubm${1}/insert.txt
