from app.db.session import engine
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    print("🔍 Tablas encontradas en test.db:")
    for row in result:
        print(f"- {row[0]}")
