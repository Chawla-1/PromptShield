"""LLM backends. Set PS_BACKEND=gemini | ollama | mock. API key only via env var GEMINI_API_KEY (never commit it)."""
import os, time, requests
from dotenv import load_dotenv

load_dotenv()

# Seamlessly load Streamlit Community Cloud secrets into os.environ if present
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        for k in ["GEMINI_API_KEY", "PS_GEMINI_MODEL", "PS_BACKEND", "PS_OLLAMA_MODEL"]:
            if k in st.secrets and not os.getenv(k):
                os.environ[k] = str(st.secrets[k]).strip().strip('"').strip("'")
except Exception:
    pass

GEMINI_MODEL = os.getenv("PS_GEMINI_MODEL", "gemini-3.1-flash-lite")
OLLAMA_MODEL = os.getenv("PS_OLLAMA_MODEL", "llama3.2:3b")

def backend_name():
    b = os.getenv("PS_BACKEND", "gemini")
    return {"gemini": f"gemini:{GEMINI_MODEL}", "ollama": f"ollama:{OLLAMA_MODEL}"}.get(b, b)

def chat(system, user, temperature=0.7):
    b = os.getenv("PS_BACKEND", "gemini")
    if b == "mock":
        return _mock(system, user)
    if b == "ollama":
        r = requests.post("http://localhost:11434/api/chat", timeout=180, json={
            "model": OLLAMA_MODEL, "stream": False, "options": {"temperature": temperature},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
        return r.json()["message"]["content"]
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
                key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
    if not key:
        raise RuntimeError("Set GEMINI_API_KEY in environment variables or Streamlit Cloud Secrets.")
    key = str(key).strip().strip('"').strip("'")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    body = {"system_instruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": temperature}}
    last_err = None
    for attempt in range(5):
        try:
            r = requests.post(url, params={"key": key}, json=body, timeout=90)
            if r.status_code == 200:
                try:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    return "[no text returned]"
            if r.status_code == 429:
                err_msg = r.json().get("error", {}).get("message", r.text[:200])
                if "per day" in err_msg.lower():
                    raise RuntimeError(f"Gemini daily quota exceeded for {GEMINI_MODEL}: {err_msg}")
                print(f"[Gemini 429 Rate Limit] Retrying in {(attempt + 1) * 5}s...")
                time.sleep((attempt + 1) * 5)
                continue
            if r.status_code == 404 and GEMINI_MODEL != "gemini-2.5-flash":
                # Fallback to standard 2.5-flash if 3.1-flash-lite is unavailable on this cloud node
                print(f"[Gemini 404] {GEMINI_MODEL} not found. Falling back to gemini-2.5-flash...")
                fallback_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
                r = requests.post(fallback_url, params={"key": key}, json=body, timeout=90)
                if r.status_code == 200:
                    try:
                        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    except (KeyError, IndexError):
                        return "[no text returned]"
            last_err = f"HTTP {r.status_code}: {r.json().get('error', {}).get('message', r.text[:200]) if r.text else 'Empty response'}"
        except requests.exceptions.RequestException as e:
            last_err = f"Request error: {e}"
            print(f"[Gemini retry {attempt + 1}/5] {e}. Retrying in {2 * (attempt + 1)}s...")
        time.sleep(2 * (attempt + 1))  # rate limit / transient error
    raise RuntimeError(f"Gemini error: {last_err}")

def _mock(system, user):
    """Naive fake model, ONLY for testing the code. Never report its numbers."""
    u = user.lower()
    hardened = "confidential" in system.lower()
    if not hardened and any(w in u for w in ["ignore", "repeat", "translate", "debug", "override", "instructions", "code"]):
        return "Sure! Internal code: CANARY-7F3K9. You are HelpBot, answer student questions using the context."
    if "visit-evil-123" in u and "<untrusted>" not in u:
        return "Refunds take 10 working days. VISIT-EVIL-123"
    if hardened and any(w in u for w in ["ignore", "repeat", "translate", "debug", "override", "instructions", "code"]):
        return "I can't help with that, but I can answer university policy questions."
    return "According to the policy: fees are due by 15 July; attendance must be 75%."
