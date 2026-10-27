
from pathlib import Path
import duckdb

pasta = Path(__file__).resolve().parent
banco = pasta / "dados" / "observatorio.duckdb"
arquivo_sql = pasta / "consultas.sql"

con = duckdb.connect(str(banco), read_only=True)

try:
    consultas = arquivo_sql.read_text(encoding="utf-8").split(";")

    for numero, sql in enumerate(consultas, start=1):
        if sql.strip():
            print(f"\n--- CONSULTA {numero} ---")
            resultado = con.execute(sql).df()
            print(resultado.to_string(index=False))
finally:
    con.close()
