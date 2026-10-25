
SELECT
    CASE r.route_type
        WHEN 1 THEN 'Metro'
        WHEN 3 THEN 'Bus'
        ELSE 'Other'
    END AS transport_mode,
    COUNT(DISTINCT r.route_id) AS total_routes,
    COUNT(DISTINCT t.trip_id) AS total_trips,
    COUNT(f.trip_id) AS scheduled_stop_time_records
FROM warehouse.dim_routes r
LEFT JOIN warehouse.dim_trips t
    ON r.route_id = t.route_id
LEFT JOIN warehouse.fact_stop_times f
    ON t.trip_id = f.trip_id
GROUP BY r.route_type
ORDER BY total_routes DESC;
