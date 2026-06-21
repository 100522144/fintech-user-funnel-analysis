--Numero de usuarios por plan 
SELECT plan, COUNT (*) AS usuarios
FROM users
GROUP BY plan
ORDER BY users DESC;
