--Paises con sus respectivos usuarios
SELECT country, COUNT(*) AS usuarios
FROM users
GROUP BY country
ORDER BY usuarios DESC
