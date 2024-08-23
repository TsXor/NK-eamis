import json
from pathlib import Path
from eamis_sys import EamisCatcher

HERE = Path(__file__).parent

client = EamisCatcher.from_webview()
lesson_data = client.all_lesson_data()

with open(HERE / 'data.json', 'wt', encoding='utf-8') as log_wfp:
    json.dump(lesson_data, log_wfp, ensure_ascii=False, indent=4)
