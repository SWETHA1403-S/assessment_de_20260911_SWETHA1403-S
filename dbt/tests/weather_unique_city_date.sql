SELECT
    city,
    weather_date,
    COUNT(*) AS row_count
FROM {{ ref('fct_city_daily') }}
GROUP BY city, weather_date
HAVING COUNT(*) > 1