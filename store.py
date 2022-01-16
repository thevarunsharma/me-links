from pickle import dump, load
from typing import List, Tuple

class DatabaseHandler:

    def __init__(self,
                 dbname: str):
        self.dbname = dbname
        
    def set(self,
            key: str,
            link: str,
            has_query: bool = False):
        """Sets key's value as link in the database"""
        
        with open(self.dbname, "rb") as fh:
            data = load(fh)

        data[key] = [link, has_query]

        with open(self.dbname, "wb") as fh:
            dump(data, fh)
    
    def has_key(self,
               key: str) -> bool:
        with open(self.dbname, "rb") as fh:
            data = load(fh)
        return key in data

    def get(self,
            key: str) -> Tuple[str, bool]:
        """Get value for key from the database"""
        
        with open(self.dbname, "rb") as fh:
            data = load(fh)
            value, has_query = data.get(key, [None, False])
        return value, has_query
    
    def match(self,
              keyword: str) -> List[str]:
        """Return a list of go-links matching keyword"""
        with open(self.dbname, "rb") as fh:
            data = load(fh)
            matches = [[key, data[key]] for key in data.keys() if keyword in key.lower()]
        matches.sort(key=lambda i: (
            not i[0].lower().startswith(keyword), i[0]
        ))
        return matches

    def pop(self,
            key: str):
        """Pops key from database"""
        with open(self.dbname, "rb") as fh:
            data = load(fh)
        data.pop(key)
        with open(self.dbname, "wb") as fh:
            dump(data, fh)
