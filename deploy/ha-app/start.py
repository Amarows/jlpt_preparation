import json
import os
import runpy
import sys

options = json.loads(open("/data/options.json", encoding="utf-8").read())
os.environ.update({
    "JLPT_HOME": "/config",
    "JLPT_AUDIO": "/media/jlpt/audio",
    "JLPT_BIND": "127.0.0.1",
    "JLPT_PORT": "8080",
    "JLPT_AUTH": "tailscale",
    "JLPT_ORIGIN": str(options.get("origin") or ""),
})
os.chdir("/app")
sys.path.insert(0, "/app")
runpy.run_path("/app/server.py", run_name="__main__")
