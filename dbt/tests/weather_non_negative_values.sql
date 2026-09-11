SELECT *
FROM {{ ref('fct_city_daily') }}
WHERE precipitation_sum < 0
   OR wind_speed_10m_max < 02