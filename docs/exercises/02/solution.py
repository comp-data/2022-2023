from sqlite3 import connect

from pandas import Series, read_csv

biblio_res = read_csv("docs/exercises/02/data.csv", 
                  keep_default_na=False,
                  dtype={
                      "id": "string",
                      "title": "string",
                      "type": "string"
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