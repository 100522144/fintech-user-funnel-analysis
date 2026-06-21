--Nmero de usuarios por tipo de dispositvo
SELECT device, COUNT(*) AS usuarios
FROM users
GROUP BY device;