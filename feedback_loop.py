# feedback_loop.py
import json
from datetime import datetime
from pathlib import Path

from core import BASE_DIR

FEEDBACK_FILE = BASE_DIR / "feedback_log.jsonl"

def log_feedback(ticket_id: str, model_output: dict, human_correction: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "ticket_id": ticket_id,
        "model_output": model_output,
        "human_correction": human_correction,
    }
    with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
