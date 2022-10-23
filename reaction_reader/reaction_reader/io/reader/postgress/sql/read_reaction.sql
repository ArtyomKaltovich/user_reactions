SELECT
	COUNT(DISTINCT ur.username) n_uniqie_users,
	SUM((reaction = 'click')::int) n_clicks,
	SUM((reaction = 'impression')::int) n_impressions,
	date_trunc('hour', ur.timestamp) t
FROM user_reaction ur
GROUP BY t;
