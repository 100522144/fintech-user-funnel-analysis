SELECT 
    u.acquisition_chanel,
    COUNT(DISTINCT CASE
        WHEN e.events = "investment_started"
        THEN u.user_id
    END)100*0

    /

    COUNT(DISTINCT u.user_id)
    AS investment_rate

    FROM users u LEFT JOIN events e
ON u.user_id = e.user_id
ORDER BY investment_rate DESC;