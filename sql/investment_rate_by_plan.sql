--SUSCRIPCION CON LA MAYOR TASA DE CONVERSION A INVERSORES
SELECT 
    u.plan,
    COUNT(DISTINCT CASE
        WHEN e.event = "investment_started"
        THEN u.user_id
    END)*100.0
    /
    COUNT(u.user_id)
    AS investment_rate
    FROM users u 
    LEFT JOIN events e
        ON u.user_id = e.user_id
    GROUP BY
    ORDER BY investment_rate DESC;

