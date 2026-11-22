import json, streamlit as st
from backend import backend_name
from target_bot import RagBot
from judge import attack_succeeded
from defences import SYSTEM

st.set_page_config(page_title="PromptShield", page_icon="🛡️")
st.title("🛡️ PromptShield")
st.caption(f"Attack a fake university bot and compare defence prompts. Model: {backend_name()}. All data is fictional.")
attacks = json.load(open("attacks/attacks.json", encoding="utf-8"))
version = st.selectbox("Defence version", ["v0", "v1", "v2"], format_func=lambda v: {"v0":"v0 baseline","v1":"v1 hardened instructions","v2":"v2 + spotlighting"}[v])
choice = st.selectbox("Attack", ["(write my own)"] + [f'{a["id"]} - {a["prompt"][:60]}' for a in attacks])
atk = None if choice == "(write my own)" else next(a for a in attacks if a["id"] == choice.split(" - ")[0])
text = st.text_area("Message to the bot", value=atk["prompt"] if atk else "", height=80)
with st.expander("Show system prompt for this version"): st.code(SYSTEM[version])
if st.button("Run"):
    bot = RagBot(version, [atk["poison"]] if atk and "poison" in atk else None)
    out = bot.answer(text)
    st.write("**Bot reply:**"); st.info(out)
    if atk:
        st.error("ATTACK SUCCEEDED") if attack_succeeded(atk, out) else st.success("ATTACK BLOCKED")
st.divider()
try:
    import pandas as pd
    df = pd.read_csv("results/runs.csv")
    st.subheader("Saved results (results/runs.csv)")
    a = df[df.kind == "attack"].groupby(["backend", "version"])["success"].mean().mul(100).round(1).rename("ASR %")
    st.dataframe(a)
except Exception:
    st.caption("No saved results yet. Run run_eval.py first.")
