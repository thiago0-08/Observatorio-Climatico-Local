# Trata os dados meteorológicos e carrega uma tabela no DuckDB.
import json
from pathlib import Path
import duckdb
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
ARQUIVO_JSON = DADOS_DIR / "resposta_original.json"
ARQUIVO_CSV = DADOS_DIR / "dados_tratados.csv"
ARQUIVO_BANCO = DADOS_DIR / "observatorio.duckdb"

COLUNAS = {
    "time": "data",
    "temperature_2m_min": "temperatura_minima_c",
    "temperature_2m_max": "temperatura_maxima_c",
    "precipitation_sum": "precipitacao_mm",
}

def main():
    if not ARQUIVO_JSON.exists():
        raise FileNotFoundError("Arquivo dados/resposta_original.json não encontrado. Execute primeiro: python coleta.py")

    bruto = json.loads(ARQUIVO_JSON.read_text(encoding="utf-8"))
    daily = bruto.get("daily", {})
    df = pd.DataFrame(daily).rename(columns=COLUNAS)

    obrigatorias = list(COLUNAS.values())
    faltantes = [c for c in obrigatorias if c not in df.columns]
    if faltantes:
        raise ValueError(f"Campos ausentes na resposta: {faltantes}")

    df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
    for coluna in ["temperatura_minima_c", "temperatura_maxima_c", "precipitacao_mm"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    linhas_iniciais = len(df)
    df = df.dropna(subset=["data"])
    duplicadas = int(df.duplicated(subset=["data"]).sum())
    df = df.drop_duplicates(subset=["data"], keep="last")

    # Valores ausentes são mantidos como NULL/NaN; não são transformados em zero.
    df = df.sort_values("data").reset_index(drop=True)

    invalidas = (
        (df["temperatura_minima_c"].notna() &
         df["temperatura_maxima_c"].notna() &
         (df["temperatura_minima_c"] > df["temperatura_maxima_c"]))
    )
    qtd_invalidas = int(invalidas.sum())
    if qtd_invalidas:
        raise ValueError(f"Foram encontradas {qtd_invalidas} linhas com mínima maior que máxima. Verifique os dados antes de carregar.")

    df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8")
    print("Validação dos dados")
    print(f"- Linhas recebidas: {linhas_iniciais}")
    print(f"- Datas duplicadas removidas: {duplicadas}")
    print(f"- Registros válidos após tratamento: {len(df)}")
    print(f"- Datas cobertas: {df['data'].min()} a {df['data'].max()}")
    print(f"- Valores ausentes por coluna: {df.isna().sum().to_dict()}")

    con = duckdb.connect(str(ARQUIVO_BANCO))
    try:
        con.execute("""
            CREATE TABLE IF NOT EXISTS clima_diario (
                data DATE PRIMARY KEY,
                temperatura_minima_c DOUBLE,
                temperatura_maxima_c DOUBLE,
                precipitacao_mm DOUBLE
            )
        """)
    # ele refaz o processo de busca para nao duplicar os dados, e substitiu pela pesquisa mais recente 
        
        con.register("df_lote", df)
        con.execute("DELETE FROM clima_diario WHERE data IN (SELECT data FROM df_lote)")
        con.execute("""
            INSERT INTO clima_diario
            SELECT data, temperatura_minima_c, temperatura_maxima_c, precipitacao_mm
            FROM df_lote
        """)
        total = con.execute("SELECT COUNT(*) FROM clima_diario").fetchone()[0]
        print(f"Banco atualizado: {ARQUIVO_BANCO}")
        print(f"Total de registros na tabela clima_diario: {total}")
        print(con.execute("""
            SELECT * FROM clima_diario ORDER BY data DESC LIMIT 5
        """).df().to_string(index=False))
    finally:
        con.close()

if __name__ == "__main__":
    main()
