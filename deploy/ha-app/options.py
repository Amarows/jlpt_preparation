import json
import sys

value = json.loads(open("/data/options.json", encoding="utf-8").read()).get(sys.argv[1]) or ""
sys.stdout.write(str(value))
