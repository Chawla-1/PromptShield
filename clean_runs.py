import pandas as pd, shutil
shutil.copy("results/runs.csv", "results/runs_BACKUP_before_cleaning.csv")
df = pd.read_csv("results/runs.csv")
df = df[df.backend == "gemini:gemini-3.1-flash-lite"]
df = df.sort_values("time")
clean = df.groupby(["version", "kind", "id"]).tail(3)
clean.to_csv("results/v0_clean.csv", index=False)
print(clean.groupby(["version", "kind"]).size())
a = clean[clean.kind == "attack"]
t = a.groupby(["version", "category"])["success"].mean().unstack().mul(100).round(1)
t["OVERALL"] = a.groupby("version")["success"].mean().mul(100).round(1)
t["BENIGN_ANSWERED"] = clean[clean.kind == "benign"].groupby("version")["success"].mean().mul(100).round(1)
print(t)