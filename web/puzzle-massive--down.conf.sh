#!/usr/bin/env bash

set -eu -o pipefail

ENVIRONMENT=$1
SRVDIR=$2
NGINXLOGDIR=$3
PORTREGISTRY=$4
INTERNALIP=$5
CACHEDIR=$6

# shellcheck source=/dev/null
source "$PORTREGISTRY"

# shellcheck source=/dev/null
source .env

cat <<HERE
server {
  # Redirect for old hosts
  listen       80;
  server_name puzzle.weboftomorrow.com www.puzzle.massive.xyz;
  return       301 http://puzzle.massive.xyz\$request_uri;
}

map \$request_uri \$loggable {
    # Don't log requests to the anonymous login link.
    ~/puzzle-api/bit/.* 0;
    ~/newapi/user-login/.* 0;

    default 1;
}


server {
  listen      80;
  root ${SRVDIR}root;
  valid_referers server_names;

  # Rewrite the homepage url
  rewrite ^/index.html\$ / permanent;

  # redirect the old puzzlepage url
  rewrite ^/puzzle/(.*)\$ /chill/site/puzzle/\$1/ permanent;

  # rewrite old bit login (Will probably always need to have this rewritten)
  rewrite ^/puzzle-api/bit/([^/]+)/?\$ /newapi/user-login/\$1/;

  # handle old style of scale query param where 'scale=' meant to use without scaling
  rewrite ^/chill/site/puzzle/([^/]+)/\$ /chill/site/puzzle/\$1/scale/\$arg_scale/?;
  rewrite ^/chill/site/puzzle/([^/]+)/scale//\$ /chill/site/puzzle/\$1/scale/0/? last;
  rewrite ^/chill/site/puzzle/([^/]+)/scale/(\d+)/\$ /chill/site/puzzle/\$1/scale/1/? last;

  # redirect old puzzle queues
  rewrite ^/chill/site/queue/(.*)\$ /chill/site/puzzle-list/ permanent;

  # temporary redirect player profile page
  rewrite ^/chill/site/player/[^/]+/\$ /chill/site/player/ redirect;

  rewrite ^/\$ /chill/site/front/ last;
  location / {
    try_files \$uri \$uri =404;
  }
  location /chill/site/ {
    # stop caching
    expires -1;
    add_header Cache-Control "public";

    rewrite ^/.* /error_page.html break;
  }
  location /newapi/ {
    return 503;
  }
  location /newapi/message/ {
    rewrite ^/.* /puzzle-massive-message.html break;
  }

HERE

if test "${ENVIRONMENT}" == 'development'; then
cat <<HEREBEDEVELOPMENT
  # Only when in development should the site be accessible via internal ip.
  # This makes it easier to test with other devices that may not be able to
  # update a /etc/hosts file.
  server_name local-puzzle-massive $INTERNALIP;
HEREBEDEVELOPMENT
else
cat <<HEREBEPRODUCTION
  server_name puzzle-blue puzzle-green ${DOMAIN_NAME};
HEREBEPRODUCTION
fi
cat <<HERE
  error_page 500 501 502 504 505 506 507 /error_page.html;
  location = /error_page.html {
    ssi on;
    ssi_silent_errors off;
    internal;
  }

  error_page 503 /overload_page.html;
  location = /overload_page.html {
    internal;
  }

  error_page 401 403 /unauthorized_page.html;
  location = /unauthorized_page.html {
    internal;
  }

  error_page 404 /notfound_page.html;
  location = /notfound_page.html {
    internal;
  }

  error_page 429 /too_many_requests_page.html;
  location = /too_many_requests_page.html {
    internal;
  }

  error_page 409 /conflict_page.html;
  location = /conflict_page.html {
    internal;
  }
}
HERE