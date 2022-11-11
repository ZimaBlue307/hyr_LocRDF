if [ $# -eq 1 ];
then
    echo "num: $1"
else
	echo "错误"
    exit
fi


mkdir -p log/lubm${1}
python query.py --q 0 > log/lubm${1}/query0.txt
python query.py --q 0 > log/lubm${1}/query1.txt
python query.py --q 1 > log/lubm${1}/query2.txt
python query.py --q 2 > log/lubm${1}/query3.txt
python query.py --q 3 > log/lubm${1}/query4.txt
python query.py --q 4 > log/lubm${1}/query5.txt
python query.py --q 5 > log/lubm${1}/query6.txt
python query.py --q 6 > log/lubm${1}/query7.txt
python query.py --q 7 > log/lubm${1}/query8.txt
