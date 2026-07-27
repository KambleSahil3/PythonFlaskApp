#!/bin/bash

URL="http://localhost:5000/health"

echo "Starting health monitor — polling $URL every 10 seconds. Press Ctrl+C to stop."
echo "---"

while true; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$TIMESTAMP] HTTP $STATUS"
  sleep 10
done
