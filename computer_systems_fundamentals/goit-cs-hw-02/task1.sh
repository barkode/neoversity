#!/bin/bash

LOG_FILE="website_status.log"

WEBSITES=(
    "https://google.com"
    "https://facebook.com"
    "https://twitter.com"
)

> "$LOG_FILE"

for site in "${WEBSITES[@]}"; do
    http_code=$(curl -L -s -o /dev/null -w "%{http_code}" --max-time 10 "$site")

    if [ "$http_code" -eq 200 ]; then
        echo "<$site> is UP" >> "$LOG_FILE"
    else
        echo "<$site> is DOWN" >> "$LOG_FILE"
    fi
done

echo "Site log: $LOG_FILE"