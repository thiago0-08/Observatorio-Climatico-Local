-- 1. Qual foi a maior temperatura máxima e em qual data ocorreu?
SELECT data, temperatura_maxima_c
FROM clima_diario
WHERE temperatura_maxima_c = (
    SELECT MAX(temperatura_maxima_c) FROM clima_diario
)
ORDER BY data;

-- 2. Quais foram os cinco dias com maior precipitação?
SELECT data, precipitacao_mm
FROM clima_diario
WHERE precipitacao_mm IS NOT NULL
ORDER BY precipitacao_mm DESC, data
LIMIT 5;

-- 3. Resumo do período: médias de temperatura e precipitação acumulada.
SELECT
    ROUND(AVG(temperatura_minima_c), 1) AS media_temperatura_minima_c,
    ROUND(AVG(temperatura_maxima_c), 1) AS media_temperatura_maxima_c,
    ROUND(SUM(precipitacao_mm), 1) AS precipitacao_acumulada_mm,
    ROUND(AVG(precipitacao_mm), 1) AS media_precipitacao_diaria_mm
FROM clima_diario;

-- KPI adicional: amplitude média diária entre máxima e mínima.
SELECT
    ROUND(AVG(temperatura_maxima_c - temperatura_minima_c), 1)
        AS amplitude_media_diaria_c
FROM clima_diario
WHERE temperatura_maxima_c IS NOT NULL
  AND temperatura_minima_c IS NOT NULL;
