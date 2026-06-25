-- ==========================================================
-- Users by Device
-- Count the number of users for each device.
-- ==========================================================

SELECT device, COUNT(*) AS users
FROM users
GROUP BY device
ORDER BY users DESC;

-- ==========================================================
-- Average Deposit by Device
-- Calculate the average first deposit amount.
-- ==========================================================

SELECT u.device, ROUND(AVG(e.deposit_amount),2) AS average_deposit
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP BY u.device
ORDER BY average_deposit DESC;

-- ==========================================================
-- Total Deposit Volume by Device
-- Calculate total deposited money.
-- ==========================================================

SELECT u.device, ROUND(SUM(e.deposit_amount),2) AS total_deposit_volume
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP BY u.device
ORDER BY total_deposit_volume DESC;

-- ==========================================================
-- Investment Rate by Device
-- Percentage of users who started investing.
-- ==========================================================

SELECT u.device, ROUND(COUNT(DISTINCT CASE
                            WHEN e.event = 'investment_started'
                            THEN u.user_id
                        END)*100.0/
                        COUNT(DISTINCT u.user_id),2
                        ) AS investment_rate
FROM users u LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.device
ORDER BY investment_rate DESC;

-- ==========================================================
-- Active Users by Device
-- Users who opened the app.
-- ==========================================================

SELECT u.device, COUNT(DISTINCT e.user_id) AS active_users
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'app_opened'
GROUP BY u.device
ORDER BY active_users DESC;

-- ==========================================================
-- App Sessions by Device
-- Total number of app sessions.
-- ==========================================================

SELECT u.device, COUNT(*) AS sessions
FROM users u JOIN events e on u.user_id = e.user_id
WHERE e.event = 'app_opened'
GROUP BY u.device
ORDER BY sessions DESC;
