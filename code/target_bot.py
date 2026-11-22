import glob, re
from backend import chat
from defences import build

def _tok(t): return set(re.findall(r"\w+", t.lower()))

def load_chunks(folder="data/policy_docs"):
    out = []
    for p in sorted(glob.glob(f"{folder}/*.txt")):
        out += [c.strip() for c in open(p, encoding="utf-8").read().split("\n\n") if c.strip()]
    return out

class RagBot:
    def __init__(self, version="v0", extra_docs=None):
        self.version = version
        self.chunks = load_chunks() + (extra_docs or [])

    def retrieve(self, q, k=2):
        qt = _tok(q)
        ranked = sorted(self.chunks, key=lambda c: len(qt & _tok(c)), reverse=True)
        return ranked[:k]

    def answer(self, question, temperature=0.7):
        if not question.strip():
            return "Please type a question about university policy."   # input validation
        system, user = build(self.version, question, self.retrieve(question))
        return chat(system, user, temperature)
