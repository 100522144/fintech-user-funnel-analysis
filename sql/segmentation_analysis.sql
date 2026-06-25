-- ==========================================================
-- Users by Country and Occupation
-- Analyze the distribution of users across countries and occupations.
-- ==========================================================

SELECT country, occupation, COUNT (*) AS users
FROM users
GROUP BY country, occupation
ORDER BY users DESC;

-- ==========================================================
-- Users by Country and Plan
-- Analyze the distribution of subscription plans across countries.
-- ==========================================================

SELECT country, plan, COUNT (*) AS users
FROM users
GROUP BY country, plan
ORDER BY users DESC;

-- ==========================================================
-- Users by Plan and Device
-- Analyze the distribution of devices within each subscription plan.
-- ==========================================================

SELECT plan, device, COUNT (*) AS users
FROM users
GROUP BY plan, device
ORDER BY users DESC;

-- ==========================================================
-- Investment Rate by Segment
-- Identify the country and occupation segments with the highest investment rate.
-- ==========================================================

SELECT u.country, u.occupation, ROUND(
                                    COUNT(DISTINCT CASE
                                        WHEN e.event = 'investment_started'
                                        THEN u.user_id
                                    END) *100.0/

                                    COUNT(DISTINCT u.user_id),2
                                    ) AS investment_rate
FROM users u LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.country, u.occupation
ORDER BY investment_rate DESC;

-- ==========================================================
-- Average Deposit by Segment
-- Compare the average first deposit amount across country and plan segments.
-- ==========================================================

SELECT u.country, u.plan, ROUND(
                            AVG(e.deposit_amount),2
                        )AS average_deposit
FROM users u JOIN events e ON u.user_id = e.user_id
WHERE e.event = 'first_deposit'
GROUP BY u.country, u.plan 
ORDER BY average_deposit DESC;