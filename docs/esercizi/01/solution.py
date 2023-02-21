from pandas import DataFrame, read_csv
from typing import List

class Reader():
    def load(self, path: str) -> DataFrame:
        data = read_csv(path, keep_default_na=False, dtype="string")
        return data

class Storer():
    def store(self, data: DataFrame, path: str) -> None:
        data.to_csv(path)

class Identifier():
    def __init__(self):
        self.identifier_scheme = None
        self.literal_value = None

    def create_doi(self, literal_value: str) -> None:
        self.identifier_scheme = 'doi'
        self.literal_value = literal_value

    def create_meta(self, literal_value: str) -> None:
        self.identifier_scheme = 'meta'
        self.literal_value = literal_value
    
    def full_ids_as_string(self) -> str:
        output = ''
        if self.identifier_scheme and self.literal_value:
            output = self.identifier_scheme + ':' + self.literal_value
        return output

class ResponsibleAgent():
    def __init__(self):
        self.family_name = None
        self.given_name = None
        self.name = None

    def has_given_name(self, given_name: str):
        self.given_name = given_name
    
    def has_family_name(self, family_name: str):
        self.family_name = family_name
    
    def has_name(self, name: str):
        self.name = name

    def get_full_name(self) -> str:
        if self.family_name and self.given_name:
            return f'{self.family_name}, {self.given_name}'
        elif self.family_name and not self.given_name:
            return f'{self.family_name},'
        elif not self.family_name and self.given_name:
            return f',{self.given_name}'
        elif not self.family_name and not self.given_name and self.name:
            return self.name

class BibliographicEntity():
    def __init__(self):
        self.identifiers = list()

    def get_identifiers(self) -> list:
        identifiers = []
        for identifier in self.identifiers:
            identifiers.append(identifier.full_ids_as_string())
        return ' '.join(identifiers)

    def has_identifiers(self, identifiers: list) -> None:
        for identifier_string in identifiers:
            id_elements = identifier_string.split(':')
            id_scheme = id_elements[0]
            id_literal_value = id_elements[1]
            identifier = Identifier()
            if id_scheme == 'doi':
                identifier.create_doi(id_literal_value)
            elif id_scheme == 'meta':
                identifier.create_meta(id_literal_value)
            self.identifiers.append(identifier)

class BibliographicResource(BibliographicEntity):
    def __init__(self):
        super().__init__()
        self.title = None
        self.venue = None
        self.authors = list()
    
    def get_title(self):
        return self.title
    
    def has_title(self, title: str):
        self.title = title
    
    def get_is_part_of(self):
        return self.venue
        
    def is_part_of(self, res: BibliographicEntity):
        self.venue = res
    
    def has_author(self, author: ResponsibleAgent):
        self.authors.append(author)
    
    def get_authors(self):
        return self.authors

class Library():
    def __init__(self):
        self.bibliographic_resources: List[BibliographicResource] = list()

    def add_bibliographic_resources(self, data: DataFrame = None, source: str = None) -> None:
        if data is None and source is None:
            return
        if source:
            reader = Reader()
            data = reader.load(source)
        for _, row in data.iterrows():
            br = BibliographicResource()
            venue = BibliographicResource()
            identifiers = row['id'].split()
            title = row['title']
            venue_name = row['venue_name']
            venue_ids = row['venue_ids'].split()
            for author in row['author'].split('; '):
                ra = ResponsibleAgent()
                family_given = author.split(',')
                if len(family_given) == 2:
                    ra.has_family_name(family_given[0].strip())
                    ra.has_given_name(family_given[1].strip())
                else:
                    ra.has_name(family_given[0])
                br.has_author(ra)
            if identifiers:
                br.has_identifiers(identifiers)
            br.has_title(title)
            if venue_ids:
                venue.has_identifiers(venue_ids)            
            venue.has_title(venue_name)
            br.is_part_of(venue)
            self.bibliographic_resources.append(br)
        
    def save_on_file(self, path: str):
        data = list()
        for br in self.bibliographic_resources:
            row = dict()
            ids = br.get_identifiers()
            title = br.get_title()
            venue = br.get_is_part_of()
            venue_title = venue.get_title()
            venue_ids = venue.get_identifiers()
            authors = br.get_authors()
            author_names = []
            for author in authors:
                author_names.append(author.get_full_name())
            row['id'] = ids
            row['title'] = title
            row['venue_name'] = venue_title
            row['venue_ids'] = venue_ids
            row['author'] = '; '.join(author_names)
            data.append(row)
        reader = Storer()
        reader.store(DataFrame(data), path)