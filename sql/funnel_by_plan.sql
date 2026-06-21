SELECT u.plan, e.evenT, COUNT(DISTINCT u.user_id) AS users
FROM users u JOIN events e ON u.user_id = e.user_id
GROUP BY u.plan, e.event
ORDER BY u.plan
