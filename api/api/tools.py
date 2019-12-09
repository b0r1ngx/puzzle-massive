from __future__ import division
from past.utils import old_div
import os
import re
import logging

from flask import Config

INITIAL_KARMA = 10
HOUR = 3600  # hour in seconds

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def loadConfig(argconfig):
    "Load the config file the same way Flask does which Chill uses."
    config_file = (
        argconfig if argconfig[0] == os.sep else os.path.join(os.getcwd(), argconfig)
    )
    config = Config(os.getcwd())
    config.from_pyfile(config_file)
    return config


def formatPieceMovementString(piece_id, x="", y="", r="", g="", s="", **args):
    if s == None:
        s = ""
    if g == None:
        g = ""
    return u":{piece_id}:{x}:{y}:{r}:{g}:{s}".format(**locals())


def formatBitMovementString(user_id, x="", y=""):
    return u":{user_id}:{x}:{y}".format(**locals())


def init_karma_key(redisConnection, puzzle, ip):
    """
    Initialize the karma value and expiration if not set.
    """
    karma_key = "karma:{puzzle}:{ip}".format(puzzle=puzzle, ip=ip)
    if redisConnection.setnx(karma_key, INITIAL_KARMA):
        redisConnection.expire(karma_key, HOUR)
    return karma_key


def get_public_karma_points(redisConnection, ip, user, puzzle):
    karma_key = init_karma_key(redisConnection, puzzle, ip)
    points_key = "points:{user}".format(user=user)
    recent_points = min(old_div(100, 2), int(redisConnection.get(points_key) or 0))
    karma = min(old_div(100, 2), int(redisConnection.get(karma_key)))
    karma = max(0, min(old_div(100, 2), karma + recent_points))
    return karma


def deletePieceDataFromRedis(redisConnection, puzzle, all_pieces):
    groups = set()
    for piece in all_pieces:
        pieceFromRedis = redisConnection.hgetall("pc:{puzzle}:{id}".format(**piece))
        # Find all the groups for each piece
        groups.add(pieceFromRedis.get("g"))

    # Create a pipe for buffering commands and disable atomic transactions
    pipe = redisConnection.pipeline(transaction=False)

    # Delete all piece data
    for piece in all_pieces:
        pipe.delete("pc:{puzzle}:{id}".format(**piece))

    # Delete all groups
    for g in groups:
        pipe.delete("pcg:{puzzle}:{g}".format(puzzle=puzzle, g=g))

    # Delete Piece Fixed
    pipe.delete("pcfixed:{puzzle}".format(puzzle=puzzle))

    # Delete Piece Stacked
    pipe.delete("pcstacked:{puzzle}".format(puzzle=puzzle))

    # Delete Piece X
    pipe.delete("pcx:{puzzle}".format(puzzle=puzzle))

    # Delete Piece Y
    pipe.delete("pcy:{puzzle}".format(puzzle=puzzle))

    # Remove from the pcupdates sorted set
    pipe.zrem("pcupdates", puzzle)

    pipe.execute()


def check_bg_color(bg_color):
    "Validate the bg_color that was submitted and return a default not valid."
    color_regex = re.compile(".*?#?([a-f0-9]{6}|[a-f0-9]{3}).*?", re.IGNORECASE)
    color_match = color_regex.match(bg_color)
    if color_match:
        return "#{0}".format(color_match.group(1))
    else:
        return "#808080"


strip_chars_regex = re.compile("\s+")


def normalize_name_from_display_name(display_name):
    "Strip out any white-space and lowercase the display_name from NameRegister when storing as name."
    name = display_name.lower()
    name = re.sub(strip_chars_regex, "", name)
    return name


def purge_route_from_nginx_cache(route, PURGEURLLIST):
    """Append route to the purge url list file which will then be picked up by
    the puzzle-massive-cache-purge service."""
    logger.info("Purging {} from nginx cache".format(route))
    f = open(PURGEURLLIST, "a")
    f.write(route + "\n")
    f.close()
