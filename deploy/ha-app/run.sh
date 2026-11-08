#!/bin/sh
set -eu
SOCK=/tmp/tailscaled.sock
mkdir -p /data/tailscale
tailscaled --tun=userspace-networking --statedir=/data/tailscale --socket="$SOCK" &
i=0
until [ -S "$SOCK" ]; do
  i=$((i + 1))
  [ "$i" -le 30 ] || { echo "tailscaled did not start" >&2; exit 1; }
  sleep 1
done
state=$(tailscale --socket="$SOCK" status --json 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get("BackendState",""))' || true)
if [ "$state" != "Running" ]; then
  umask 077
  python3 /options.py ts_authkey > /tmp/ts_authkey
  [ -s /tmp/ts_authkey ] || { rm -f /tmp/ts_authkey; echo "ts_authkey option is empty and the node is not logged in" >&2; exit 1; }
  tailscale --socket="$SOCK" up --auth-key=file:/tmp/ts_authkey --hostname=jlpt
  rm -f /tmp/ts_authkey
fi
tailscale --socket="$SOCK" serve --bg 8080
exec python3 /start.py
