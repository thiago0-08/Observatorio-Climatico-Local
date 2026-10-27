# Observatório Climático Local — Marília-SP

## Objetivo
Analisar dados meteorológicos históricos de Marília-SP para produzir informações úteis a entregadores que trabalham ao ar livre, com atenção às variações de temperatura e à precipitação.

## Público-alvo
Profissionais que realizam entregas nas ruas.

## Fonte e variáveis
- Fonte: API histórica Open-Meteo (`https://archive-api.open-meteo.com/v1/archive`).
- Coordenadas usadas: latitude `-22.2171`, longitude `-49.9501` 
- Fuso horário: `America/Sao_Paulo`.
- Período: os 30 dias completos anteriores à execução de `coleta.py`.
- Variáveis: temperatura mínima diária (°C), temperatura máxima diária (°C) e precipitação acumulada diária (mm).

Os valores são dados históricos disponibilizados pela Open-Meteo e não devem ser descritos como medições diretas de uma estação meteorológica específica de Marília sem confirmação da origem.

## Arquivos
- `coleta.py`: consulta a API e salva a resposta JSON original.
- `banco.py`: trata, valida e carrega os dados em DuckDB.
- `consultas.sql`: consultas analíticas.
- `requirements.txt`: bibliotecas Python.
- `dados/`: arquivos gerados durante a execução.
- `docs/escopo-1/AE2/`: local sugerido para o relatório.

## Preparação e execução
Requer Python 3.10 ou superior.

## rode um por vez para o instalar e rodar o projeto 

``` entre no terminal 
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python coleta.py
python banco.py
```

Execute `coleta.py` antes de `banco.py`. O script de coleta gera `dados/resposta_original.json`; o script de tratamento gera `dados/dados_tratados.csv` e `dados/observatorio.duckdb`.

## Indicadores (KPIs)
1. Maior temperatura máxima diária do período e data correspondente.
2. Dias com maior precipitação acumulada.
3. Precipitação acumulada no período e amplitude média diária de temperatura.

## Limitações e cuidados
- Os dados descrevem condições meteorológicas históricas e não são previsão do tempo.
- A resolução espacial e a metodologia da fonte podem não representar exatamente as condições de cada rua ou bairro.
- Chuva e temperatura podem influenciar o planejamento de entregas, mas os dados não medem diretamente acidentes, renda, demanda ou produtividade dos entregadores.
- Não são coletados nomes, localização individual ou dados pessoais de entregadores.
- Registre no relatório a data real da coleta e os resultados observados após executar os scripts.

## Consultas
Abra `consultas.sql` e execute as consultas em um cliente DuckDB ou adapte-as para executar via Python. As consultas requer que `banco.py` já foi criado.
