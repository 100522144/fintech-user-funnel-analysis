-- ==========================================================
-- Users by Plan
-- Count the number of users subscribed to each plan.
-- ==========================================================

SELECT plan, COUNT (*) AS users
FROM users
GROUP BY plan
ORDER BY users DESC;

-- ==========================================================
-- Average Deposit by Plan
-- Calculate the average first deposit amount.
-- ==========================================================

SELECT u.plan, ROUND(AVG(e.deposit_amount),2) AS average_deposit
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP by u.plan 
ORDER BY average_deposit DESC;

-- ==========================================================
-- Total Deposit Volume by Plan
-- Sum all deposits for each plan.
-- ==========================================================

SELECT u.plan, ROUND(SUM(e.deposit_amount),2) AS total_deposit_volume
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP BY u.plan 
ORDER BY total_deposit_volume DESC;

-- ==========================================================
-- Investment Rate by Plan
-- Percentage of users who started investing.
-- ==========================================================

SELECT u.plan, ROUND(COUNT(DISTINCT CASE
                            WHEN e.event = 'investment_started'
                            THEN u.user_id
                    END)*100.0/
                    COUNT(DISTINCT u.user_id),2) AS investment_rate
FROM users u LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY plan 
ORDER BY investment_rate DESC;

-- ==========================================================
-- Active Users by Plan
-- Number of users who opened the app.
-- ==========================================================

SELECT u.plan, COUNT(DISTINCT e.user_id) AS active_users
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'app_opened'
GROUP BY u.plan 
ORDER BY active_users DESC;

-- ==========================================================
-- App Sessions by Plan
-- Total number of app_opened events.
-- ==========================================================

SELECT u.plan, COUNT(*) AS sessions
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'app_opened'
GROUP BY u.PLAN
ORDER BY sessions DESC;

-- ==========================================================
-- Average Sessions per User
-- Average number of app sessions for each plan.
-- ==========================================================

SELECT u.plan, ROUND(COUNT(*)*1.0/COUNT(DISTINCT u.user_id),2) AS average_sessions
FROM users u JOIN events e ON u.user_id = e.user_id 
WHERE e.event = 'app_opened'
GROUP BY u.plan 
ORDER BY average_sessions DESC;

-- ==========================================================
-- Card Orders by Plan
-- Number of users who ordered a card.
-- ==========================================================

SELECT u.plan, COUNT(DISTINCT e.user_id) AS card_orders
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'card_ordered'
GROUP BY u.plan  
ORDER BY card_orders DESC;