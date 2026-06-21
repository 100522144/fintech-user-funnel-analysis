--DEPOSITO MEDIO POR PLAN

SELECT 
    u.plan,
    ROUND(AVG e.deposit_amount),2 AS avg_deposit
FROM users u FULL JOIN events 
ON u.user_id = e.user_id
WHERE e.event = "first_deposit"
GROUP BY u.plan
ORDER BY avg_deposit DESC;