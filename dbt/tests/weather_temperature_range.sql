SELECT *
FROM {{ ref('fct_city_daily') }}
WHERE temperature_2m_min > temperature_2m_max
   OR temperature_2m_mean < temperature_2m_min
   OR temperature_2m_mean > temperature_2m_max