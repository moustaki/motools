rapper -i turtle -e -o rdfxml ../rdf/temperament.n3 > ../rdf/temperament.owl
python specgen.py ../rdf/temperament.owl tm template.html temperament.html -i