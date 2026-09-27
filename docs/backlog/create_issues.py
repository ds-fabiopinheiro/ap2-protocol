#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cria labels, milestones e issues (com sub-issues) no GitHub a partir de out/.

Requer a CLI `gh` autenticada com permissão de escrita em issues no repositório.

Uso:
  python3 create_issues.py                 # simulação: só mostra o que faria
  python3 create_issues.py --apply         # cria de verdade
  python3 create_issues.py --apply --only v3   # só uma versão

Idempotência: antes de criar, procura uma issue aberta ou fechada com o mesmo
título; se existir, reutiliza o número. O mapa chave → número fica em
out/created.json.
"""
import argparse
import json
import os
import subprocess
import sys

REPO = "ds-fabiopinheiro/ap2-protocol"
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")

LABELS = {
    "tipo:épico": ("5319E7", "Épico: uma versão (branch homolog-vN)"),
    "tipo:feature": ("1D76DB", "Feature de um épico"),
    "tipo:pbi": ("0E8A16", "Product Backlog Item"),
    "tipo:task": ("C5DEF5", "Task técnica de um PBI"),
    "área:back": ("FBCA04", "Backend / agentes"),
    "área:front": ("F9D0C4", "Web client"),
    "área:infra": ("BFD4F2", "HF Space, Vercel, Supabase, CI"),
    "área:qa": ("D4C5F9", "Testes e evidências"),
    "área:docs": ("EDEDED", "Documentação"),
    "área:mobile": ("C2E0C6", "App Android"),
    "área:segurança": ("B60205", "Segurança"),
    "versão:v3": ("0B3C49", "homolog-v3"),
    "versão:v4": ("0B3C49", "homolog-v4"),
    "versão:v5": ("0B3C49", "homolog-v5"),
    "versão:v6": ("0B3C49", "homolog-v6"),
}


def gh(args, apply, capture=True):
    cmd = ["gh"] + args
    if not apply:
        print("[simulação]", " ".join(a if " " not in a else repr(a) for a in cmd[:8]), "..." if len(cmd) > 8 else "")
        return ""
    res = subprocess.run(cmd, capture_output=capture, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:4])}: {res.stderr.strip()}")
    return res.stdout.strip()


def read_body(path):
    text = open(path, encoding="utf-8").read()
    # remove o front matter
    if text.startswith("---"):
        text = text.split("---", 2)[2].lstrip("\n")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="v3, v4, v5 ou v6")
    a = ap.parse_args()

    items = json.load(open(os.path.join(OUT, "issues.json"), encoding="utf-8"))
    if a.only:
        items = [i for i in items if f"versão:{a.only}" in i["labels"]]

    created_path = os.path.join(OUT, "created.json")
    created = json.load(open(created_path)) if os.path.exists(created_path) else {}

    # 1. Labels
    for name, (color, desc) in LABELS.items():
        try:
            gh(["label", "create", name, "--repo", REPO, "--color", color, "--description", desc, "--force"], a.apply)
        except RuntimeError as e:
            print("aviso:", e)

    # 2. Milestones
    existing = []
    if a.apply:
        existing = json.loads(gh(["api", f"repos/{REPO}/milestones?state=all&per_page=100"], True) or "[]")
    have = {m["title"] for m in existing}
    for ms in sorted({i["milestone"] for i in items}):
        if ms not in have:
            gh(["api", f"repos/{REPO}/milestones", "-f", f"title={ms}"], a.apply)

    # 3. Issues (ordem do arquivo: pais antes dos filhos)
    for it in items:
        key = it["key"]
        if key in created:
            continue
        if a.apply:
            found = json.loads(gh(["issue", "list", "--repo", REPO, "--state", "all", "--search", f'"{it["title"]}" in:title', "--json", "number,title", "--limit", "5"], True) or "[]")
            match = [f for f in found if f["title"] == it["title"]]
            if match:
                created[key] = match[0]["number"]
                continue
        args = ["issue", "create", "--repo", REPO, "--title", it["title"], "--body-file", os.path.join(OUT, "issues", it["file"]),
                "--milestone", it["milestone"]]
        for lb in it["labels"]:
            args += ["--label", lb]
        if a.apply:
            # grava o corpo sem front matter em arquivo temporário
            tmp = os.path.join(OUT, ".body.md")
            open(tmp, "w", encoding="utf-8").write(read_body(os.path.join(OUT, "issues", it["file"])))
            args[args.index("--body-file") + 1] = tmp
            url = gh(args, True)
            created[key] = int(url.rstrip("/").split("/")[-1])
            json.dump(created, open(created_path, "w"), indent=2)
            print(f"{key} → #{created[key]}")
        else:
            gh(args, False)

    # 4. Sub-issues (pai ← filho)
    for it in items:
        parent = it["parent"]
        if not parent:
            continue
        if not a.apply:
            print(f"[simulação] vincular {it['key']} como sub-issue de {parent}")
            continue
        if parent not in created or it["key"] not in created:
            print("aviso: pai ou filho sem número:", parent, it["key"])
            continue
        child_id = json.loads(gh(["api", f"repos/{REPO}/issues/{created[it['key']]}"], True))["id"]
        try:
            gh(["api", "-X", "POST", f"repos/{REPO}/issues/{created[parent]}/sub_issues", "-F", f"sub_issue_id={child_id}"], True)
        except RuntimeError as e:
            if "already" not in str(e).lower():
                print("aviso:", e)

    if not a.apply:
        print(f"\nSimulação concluída: {len(items)} issues. Rode com --apply para criar.")


if __name__ == "__main__":
    sys.exit(main())
