import pandas as pd
df = pd.concat([pd.read_csv("results/v0_clean.csv"),
                pd.read_csv("results/runs_v1.csv"),
                pd.read_csv("results/runs_v2.csv")])
df = df[df.backend == "gemini:gemini-3.1-flash-lite"]
df.to_csv("results/all_runs.csv", index=False)
a = df[df.kind == "attack"]
t = a.groupby(["version", "category"])["success"].mean().unstack().mul(100).round(1)
t["OVERALL"] = a.groupby("version")["success"].mean().mul(100).round(1)
t["BENIGN_ANSWERED"] = df[df.kind == "benign"].groupby("version")["success"].mean().mul(100).round(1)
print(df.groupby(["version", "kind"]).size()); print(t)