-- should match results from select_available_puzzle_images.sql

select count(*) as puzzle_count from (
    select
p.m_date is not null and strftime('%s', p.m_date) >= strftime('%s', 'now', '-7 hours') as is_recent,
p.m_date is not null and not strftime('%s', p.m_date) >= strftime('%s', 'now', '-7 hours') and p.status in (1, 2) as is_active,
p.m_date is null and p.status in (1, 2) as is_new, -- ACTIVE, IN_QUEUE
pi.original == pi.instance as is_original

from Puzzle as p
join PuzzleInstance as pi on (pi.instance = p.id)
join Puzzle as p1 on (pi.original = p1.id)
join PuzzleFile as pf on (p1.id = pf.puzzle)

where pf.name == 'preview_full'
and p.permission = 0 -- PUBLIC
and is_recent in {recent_status}
and is_active in {active_status}
and is_new in {new_status}
and is_original in {original_type}
and p.status in {status}
and p.pieces >= :pieces_min
and p.pieces <= :pieces_max
) as puzzle_list
;