from sqlalchemy import create_engine
from model import Base


DB_PATH = './testdb.db'
engine = create_engine('sqlite:///' + DB_PATH)
Base.metadata.create_all(engine)

