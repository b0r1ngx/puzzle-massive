from flask import current_app, request, abort, json, make_response
from flask.views import MethodView
import redis
import time

from api.app import db
from api.user import user_id_from_ip, user_not_banned
from api.database import fetch_query_string, rowify

encoder = json.JSONEncoder(indent=2, sort_keys=True)

redisConnection = redis.from_url('redis://localhost:6379/0/', decode_responses=True)

DAY = 24 * 60 * 60
ACTIVE_RANGE = 14 * DAY

class PlayerRanksView(MethodView):
    """
    """

    decorators = [user_not_banned]

    def get(self):
        ""
        ip = request.headers.get('X-Real-IP')
        user = current_app.secure_cookie.get(u'user') or user_id_from_ip(ip)
        if user != None:
            user = int(user)
        args = {}
        if request.args:
            args.update(request.args.to_dict(flat=True))
        start = args.get('start')
        count = args.get('count')
        if count == None:
            return make_response(encoder.encode({
                'msg': "missing count param"
            }), 400)

        count = int(count)
        if count > 45:
            return make_response(encoder.encode({
                'msg': "Count arg is too high"
            }), 400)


        cur = db.cursor()
        now = int(time.time())
        total_players = redisConnection.zcard('rank')
        player_rank = redisConnection.zrevrank('rank', user)
        if player_rank == None:
            player_rank = total_players - 1
        player_rank = player_rank + 1
        active_players = frozenset(map(int, redisConnection.zrevrangebyscore('timeline', '+inf', now - ACTIVE_RANGE)))

        if start == None:
            start = max(0, player_rank - int(count / 2))
        else:
            start = int(start)
        stop = start + count
        rank_slice = redisConnection.zrevrange('rank', start, stop, withscores=True)

        ranks = []
        for index, item in enumerate(rank_slice):
            (user, score) = map(int, item)
            ranks.append({
                "id": user,
                "score": score,
                "rank": start + index,
                "active": user in active_players,
            })

        player_ranks = {
            "total_players": total_players,
            "total_active_players": len(active_players),
            "player_rank": player_rank,
            "rank_slice": ranks,
        }

        cur.close()
        return encoder.encode(player_ranks)

class PuzzleStatsView(MethodView):
    """
    Return statistics on a puzzle.
    """

    decorators = [user_not_banned]

    def get(self, puzzle_id):
        ""
        cur = db.cursor()
        result = cur.execute(fetch_query_string('_select-puzzle-by-puzzle_id.sql'), {
            'puzzle_id': puzzle_id
            }).fetchall()
        if not result:
            # 404 if puzzle does not exist
            abort(404)

        (result, col_names) = rowify(result, cur.description)
        puzzle = result[0].get('id')
        now = int(time.time())

        timeline = redisConnection.zrevrange('timeline:{puzzle}'.format(puzzle=puzzle), 0, -1, withscores=True)
        score_puzzle = redisConnection.zrange('score:{puzzle}'.format(puzzle=puzzle), 0, -1, withscores=True)
        user_score = dict(score_puzzle)
        user_rank = {}
        for index, item in enumerate(score_puzzle):
            user_rank[int(item[0])] = index + 1

        players = []
        for index, item in enumerate(timeline):
            (user, timestamp) = item
            players.append({
                "id": int(user),
                "score": int(user_score.get(user, 0)),
                "rank": user_rank.get(int(user), 0), # a 0 value means the player hasn't joined any pieces
                "seconds_from_now": int(now - timestamp),
            })

        puzzle_stats = {
            "now": now,
            "players": players
        }

        cur.close()
        return encoder.encode(puzzle_stats)

class PuzzleActiveCountView(MethodView):
    """
    Return active player count on a puzzle.
    """

    decorators = [user_not_banned]

    def get(self, puzzle_id):
        ""
        ip = request.headers.get('X-Real-IP')
        user = int(current_app.secure_cookie.get(u'user') or user_id_from_ip(ip))
        cur = db.cursor()
        result = cur.execute(fetch_query_string('select_viewable_puzzle_id.sql'), {
            'puzzle_id': puzzle_id
            }).fetchall()
        if not result:
            # 404 if puzzle does not exist
            abort(404)

        (result, col_names) = rowify(result, cur.description)
        puzzle = result[0].get('puzzle')
        status = result[0].get('status')
        now = int(time.time())

        count = redisConnection.zcount('timeline:{puzzle}'.format(puzzle=puzzle), now - 5*60, "+inf") or 0

        player_active_count = {
            "now": now,
            "count": count
        }

        cur.close()
        return json.jsonify(player_active_count)
