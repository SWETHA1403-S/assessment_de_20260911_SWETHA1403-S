SELECT
    city,
    latitude::double precision AS latitude,
    longitude::double precision AS longitude,
    weather_date::date AS weather_date,
    temperature_2m_max::double precision AS temperature_2m_max,
    temperature_2m_min::double precision AS temperature_2m_min,
    temperature_2m_mean::double precision AS temperature_2m_mean,
    precipitation_sum::double precision AS precipitation_sum,
    wind_speed_10m_max::double precision AS wind_speed_10m_max
FROM {{ source('raw', 'weather_daily') }}
WHERE city IS NOT NULL
  AND weather_date IS NOT NULL