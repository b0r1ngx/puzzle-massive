SELECT u.login, b.name AS icon, u.score, u.points as dots, u.id, u.cookie_expires,
strftime('%s', u.cookie_expires) <= strftime('%s', 'now', '+351 days') as will_expire_cookie,
strftime('%s', b.expiration) <= strftime('%s', 'now') as bit_expired,
(select count(*) from User_Puzzle where player = :id) as user_puzzle_count
FROM User AS u
LEFT OUTER JOIN BitIcon AS b ON u.id = b.user
WHERE u.id = :id;