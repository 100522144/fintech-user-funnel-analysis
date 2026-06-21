SELECT event, COUNT(DISTINCT user_id) AS usuarios
FROM events
GROUP BY event
ORDER BY usuarios DESC; 