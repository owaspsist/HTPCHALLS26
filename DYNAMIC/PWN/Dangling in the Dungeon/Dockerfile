FROM python:3.11-slim

# Create a dedicated, non-root user
RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf

# Set up the challenge directory
WORKDIR /app

# Copy the files into the container
COPY dungeon.py /app/dungeon.py
COPY start.sh /app/start.sh

# Make both scripts executable
RUN chmod +x /app/dungeon.py /app/start.sh

# Secure the directory (root owns it, ctf can read/execute)
RUN chown -R root:ctf /app && chmod -R 750 /app

# Expose the exact port used in the Python script
EXPOSE 9993

# The container MUST start as root to catch GZCTF_FLAG and write /flag
USER root

# Execute the wrapper script using JSON array syntax
CMD ["/app/start.sh"]
