SELECT 
    country, ocupation, plan, COUNT(*) AS investors
FROM users u JOIN events e 
    ON u.user_id = e.user_id
WHERE e.event = "investment_started"
GROUP BY country, occupation, plan
ORDER BY investors DESC;

