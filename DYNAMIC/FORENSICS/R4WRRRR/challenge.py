#!/usr/bin/env python3

from socketserver import ThreadingTCPServer, StreamRequestHandler
import os
import math

BANNER = r"""
                              .___.__               __                            .__
  ____  ____   ___________  __| _/|__| ____ _____ _/  |_  ____   ______    ______ |  |   ____ _____    ______ ____
_/ ___\/  _ \ /  _ \_  __ \/ __ | |  |/    \\__  \\   __\/ __ \ /  ___/    \____ \|  | _/ __ \\__  \  /  ___// __ \
\  \__(  <_> |  <_> )  | \/ /_/ | |  |   |  \/ __ \|  | \  ___/ \___ \     |  |_> >  |_\  ___/ / __ \_\___ \\  ___/
 \___  >____/ \____/|__|  \____ | |__|___|  (____  /__|  \___  >____  >    |   __/|____/\___  >____  /____  >\___  >
     \/                        \/         \/     \/          \/     \/     |__|             \/     \/     \/     \/
        ___.   .__       ________  __
        \_ |__ |  |  __ _\_____  \|  | _____.__.
  ______ | __ \|  | |  |  \_(__  <|  |/ <   |  |
 /_____/ | \_\ \  |_|  |  /       \    < \___  |
         |___  /____/____/______  /__|_ \/ ____|
             \/                 \/     \/\/
"""

# Safari World, Ibra (approx.)
TARGET_LAT = 22.630083
TARGET_LON = 58.539556

# Accept roughly ±1.5km around target
TOLERANCE = 0.015


def is_correct_location(lat, lon):
    dist = math.sqrt(
        (lat - TARGET_LAT) ** 2 +
        (lon - TARGET_LON) ** 2
    )
    return dist <= TOLERANCE


class ChallengeHandler(StreamRequestHandler):

    def send(self, text):
        self.wfile.write(text.encode())

    def handle(self):
        try:
            self.send(BANNER)

            self.send(
                "\n"
                "Approximate coordinates are sufficient.\n"
                "Format: latitude,longitude\n\n"
                "coordinates> "
            )

            user_input = (
                self.rfile.readline()
                .decode("utf-8", errors="ignore")
                .strip()
            )

            try:
                lat_str, lon_str = user_input.split(",")
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())

            except Exception:
                self.send(
                    "\n[-] Invalid format.\n"
                    "Example: 22.630083,58.539556\n"
                )
                return

            if not is_correct_location(lat, lon):
                self.send(
                    "\n[-] That's not where BLUEKY went.\n"
                    "[-] Keep following the trail.\n"
                )
                return

            self.send(
                "\n[+] Safari located.\n"
                "[+] Coordinates verified.\n\n"
            )

            flag = (
                os.getenv("GZCTF_FLAG")
                or os.getenv("FLAG")
                or "FLAG_NOT_SET"
            )

            try:
                with open("/flag", "r") as f:
                    flag = f.read().strip()
            except Exception:
                pass

            self.send(flag + "\n")

        except Exception as e:
            print(f"Client error: {e}")


if __name__ == "__main__":
    server = ThreadingTCPServer(("0.0.0.0", 9998), ChallengeHandler)
    server.allow_reuse_address = True

    print("Listening on 0.0.0.0:9999")
    server.serve_forever()
