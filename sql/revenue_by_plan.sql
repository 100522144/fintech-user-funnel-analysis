SELECT u.plan, ROUND(SUM(e.deposit_amount), 2) AS total_deposit
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = "first_deposit"
GROUP BY u.plan
ORDER BY total_deposit DESC;
