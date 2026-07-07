flag: warCTF{ch3ck_7h3_4lph4}

flag is encoded in b64 and hidden in LSBs of alpha channel.

example script:

```py
from PIL import Image

INPUT_IMAGE = "encoded.png"

img = Image.open(INPUT_IMAGE).convert("RGBA")
width, height = img.size
pixels = img.load()

bits = []

for y in range(height):
    for x in range(width):
        _, _, _, a = pixels[x, y]
        bits.append(a & 1)

length = 0
for bit in bits[:32]:
    length = (length << 1) | bit

message_bits = bits[32:32 + length * 8]

message = bytearray()

for i in range(0, len(message_bits), 8):
    byte = 0
    for bit in message_bits[i:i + 8]:
        byte = (byte << 1) | bit
    message.append(byte)

print(message.decode("ascii"))
```