import sqlite3

class DatabaseManager():
  conn = None
  def __init__(self, path):
    self.conn = sqlite3.connect(path)
    c = self.conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tokens (name TEXT, token TEXT)')
    self.conn.commit()

  def get_token(self, name):
    c = self.conn.cursor()
    c.execute("SELECT token FROM tokens WHERE name=?", (name,));
    return c.fetchone()[0]

  def set_token(self, name, tok):
    c = self.conn.cursor()
    c.execute("INSERT INTO tokens VALUES (?,?)", (name, tok));
    self.conn.commit()

db = DatabaseManager("csb.db")
