import re
from typing import Tuple

class PathParser:
    
    def __init__(self):
        self.__pattern = re.compile(r"^(.*?)\s+(.*)$")
    
    def parse(self,
              path: str) -> Tuple[str, str]:
        """Parse a path and return keyword and query arguments"""
        match = self.__pattern.search(path)
        if match is None:
            return path, ""
        return match[1], match[2]
        
    def is_valid(self,
                 key: str):
        """Checks if the proposed key is a valid one"""
        match = self.__pattern.search(key)
        # key shouldn't have any spaces
        return match is None
    