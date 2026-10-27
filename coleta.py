# Coleta dados meteorológicos históricos de Marília-SP via Open-Meteo.
from datetime import date, timedelta
import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"
DADOS_DIR.mkdir(exist_ok=True)

LATITUDE = -22.2171
LONGITUDE = -49.9501
TIMEZONE = "America/Sao_Paulo"
URL = "https://archive-api.open-meteo.com/v1/archive"

def main():
    # Usa os últimos 30 dias completos, terminando ontem.
    data_fim = date.today() - timedelta(days=1)
    data_inicio = data_fim - timedelta(days=29)

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": data_inicio.isoformat(),
        "end_date": data_fim.isoformat(),
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": TIMEZONE,
    }

    print(f"Coletando Marília-SP de {data_inicio} até {data_fim}...")
    resposta = requests.get(URL, params=params, timeout=60)
    resposta.raise_for_status()
    dados = resposta.json()

    if "daily" not in dados or not dados["daily"].get("time"):
        raise ValueError("A API não retornou dados diários para o período solicitado.")

    arquivo_json = DADOS_DIR / "resposta_original.json"
    arquivo_json.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Resposta original preservada em: {arquivo_json}")
    print(f"Registros diários recebidos: {len(dados['daily']['time'])}")
    print("Coleta concluída. Execute agora: python banco.py")

if __name__ == "__main__":
    main()
