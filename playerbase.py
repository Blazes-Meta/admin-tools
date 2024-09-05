import os

class Playerbase
    def __init__(self, database_path: str):
        self.database_path = database_path
        if not os.pathexists(self.database_path)
            