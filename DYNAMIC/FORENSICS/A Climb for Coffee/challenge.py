#!/usr/bin/env python3

from socketserver import ThreadingTCPServer, StreamRequestHandler


class ChallengeHandler(StreamRequestHandler):
    def handle(self):
        try:
            self.wfile.write(b"========================================\n")
            self.wfile.write(b"          Welcome to Map Steg           \n")
            self.wfile.write(b"   Follow the trail to find the secret  \n")
            self.wfile.write(b" -blu3ky                                \n")
            self.wfile.write(b"========================================\n")
            self.wfile.write(
                b"Enter the secret key found at the destination: "
            )

            user_input = (
                self.rfile.readline()
                .strip()
                .decode("utf-8", errors="ignore")
            )

            correct_key = "0m4n_1s_p34ac3fu1"

            if user_input == correct_key:
                self.wfile.write(b"\nCorrect! Fetching your flag...\n")

                try:
                    with open("/flag", "r") as f:
                        flag = f.read().strip()

                    self.wfile.write(
                        f"Here is your flag:\n{flag}\n".encode("utf-8")
                    )

                except FileNotFoundError:
                    self.wfile.write(
                        b"Error: Flag file not found.\n"
                    )
            else:
                self.wfile.write(
                    b"\nWrong key! The trail goes cold here.\n"
                )

        except Exception as e:
            print(f"Client error: {e}")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 9997

    server = ThreadingTCPServer((HOST, PORT), ChallengeHandler)
    server.allow_reuse_address = True

    print(f"Listening on {HOST}:{PORT}")
    server.serve_forever()
