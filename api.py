from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import json
import os
import time
import requests

app = FastAPI(
    title="AI SOC Alert Triage API",
    version="1.0.0"
)

# Enable CORS (for frontend dashboard if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
PROMPT_FILE = "C:/sentinel-ai/prompts/triage_prompt.txt"
RESULTS_DIR = "C:/sentinel-ai/results"

os.makedirs(RESULTS_DIR, exist_ok=True)


class AlertRequest(BaseModel):
    alert_id: Optional[str] = None
    source: Optional[str] = "Manual"
    raw_alert: str


def call_model(alert_text: str):
    with open(PROMPT_FILE, "r") as f:
        template = f.read()

    prompt = template.replace("{ALERT}", alert_text)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    raw = response.json()["response"].strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())


@app.get("/")
def root():
    return {
        "service": "AI SOC Alert Triage",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    try:
        requests.get("http://localhost:11434", timeout=5)
        model_status = "reachable"
    except:
        model_status = "unreachable"

    return {
        "api_status": "online",
        "model_status": model_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/triage")
def triage_alert(req: AlertRequest):
    start_time = time.time()

    try:
        result = call_model(req.raw_alert)
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Model service not available"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid response from model"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    alert_id = req.alert_id or f"ALT-{int(time.time())}"

    result.update({
        "alert_id": alert_id,
        "source": req.source,
        "triaged_at": datetime.utcnow().isoformat(),
        "processing_time_seconds": round(time.time() - start_time, 2)
    })

    output_path = os.path.join(
        RESULTS_DIR,
        f"{alert_id}_result.json"
    )

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


@app.get("/results")
def get_results():
    results = []

    for filename in sorted(os.listdir(RESULTS_DIR)):
        if filename.endswith("_result.json"):
            try:
                with open(os.path.join(RESULTS_DIR, filename)) as f:
                    results.append(json.load(f))
            except:
                continue

    results = sorted(
        results,
        key=lambda x: x.get("triaged_at", ""),
        reverse=True
    )

    return {
        "total": len(results),
        "results": results
    }


@app.get("/results/{alert_id}")
def get_single_result(alert_id: str):
    path = os.path.join(
        RESULTS_DIR,
        f"{alert_id}_result.json"
    )

    if not os.path.exists(path):
        raise HTTPException(
            status_code=404,
            detail="Result not found"
        )

    with open(path) as f:
        return json.load(f)


@app.get("/stats")
def get_statistics():
    results = get_results()["results"]

    stats = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "true_positive": 0,
        "false_positive": 0
    }

    for r in results:
        severity = r.get("severity", "LOW")
        if severity in stats:
            stats[severity] += 1

        if r.get("is_true_positive"):
            stats["true_positive"] += 1
        else:
            stats["false_positive"] += 1

    stats["total"] = len(results)
    return stats


@app.delete("/results")
def clear_results():
    count = 0

    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith("_result.json"):
            os.remove(os.path.join(RESULTS_DIR, filename))
            count += 1

    return {"deleted_files": count}