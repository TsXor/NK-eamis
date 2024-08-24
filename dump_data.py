import json
from pathlib import Path
from eamis_sys import EamisCatcher

HERE = Path(__file__).parent

client = EamisCatcher.from_webview()
lesson_data, std_count = client.all_lesson_data()

with open(HERE / 'lesson_data.json', 'wt', encoding='utf-8') as log_wfp:
    json.dump(lesson_data, log_wfp, ensure_ascii=False, indent=4)
with open(HERE / 'std_count.json', 'wt', encoding='utf-8') as log_wfp:
    json.dump(std_count, log_wfp, ensure_ascii=False, indent=4)