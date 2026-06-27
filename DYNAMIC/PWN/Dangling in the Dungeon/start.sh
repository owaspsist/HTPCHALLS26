#!/bin/bash
set -e

# Grab the flag and write it without trailing newlines
echo -n "${GZCTF_FLAG:-flag{local_test_fallback}}" > /flag

# Lock the flag file
chmod 444 /flag

# Destroy the environment variable so players can't read it
unset GZCTF_FLAG

# Start the game as the unprivileged user
exec su -s /bin/bash ctf -c "python3 /app/dungeon.py"
