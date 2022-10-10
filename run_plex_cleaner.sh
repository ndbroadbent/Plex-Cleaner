#!/bin/bash
set -euo pipefail

cd /opt/Plex-Cleaner
rm -f plexcleaner.log

STATUS=1
if /usr/bin/python3 PlexCleaner.py && [ -f plexcleaner.log ] && ! grep -q "ERROR" plexcleaner.log; then
  STATUS=0
fi

HEALTHCHECKSIO_ID="$(cat healthchecksio_id)"
printf "Healthchecks.io ping ($STATUS) => ${HEALTHCHECKSIO_ID}: " | tee plexcleaner.log
curl --retry 3 -s https://hc-ping.com/$HEALTHCHECKSIO_ID/$STATUS | tee plexcleaner.log
echo | tee plexcleaner.log
