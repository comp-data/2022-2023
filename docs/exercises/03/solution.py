from pandas import read_csv
from rdflib import Graph, Literal, URIRef
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

base_url = URIRef("https://comp-data.github.io/res/")
name = URIRef('https://schema.org/name')
identifier = URIRef('https://schema.org/Identifier')
br = URIRef('https://schema.org/BibliographicResource')
a = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
has_publisher = URIRef('https://schema.org/hasPublisher')

pub_id_mapping = {}
my_graph = Graph()

publications = read_csv("docs/exercises/02/publisher.csv", 
                        keep_default_na=False,
                        dtype={
                            "id": "string",
                            "name": "string"
                        })
for idx, row in publications.iterrows():
    publication_internal_id = "publication-" + str(idx)
    subj = URIRef(base_url + publication_internal_id)
    my_graph.add((subj, identifier, Literal(row["id"])))
    my_graph.add((subj, name, Literal(row["name"])))
    pub_id_mapping[row["id"]] = subj

biblio_res = read_csv("docs/exercises/03/data.csv", 
                  keep_default_na=False,
                  dtype={
                      "id": "string",
                      "title": "string",
                      "publisher": "string"
                  })
for idx, row in biblio_res.iterrows():
    local_id = "br-" + str(idx)
    subj = URIRef(base_url + local_id)
    my_graph.add((subj, a, br))
    my_graph.add((subj, name, Literal(row["title"])))
    my_graph.add((subj, identifier, Literal(row["id"])))
    my_graph.add((subj, has_publisher, pub_id_mapping[row["publisher"]]))

store = SPARQLUpdateStore()
endpoint = 'http://127.0.0.1:9999/blazegraph/sparql'
store.open((endpoint, endpoint))
for triple in my_graph.triples((None, None, None)):
   store.add(triple)
store.close()

query_1 = '''
SELECT ?res ?title ?publisher_id
WHERE {
    ?res <https://schema.org/Identifier> "doi:10.1037/e463622004-001";
        <https://schema.org/name> ?title.
}
'''
query_2 = '''
SELECT ?res ?title ?publisher_id ?publisher_name
WHERE {
    ?res <https://schema.org/Identifier> "doi:10.1109/cyberneticscom.2012.6381631";
        <https://schema.org/name> ?title;
        <https://schema.org/hasPublisher> ?pub_res.
    ?pub_res <https://schema.org/Identifier> ?publisher_id;
            <https://schema.org/name> ?publisher_name.
}
'''
store.open((endpoint, endpoint))
result_1 = store.query(query=query_1)
result_2 = store.query(query=query_2)
store.close()
print(result_1.serialize().decode('utf8'), '\n', result_2.serialize().decode('utf8'))