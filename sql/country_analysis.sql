-- ==========================================================
-- Users by Country
-- Count the number of registered users in each country.
-- ==========================================================

SELECT country, COUNT(*) AS users
FROM users
GROUP BY country
ORDER BY users DESC;


-- ==========================================================
-- Average Deposit by Country
-- Calculate the average first deposit amount for each country.
-- ==========================================================

SELECT u.country, ROUND(AVG(e.deposit_amount),2) AS average_deposit
FROM users u JOIN events e
ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP BY u.country
ORDER BY average_deposit DESC;

-- ==========================================================
-- Total Deposit Volume by Country
-- Sum all first deposits by country.
-- ==========================================================

SELECT u.country, ROUND(SUM(e.deposit_amount),2) AS total_deposit_volume
FROM users u JOIN events e
ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP BY u.country
ORDER BY total_deposit_volume DESC;

-- ==========================================================
-- Investment Rate by Country
-- Percentage of users who started investing.
-- ==========================================================

SELECT u.country, ROUND(
        COUNT(DISTINCT CASE 
                    WHEN e.event = 'investment_started' 
                    THEN u.user_id 
                END) *100.0/
        COUNT(DISTINCT u.user_id),2

        ) AS investment_rate
FROM users u
LEFT JOIN events e
ON u.user_id = e.user_id
GROUP BY country
ORDER BY investment_rate DESC;

-- ==========================================================
-- Active Users by Country
-- Number of users who opened the app at least once.
-- ==========================================================

SELECT u.country, COUNT(DISTINCT e.user_id) AS active_users
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'app_opened'
GROUP BY u.country
ORDER BY active_users DESC;

-- ==========================================================
-- App Sessions by Country
-- Total number of app_opened events.
-- ==========================================================

SELECT u.country, COUNT(*) AS sessions
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'app_opened'
GROUP BY u.country
ORDER BY sessions DESC; 