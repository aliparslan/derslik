import json
import re
from pathlib import Path

# Load passages
with open('/tmp/passages_full.json') as f:
    passages = json.load(f)

# Load Quran
with open('/tmp/quran-simple.json') as f:
    qdata = json.load(f)['data']

ayahs = {}
for s in qdata['surahs']:
    snum = s['number']
    for a in s['ayahs']:
        anum = a['numberInSurah']
        ayahs[(snum, anum)] = a['text']

# Manual map for all 133 passages
# Format: idx -> (replacement_text, note)
# We will construct a mapping of exact old_text -> new_text

print(f"Total passages to map: {len(passages)}")
