sql0="use lubm"
sql1="go from \"<http://www.Department0.University0.edu/FullProfessor0>\" over_infer \"dataset\""
sql2="go from \"<http://www.Department0.University0.edu/GraduateCourse0>\" over_infer \"dataset\" REVERSELY"
sql3="go from \"<http://www.Department0.University0.edu/FullProfessor0>\" over_infer \"dataset\" type \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#Course>\""
sql4="go from \"<http://www.Department0.University0.edu/GraduateCourse0>\" over_infer \"dataset\" REVERSELY type \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#GraduateStudent>\""
sql5="go from \"<http://www.Department15.University3.edu/GraduateStudent15>\" over_infer \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#takesCourse>\""
sql6="go from \"<http://www.Department0.University0.edu/GraduateCourse0>\" over_infer \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#takesCourse>\" REVERSELY"
sql7="go from \"<http://www.Department15.University3.edu/GraduateStudent15>\" over_infer \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#takesCourse>\" type \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#Course>\""
sql8="go from \"<http://www.Department0.University0.edu/GraduateCourse0>\" over_infer \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#takesCourse>\" REVERSELY type \"<http://swat.cse.lehigh.edu/onto/univ-bench.owl#GraduateStudent>\""


function run_main() {
    num=${1}
    rm -rf log/lubm${num}
    mkdir -p log/lubm${num}
    ./main.sh ${num}
    sqls="${sql0}${num}\n${sql0}${num}\n${sql1}\n${sql1}\n${sql2}\n${sql3}\n${sql4}\n${sql5}\n${sql6}\n${sql7}\n${sql8}"
    echo -e ${sqls} | nebula-console.sh > log/lubm${num}/query.txt
    cp -r ../encode log/lubm${num}
    cp -r ../data/ log/lubm${num}
}


function main() {
    run_main 1
    run_main 2
    run_main 3
    run_main 4
    run_main 5
    run_main 10
    run_main 20
    run_main 30
    run_main 40
    run_main 50
}


function run_query() {
    num=${1}
    cp log/lubm${num}/encode/* /usr/local/nebula/data/encode/
    sleep 1
    sqls="${sql0}${num}\n${sql0}${num}\n${sql1}\n${sql1}\n${sql2}\n${sql3}\n${sql4}\n${sql5}\n${sql6}\n${sql7}\n${sql8}"
    echo -e ${sqls} | nebula-console.sh > log/lubm${num}/query.txt
}

function query() {
    run_query 1
    run_query 2
    run_query 3
    run_query 4
    run_query 5
    run_query 10
    run_query 20
    run_query 30
    run_query 40
    run_query 50
}

# main
query
