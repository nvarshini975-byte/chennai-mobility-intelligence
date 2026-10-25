
SELECT
    s.stop_id,
    s.stop_name,
    ROUND(s.stop_lat::NUMERIC, 5) AS latitude,
    ROUND(s.stop_lon::NUMERIC, 5) AS longitude,
    COUNT(*) AS scheduled_stop_occurrences,
    COUNT(DISTINCT f.trip_id) AS distinct_trips
FROM warehouse.fact_stop_times f
JOIN warehouse.dim_stops s
    ON f.stop_id = s.stop_id
GROUP BY
    s.stop_id,
    s.stop_name,
    s.stop_lat,
    s.stop_lon
ORDER BY scheduled_stop_occurrences DESC
LIMIT 15;
