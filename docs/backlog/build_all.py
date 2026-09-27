# -*- coding: utf-8 -*-
"""Regera issues, cenários BDD e README a partir de data.py e bdd.py."""
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
for s in ("generate.py", "gen_bdd.py"):
    subprocess.run([sys.executable, os.path.join(here, s)], check=True, cwd=here)
s = json.load(open(os.path.join(here, "out", "summary.json")))
rows = ["| Versão | Features | PBIs | Tasks | Story points | Horas |", "|---|---|---|---|---|---|"]
T = [0] * 5
for v, d in s.items():
    rows.append(f"| {v} | {d['features']} | {d['pbis']} | {d['tasks']} | {d['pts']} | {d['horas']} |")
    for i, k in enumerate(["features", "pbis", "tasks", "pts", "horas"]):
        T[i] += d[k]
rows.append(f"| **Total** | **{T[0]}** | **{T[1]}** | **{T[2]}** | **{T[3]}** | **{T[4]}** |")
t = open(os.path.join(here, "readme_template.md"), encoding="utf-8").read()
t = t.replace("__SUMMARY__", "\n".join(rows) + f"\n\nTotal de issues: {4 + T[0] + T[1] + T[2]}.")
t = t.replace("__TREE__", open(os.path.join(here, "out", "tree.txt"), encoding="utf-8").read().rstrip())
t = t.replace("- O limite de 3 tentativas", "- O limite de 3 tentativas") 
if "O limite de 3 tentativas de OTP" not in t:
    t = t.replace("- Os agentes A2A do cenário human-present usam o modelo", "- O limite de 3 tentativas de OTP (F-V5.3.3, RN02) é proposta, não regra do repositório.\n- Os agentes A2A do cenário human-present usam o modelo")
open(os.path.join(here, "README.md"), "w", encoding="utf-8").write(t)
print("README atualizado")
