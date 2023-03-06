from sqlite3 import connect

from pandas import Series, read_csv

biblio_res = read_csv("docs/exercises/02/data.csv", 
                  keep_default_na=False,
                  dtype={
                      "id": "string",
                      "title": "string",
                      "type": "string",
                      "publisher": "string"
                  })
biblio_res_internal_ids = []
for idx, row in biblio_res.iterrows():
    biblio_res_internal_ids.append("br-" + str(idx))
biblio_res.insert(0, "brId", Series(biblio_res_internal_ids, dtype="string"))

publications = read_csv("docs/exercises/02/publisher.csv", 
                        keep_default_na=False,
                        dtype={
                            "id": "string",
                            "name": "string"
                        })
publication_internal_id = []
for idx, row in publications.iterrows():
    publication_internal_id.append("publication-" + str(idx))
publications.insert(0, "internalId", Series(publication_internal_id, dtype="string"))

with connect("docs/exercises/02/database.db") as con:
    biblio_res.to_sql("BibliographicResource", con, if_exists="replace", index=False)
    publications.to_sql("Publisher", con, if_exists="replace", index=False)

query_1 = '''
SELECT title, type, publisher
FROM BibliographicResource
WHERE id='doi:10.5244/c.14.27'
'''
query_2 = '''
SELECT id, title, publisher
FROM BibliographicResource
WHERE type='book chapter'
'''
query_3 = '''
SELECT title, type, publisher, name
FROM BibliographicResource 
LEFT JOIN Publisher 
ON BibliographicResource.publisher == Publisher.id
WHERE BibliographicResource.id='doi:10.5005/jp/books/11313_5'
'''

with connect("docs/exercises/02/database.db") as con:
    cur = con.cursor()
    result_1 = cur.execute(query_1).fetchall()
    result_2 = cur.execute(query_2).fetchall()
    result_3 = cur.execute(query_3).fetchall()