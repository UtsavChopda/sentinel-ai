import requests
import json

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"
PROMPT_FILE = "C:/sentinel-ai/prompts/triage_prompt.txt"


# Load prompt template
def load_prompt(alert_text):
    with open(PROMPT_FILE, "r") as f:
        template = f.read()
    return template.replace("{ALERT}", alert_text)


# Send alert to LLM
def analyze_alert(alert_text):
    prompt = load_prompt(alert_text)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()

        raw_output = response.json()["response"].strip()

        # Remove ```json wrapper if present
        if raw_output.startswith("```"):
            raw_output = raw_output.split("```")[1]
            if raw_output.startswith("json"):
                raw_output = raw_output[4:]
        raw_output = raw_output.strip()

        return json.loads(raw_output)

    except requests.exceptions.ConnectionError:
        print("Error: Ollama service is not running.")
        return None

    except json.JSONDecodeError:
        print("Error: Invalid JSON returned by model.")
        return None


# Print result cleanly
def print_result(result):
    if not result:
        print("No result returned.")
        return

    print("\n================ ALERT TRIAGE RESULT ================\n")

    print(f"Severity       : {result.get('severity')}")
    print(f"Confidence     : {result.get('confidence')}%")
    print(f"True Positive  : {result.get('is_true_positive')}")
    print(f"\nTitle          : {result.get('title')}")
    print(f"\nSummary        : {result.get('summary')}")

    print("\nIndicators of Compromise:")
    for ioc in result.get("iocs", []):
        print(f" - {ioc}")

    print("\nMITRE Techniques:")
    for technique in result.get("mitre_techniques", []):
        print(f" - {technique}")

    print("\nRecommended Investigation Steps:")
    for step in result.get("investigation_steps", []):
        print(f" - {step}")

    print(f"\nVerdict        : {result.get('verdict')}")
    print("\n=====================================================\n")


if __name__ == "__main__":
    test_alert = """
    ALERT SOURCE: Endpoint EDR
    TIMESTAMP: 2026-02-26 03:14:22
    HOST: DESKTOP-HR04
    USER: sarah.jones

    Process creation event detected:
    Parent Process: WINWORD.EXE
    Child Process: cmd.exe
    Command Line: cmd.exe /c powershell -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0AA==

    Additional context:
    - User opened an email attachment
    - No similar behavior in last 30 days
    - Attachment name: invoice_march2026.docm
    """

    result = analyze_alert(test_alert)
    print_result(result)