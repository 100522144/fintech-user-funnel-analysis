SELECT u.acquisition_cahnnel, ROUND(SUM(e.deposit_amount),2) AS total_deposit
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.events ="first_deposit"
GROUP BY u.acqquisition_channel
ORDER BY total_deposit DESC; 