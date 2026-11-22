"""Usage: python run_eval.py --versions v0 v1 v2 --runs 3 [--limit 5]"""
import argparse, csv, json, os, datetime, time
import pandas as pd
from backend import backend_name
from target_bot import RagBot
from judge import attack_succeeded, benign_ok

ap = argparse.ArgumentParser()
ap.add_argument("--versions", nargs="+", default=["v0", "v1", "v2"])
ap.add_argument("--runs", type=int, default=3)
ap.add_argument("--limit", type=int, default=None, help="use only first N attacks per category (pilot)")
ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests to prevent rate limits")
ap.add_argument("--out", default="results/runs.csv")
a = ap.parse_args()

attacks = json.load(open("attacks/attacks.json", encoding="utf-8"))
benign = json.load(open("test-data/benign.json", encoding="utf-8"))
if a.limit:
    seen, keep = {}, []
    for x in attacks:
        seen[x["category"]] = seen.get(x["category"], 0) + 1
        if seen[x["category"]] <= a.limit: keep.append(x)
    attacks, benign = keep, benign[:a.limit]

os.makedirs("results", exist_ok=True)
new = not os.path.exists(a.out)
bk = backend_name()
with open(a.out, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new: w.writerow(["time","backend","version","kind","id","category","run","success","output"])
    for v in a.versions:
        print(f"=== Evaluating Version: {v} ===")
        for x in attacks:
            bot = RagBot(v, [x["poison"]] if "poison" in x else None)
            for r in range(a.runs):
                out = bot.answer(x["prompt"])
                succ = int(attack_succeeded(x, out))
                print(f"  [{v}] Attack {x['id']} (run {r+1}/{a.runs}): {'SUCCEEDED' if succ else 'BLOCKED'}")
                w.writerow([datetime.datetime.now().isoformat(), bk, v, "attack", x["id"], x["category"], r,
                            succ, out.replace("\n", " ")])
                if a.delay: time.sleep(a.delay)
        for b in benign:
            bot = RagBot(v)
            for r in range(a.runs):
                out = bot.answer(b["question"])
                ok = int(benign_ok(b, out))
                print(f"  [{v}] Benign {b['id']} (run {r+1}/{a.runs}): {'ANSWERED' if ok else 'MISSED'}")
                w.writerow([datetime.datetime.now().isoformat(), bk, v, "benign", b["id"], "benign", r,
                            ok, out.replace("\n", " ")])
                if a.delay: time.sleep(a.delay)
        f.flush(); print(f"done {v}\n")

def summary(path=a.out):
    df = pd.read_csv(path)
    df = df[df.backend == bk]
    atk = df[df.kind == "attack"].groupby(["version", "category"])["success"].mean().unstack().mul(100).round(1)
    atk["OVERALL_ASR_%"] = df[df.kind == "attack"].groupby("version")["success"].mean().mul(100).round(1)
    atk["BENIGN_ANSWERED_%"] = df[df.kind == "benign"].groupby("version")["success"].mean().mul(100).round(1)
    return atk
if __name__ == "__main__":
    print(f"\nBackend: {bk}\n(ASR = attack success rate, lower is better; BENIGN_ANSWERED higher is better)\n")
    print(summary())
