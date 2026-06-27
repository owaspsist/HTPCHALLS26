#!/usr/bin/env python3

from socketserver import ThreadingTCPServer, StreamRequestHandler
import os


BANNER = r"""
▗▄▄▄▖ ▄▄▄ ▗▄ ▄▖ ▄▄▄ ▗▄ ▗▖  ▄▄       ▄▄▄  ▗▄▖      ▗▖ ▄▖▗▄▄▄▖▄▖ ▗▄
▝▀█▀▘ ▀█▀ ▐█ █▌ ▀█▀ ▐█ ▐▌ █▀▀▌      ▀█▀ ▗▛▀▜      ▐▌▐▛ ▐▛▀▀▘▐▙ ▟▌
  █    █  ▐███▌  █  ▐▛▌▐▌▐▌          █  ▐▙        ▐▙█  ▐▌    █▄█ 
  █    █  ▐▌█▐▌  █  ▐▌█▐▌▐▌▗▄▖       █   ▜█▙      ▐██  ▐███  ▝█▘ 
  █    █  ▐▌▀▐▌  █  ▐▌▐▟▌▐▌▝▜▌       █     ▜▌     ▐▌▐▙ ▐▌     █  
  █   ▄█▄ ▐▌ ▐▌ ▄█▄ ▐▌ █▌ █▄▟▌      ▄█▄ ▐▄▄▟▘     ▐▌ █▖▐▙▄▄▖  █  
  ▀   ▀▀▀ ▝▘ ▝▘ ▀▀▀ ▝▘ ▀▘  ▀▀       ▀▀▀  ▀▀▘      ▝▘ ▝▘▝▀▀▀▘  ▀  

     ▗▖   ▗▄▖        ▄▄▖ ▗▖
     ▐▌   ▝▜▌       ▐▀▀█▖▐▌
     ▐▙█▙  ▐▌  ▐▌ ▐▌   ▟▌▐▌▟▛ ▝█ █▌
     ▐▛ ▜▌ ▐▌  ▐▌ ▐▌ ▐██ ▐▙█   █▖█
 ██▌ ▐▌ ▐▌ ▐▌  ▐▌ ▐▌   ▜▌▐▛█▖  ▐█▛
     ▐█▄█▘ ▐▙▄ ▐▙▄█▌▐▄▄█▘▐▌▝▙   █▌
     ▝▘▀▘   ▀▀  ▀▀▝▘ ▀▀▘ ▝▘ ▀▘  █
                               █▌
"""

SECRET = "KHUL_JA_SIM_SIM"


class ChallengeHandler(StreamRequestHandler):
    def handle(self):
        try:
            self.wfile.write(BANNER.encode() + b"\n\n")
            self.wfile.write(b"Enter the secret key found at the destination: ")

            user_input = (
                self.rfile.readline()
                .strip()
                .decode("utf-8", errors="ignore")
            )

            if user_input == SECRET:
                self.wfile.write(b"\nCorrect! Fetching your flag...\n\n")

                flag = os.getenv("GZCTF_FLAG") or os.getenv("FLAG") or "FLAG_NOT_SET"

                try:
                    with open("/flag", "r") as f:
                        flag = f.read().strip()
                except:
                    pass

                self.wfile.write(flag.encode() + b"\n")

            else:
                self.wfile.write(b"\nWrong key! The trail goes cold here.\n")

        except Exception as e:
            print(f"Client error: {e}")


if __name__ == "__main__":
    server = ThreadingTCPServer(("0.0.0.0", 9999), ChallengeHandler)
    server.allow_reuse_address = True

    print("Listening on 0.0.0.0:9996")
    server.serve_forever()
