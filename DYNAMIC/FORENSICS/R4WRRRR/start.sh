#!/bin/sh
set -e

FLAG_VALUE="${GZCTF_FLAG:-$FLAG}"

echo "$FLAG_VALUE" > /flag
chmod 444 /flag

exec python3 /challenge/challenge.py
