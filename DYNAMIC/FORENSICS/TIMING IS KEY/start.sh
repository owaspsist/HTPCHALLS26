#!/bin/bash
set -e

# GZ CTF injects flag here
FLAG_VALUE="${GZCTF_FLAG:-$FLAG}"

echo "$FLAG_VALUE" > /flag
chmod 444 /flag

exec python3 /challenge/challenge.py
