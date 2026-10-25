
SELECT
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    CASE r.route_type
        WHEN 1 THEN 'Metro'
        WHEN 3 THEN 'Bus'
        ELSE 'Other'
    END AS transport_mode,
    COUNT(DISTINCT t.trip_id) AS total_scheduled_trips,
    COUNT(f.trip_id) AS scheduled_stop_time_records
FROM warehouse.dim_routes r
LEFT JOIN warehouse.dim_trips t
    ON r.route_id = t.route_id
LEFT JOIN warehouse.fact_stop_times f
    ON t.trip_id = f.trip_id
GROUP BY
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    r.route_type
ORDER BY total_scheduled_trips DESC;
