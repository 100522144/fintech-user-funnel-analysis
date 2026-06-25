-- ==========================================================
-- Funnel Overview
-- Number of users reaching each funnel step.
-- ==========================================================

SELECT event, COUNT(DISTINCT user_id) AS users
FROM events
GROUP BY event
ORDER BY users DESC;

-- ==========================================================
-- Signup to KYC Conversion
-- Percentage of registered users who complete KYC.
-- ==========================================================

SELECT
    ROUND(
        COUNT(DISTINCT CASE
            WHEN event ='kyc_completed'
            THEN user_id
        END)*100.0/
        COUNT(DISTINCT CASE
            WHEN event = 'sign_up'
            THEN user_id
        END),2
    ) AS signup_to_kyc_conversion
FROM events;

-- ==========================================================
-- Signup to Deposit Conversion
-- Percentage of registered users who make a first deposit.
-- ==========================================================

SELECT
    ROUND(
        COUNT(DISTINCT CASE
            WHEN event ='first_deposit'
            THEN user_id
        END)*100.0/
        COUNT(DISTINCT CASE
            WHEN event = 'sign_up'
            THEN user_id
        END),2
    ) AS signup_to_deposit_conversion
FROM events;

-- ==========================================================
-- Signup to Investment Conversion
-- Percentage of users who start investing.
-- ==========================================================

SELECT
    ROUND(
        COUNT(DISTINCT CASE
            WHEN event ='investment_started'
            THEN user_id
        END)*100.0/
        COUNT(DISTINCT CASE
            WHEN event = 'sign_up'
            THEN user_id
        END),2
    ) AS signup_to_investment_conversion
FROM events;

-- ==========================================================
-- Investment Conversion by Plan
-- Percentage of users who start investing for each plan.
-- ==========================================================

SELECT u.plan,ROUND(
                COUNT(DISTINCT CASE
                    WHEN e.event ='investment_started'
                    THEN u.user_id
                END) 
                *100.0/
                COUNT(DISTINCT u.user_id),2
                ) AS investment_rate
FROM users u LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.plan 
ORDER BY investment_rate DESC;

-- ==========================================================
-- Investment Conversion by Acquisition Channel
-- ==========================================================

SELECT u.acquisition_channel,ROUND(
                COUNT(DISTINCT CASE
                    WHEN e.event ='investment_started'
                    THEN u.user_id
                END) 
                *100.0/
                COUNT(DISTINCT u.user_id),2
                ) AS investment_rate
FROM users u LEFT JOIN events e ON u.user_id = e.user_id
GROUP BY u.acquisition_channel
ORDER BY investment_rate DESC;

-- ==========================================================
-- Users Completing the Funnel
-- Users who reached the investment stage.
-- ==========================================================

SELECT COUNT(DISTINCT user_id) AS completed_funnel
FROM events
WHERE event = 'investment_started';

-- ==========================================================
-- Funnel Dropoff
-- Users who registered but never made a deposit.
-- ==========================================================

SELECT COUNT (DISTINCT user_id) AS users_whitout_deposit
FROM events
WHERE event = 'sign_up'
AND user_id NOT IN(
            SELECT user_id
            FROM events
            WHERE event = 'first_deposit'
);