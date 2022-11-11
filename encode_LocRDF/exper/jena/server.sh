if [ $# -eq 1 ];
then
    echo "num: $1"
else
	echo "错误"
    exit
fi


function create_nt() {
    cd ../..

    cd data/uba1.7
    echo ". run.sh ${1};"
    . run.sh ${1} > /dev/null
    cd ../..

    cd src/util/format
    echo "python change.py"
    python change.py
}


function log_nt() {
    rm -rf ../../data
    cp -r ../log/lubm${1}/data ../../data
}


# create_nt ${1}
log_nt ${1}


cd ~/cr/nebula/apache-jena/apache-jena-4.4.0/bin
. insert.sh


cd ~/cr/nebula/apache-jena/apache-jena-fuseki-4.4.0
./fuseki-server
