```
TZ="Europe/Moscow"
0 12,21 * * * source /scripts/todoist/.venv/bin/activate && /scripts/todoist/.venv/bin/python /scripts/todoist/todoist.py >> /scripts/todoist/log_file.txt 2>&1
```