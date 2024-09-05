import os
import sqlite3

class Playerbase:
    def __init__(self, database_path: str):
        self.database_path = database_path

        if not os.path.exists(self.database_path):
            self.execute('''
CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY,
    discordid TEXT NOT NULL,
    mcuuid TEXT,
    info TEXT
)
                         ''')

    def execute(self, sql: str, *args):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
        conn.close()

        return cursor.fetchone()


    def add(self, discordid: int, mcuuid: str = None):
        check = self.execute("SELECT * FROM member WHERE discordid = ?", (discordid,))

        if check:
            raise Exception(f"Es exitsiert bereits ein Eintrag mit der Discord-ID {discordid}")
        else:
            self.execute("""
INSERT INTO member (discordid, mcuuid)
VALUES (?, ?, ?)
""", (discordid, mcuuid))
            
    def get(self, discordid: int):
        result = self.execute("SELECT * FROM member WHERE discordid = ?", discordid)