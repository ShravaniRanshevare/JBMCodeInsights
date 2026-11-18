from sqlalchemy import create_engine,event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_alchemy_url = "sqlite:///./jbm-codeinsights"
engine = create_engine(sql_alchemy_url,connect_args={'check_same_thread':False})

@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(
    dbapi_connection,
    connection_record
):
    cursor = dbapi_connection.cursor()
    cursor.execute(
        "PRAGMA foreign_keys=ON"
    )
    cursor.close()
    
SessionLocal = sessionmaker(autocommit=False,autoflush=True,bind=engine)
Base = declarative_base()

