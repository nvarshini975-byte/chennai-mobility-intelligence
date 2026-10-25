
SELECT
    r.route_id,
    r.route_short_name,
    r.route_long_name,
    COUNT(t.trip_id) AS total_scheduled_trips
FROM warehouse.dim_routes r
JOIN warehouse.dim_trips t
    ON r.route_id = t.route_id
WHERE r.route_type = 3
GROUP BY
    r.route_id,
    r.route_short_name,
    r.route_long_name
ORDER BY total_scheduled_trips DESC
LIMIT 15;
