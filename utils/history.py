# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history.json')
MAX_ENTRIES = 50

def get_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def add_history(entry):
    history = get_history()
    entry['timestamp'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    history.insert(0, entry)
    if len(history) > MAX_ENTRIES:
        history = history[:MAX_ENTRIES]
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError:
        pass

def clear_history():
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    except IOError:
        pass
