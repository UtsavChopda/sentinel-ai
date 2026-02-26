import json
import os
import time
from datetime import datetime
import requests
import sys

# Import alert dataset
sys.path.append("C:/sentinel-ai/alerts")
from alert_library import ALERTS

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
OUTPUT_DIR = "C:/sentinel-ai/results"
PROMPT_FILE = "C:/sentinel-ai/prompts/triage_prompt.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def analyze_single(alert):
    with open(PROMPT_FILE, "r") as f:
        template = f.read()

    prompt = template.replace("{ALERT}", alert["alert"])

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    raw = response.json()["response"].strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)

    result["alert_id"] = alert["id"]
    result["source"] = alert["source"]
    result["triaged_at"] = datetime.utcnow().isoformat()

    return result


def run_batch():
    all_results = []
    stats = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "true_positive": 0,
        "false_positive": 0
    }

    start_time = time.time()

    for alert in ALERTS:
        try:
            result = analyze_single(alert)
            all_results.append(result)

            severity = result.get("severity", "LOW")
            if severity in stats:
                stats[severity] += 1

            if result.get("is_true_positive"):
                stats["true_positive"] += 1
            else:
                stats["false_positive"] += 1

            output_file = os.path.join(
                OUTPUT_DIR,
                f"{alert['id']}_result.json"
            )

            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)

        except Exception as e:
            all_results.append({
                "alert_id": alert["id"],
                "error": str(e)
            })

        time.sleep(1)

    summary_file = os.path.join(
        OUTPUT_DIR,
        f"batch_summary_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(summary_file, "w") as f:
        json.dump({
            "statistics": stats,
            "total_alerts": len(ALERTS),
            "processed_at": datetime.utcnow().isoformat(),
            "results": all_results
        }, f, indent=2)

    elapsed = round(time.time() - start_time, 2)

    print("\nBatch Processing Complete")
    print(f"Total Alerts Processed : {len(ALERTS)}")
    print(f"Processing Time        : {elapsed} seconds")
    print(f"Results Directory      : {OUTPUT_DIR}")
    print(f"Summary Report         : {summary_file}")


if __name__ == "__main__":
    run_batch()