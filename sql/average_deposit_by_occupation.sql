SELECT 
    u.occupatiom, ROUND(AVG(e.deposit_amount),2) AS avg_deposit
FROM users u 
JOIN events e ON u.user_id = e.events_id
WHERE e.events = "first_deposit"
GROUP BY u.occupation
ORDER BY avg_deposit DESC;