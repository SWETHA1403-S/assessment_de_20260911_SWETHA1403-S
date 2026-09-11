SELECT
    city,
    weather_date,
    latitude,
    longitude,
    temperature_2m_max,
    temperature_2m_min,
    temperature_2m_mean,
    precipitation_sum,
    wind_speed_10m_max
FROM {{ ref('stg_weather') }}