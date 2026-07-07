flag: warCTF{fl4c5_4r3_b3tt3r}

flag is encoded in b64 and hidden in LSBs of every 7th sample of provided wav file.

hint "every 7th sample" is appended as raw bytes to the end of the wav file. 

wav file header contains the number of audio bytes.

```c
// externals/ext13/wavinfo.c :
typedef struct _wave
{
    char  w_fileid[4];              /* chunk id 'RIFF'            */
    uint32 w_chunksize;             /* chunk size                 */
...
```

this lets you find the end of the audio file, and the remaining bits are the hint.

example script:

```py
import wave

INPUT_WAV = "encoded.wav"
STEP = 7

def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        b = 0
        for bit in bits[i:i + 8]:
            b = (b << 1) | bit
        out.append(b)
    return bytes(out)

with wave.open(INPUT_WAV, "rb") as wav:
    if wav.getsampwidth() != 2:
        raise RuntimeError()

    frames = wav.readframes(wav.getnframes())

num_samples = len(frames) // 2

bits = []

for sample_index in range(0, num_samples, STEP):
    offset = sample_index * 2

    sample = int.from_bytes(
        frames[offset:offset + 2],
        "little",
        signed=True,
    )

    bits.append(sample & 1)

length = 0
for bit in bits[:32]:
    length = (length << 1) | bit

message_bits = bits[32:32 + length * 8]

message = bits_to_bytes(message_bits).decode("ascii")

print(message)
```