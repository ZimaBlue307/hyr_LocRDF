import argparse


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', type=int, default=1)
    args = parser.parse_args()
    return args

from SPARQLWrapper import SPARQLWrapper, JSON


params = get_params()

sparql = SPARQLWrapper("http://localhost:3030/kg_demo_hudong/query")

prefix = """
PREFIX lu: <http://www.ontologydesignpatterns.org/ont/framenet/abox/lu/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ub: <http://swat.cse.lehigh.edu/onto/univ-bench.owl#>
"""

sqls = [
    """
    SELECT *
    WHERE
    {
        <http://www.Department0.University0.edu/FullProfessor0> ?p ?o
    }
    """, """
    SELECT *
    WHERE
    {
        ?s ?p <http://www.Department0.University0.edu/GraduateCourse0>
    }
    """, """
    SELECT *
    WHERE
    {
        ?o rdf:type ub:Course .
        <http://www.Department0.University0.edu/FullProfessor0> ?p ?o
    }""", """
    SELECT *
    WHERE
    {
        ?s rdf:type ub:GraduateStudent .
        ?s ?p <http://www.Department0.University0.edu/GraduateCourse0>
    }""", """
    SELECT *
    WHERE
    {
        <http://www.Department15.University3.edu/GraduateStudent15> ub:takesCourse ?o
    }""", """
    SELECT *
    WHERE
    {
        ?s ub:takesCourse <http://www.Department0.University0.edu/GraduateCourse0>
    }""", """
    SELECT *
    WHERE
    {
        ?o rdf:type ub:Course .
        <http://www.Department15.University3.edu/GraduateStudent15> ub:takesCourse ?o
    }""", """
    SELECT *
    WHERE
    {
        ?s rdf:type ub:GraduateStudent .
        ?s ub:takesCourse <http://www.Department0.University0.edu/GraduateCourse0>
    }"""
]


sparql.setQuery(prefix + sqls[params.q])

sparql.setReturnFormat(JSON)
import time
start = time.time()
results = sparql.query()
end = time.time()
print(end - start)
results_dict = results.convert()

for result in results_dict["results"]["bindings"]:
    print(result)
