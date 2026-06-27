import subprocess
import time

PIN_LEN = 8
DIGITS = "0123456789"

TRIALS = 8  # increase if noisy system

def measure(pin):
    total = 0.0

    for _ in range(TRIALS):
        start = time.perf_counter()

        p = subprocess.Popen(
            ["./pin_checker"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        p.communicate(input=(pin + "\n").encode())

        end = time.perf_counter()
        total += (end - start)

    return total / TRIALS


found = ""

for i in range(PIN_LEN):
    best_digit = None
    best_time = -1

    print(f"\n[+] Finding position {i+1}")

    for d in DIGITS:
        test_pin = found + d + "0" * (PIN_LEN - i - 1)
        t = measure(test_pin)

        print(f"Try {test_pin} -> {t:.4f}s")

        if t > best_time:
            best_time = t
            best_digit = d

    found += best_digit
    print(f"[+] Current PIN: {found}")

print("\n[+] FINAL PIN FOUND:", found)
