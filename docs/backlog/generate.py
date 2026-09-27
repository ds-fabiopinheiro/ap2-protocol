# -*- coding: utf-8 -*-
"""Gera os arquivos de issue (Markdown) e o índice do backlog a partir de data.py."""
import json
import os
import shutil

from data import EPICS, REPO
from bdd import BDD
from gen_bdd import feature_text

OUT = os.path.join(os.path.dirname(__file__), "out")
ISS = os.path.join(OUT, "issues")

MILESTONE = {
    "v3": "v3 — Merchant Agent (homolog-v3)",
    "v4": "v4 — Shopping Agent v1 (homolog-v4)",
    "v5": "v5 — Jornada assistida no web client (homolog-v5)",
    "v6": "v6 — Go e Android (homolog-v6)",
}
AREA_LABEL = {"Back": "área:back", "Front": "área:front", "Infra": "área:infra", "QA": "área:qa",
              "Docs": "área:docs", "Mobile": "área:mobile", "Segurança": "área:segurança"}


def bullets(items):
    return "\n".join(f"- {i}" for i in items) if items else "- Nenhum."


def checklist(items):
    return "\n".join(f"- [ ] {i}" for i in items)


issues = []  # dicts: key, title, labels, milestone, parent, body, kind


def add(key, title, labels, milestone, parent, body, kind):
    issues.append(dict(key=key, title=title, labels=labels, milestone=milestone, parent=parent, body=body, kind=kind))


def fmt_fields(rows):
    out = ["| Campo | Valor |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in rows]
    return "\n".join(out)


for ep in EPICS:
    v = ep["version"]
    ms = MILESTONE[v]
    feats = ep["features"]
    body = f"""## Campos
{fmt_fields([("Tipo", "Épico"), ("Versão", v), ("Branch", f"`{ep['branch']}` (criado a partir de `{ep['base']}`)"), ("Space", f"`ds-fabiopinheiro/ap2-homolog-{v}`"), ("Milestone", ms), ("Features", str(len(feats)))])}

## Contexto
{ep['contexto']}

## Objetivo
{ep['objetivo']}

## Escopo incluído
{bullets(ep['incluido'])}

## Escopo excluído
{bullets(ep['excluido'])}

## Métrica de sucesso
{bullets(ep['metrica'])}

## Dependências
{bullets(ep['dependencias'])}

## Riscos
{bullets(ep['riscos'])}

## Features previstas
{bullets([f"{f['id']} · {f['title']}" for f in feats])}

## Premissas
{bullets(ep['premissas'])}

## Definição de pronto do épico
- [ ] Todas as features fechadas.
- [ ] PR `{ep['branch']}` revisado; tag `{v}.0.0` criada no último commit.
- [ ] CLAUDE.md e deploy/README.md atualizados no branch `{ep['branch']}`.
- [ ] Roteiro de regressão das versões anteriores executado.
"""
    add(ep["id"], ep["title"], ["tipo:épico", f"versão:{v}"], ms, None, body, "Épico")

    for f in feats:
        pbis = f["pbis"]
        fbody = f"""## Campos
{fmt_fields([("Tipo", "Feature"), ("Épico", ep['id']), ("Versão", v), ("PBIs", str(len(pbis)))])}

## Problema
{f['problema']}

## Solução proposta
{f['solucao']}

## Usuários impactados
{f['usuarios']}

## Regras de negócio
{bullets(f['rns'])}

## Fora de escopo
{bullets(f['fora'])}

## Dependências
{bullets(f['deps'])}

## Critérios de aceite
{checklist(f['criterios'])}

## PBIs
{bullets([f"{p['id']} · {p['title']}" for p in pbis])}
"""
        add(f["id"], f"{f['id']} · {f['title']}", ["tipo:feature", f"versão:{v}"], ms, ep["id"], fbody, "Feature")

        for p in pbis:
            hours = sum(t[4] for t in p["tasks"])
            bdd_section = ""
            if p["id"] in BDD:
                bdd_section = ("## Cenários de teste (BDD)\n"
                               f"Arquivo no pacote: `out/bdd/{p['id']}.feature`. Matriz de cobertura em `out/bdd/README.md`.\n\n"
                               "```gherkin\n" + feature_text(ep, p, BDD[p["id"]]).rstrip() + "\n```\n\n")
            pbody = f"""## Campos
{fmt_fields([("Tipo", "PBI"), ("Feature", f['id']), ("Versão", v), ("Story points (sugestão)", str(p['pts'])), ("Horas das tasks (sugestão)", f"{hours} h"), ("Depende de", ', '.join(p['deps']) or '—')])}

## Descrição
Como **{p['como']}**
Quero **{p['quero']}**
Para **{p['para']}**

**Contexto:** {p['contexto']}

## Regras de negócio
{bullets(p['rns'])}

## Fora de escopo
{bullets(p['fora'])}

## Critérios de aceite
{checklist(p['criterios'])}

## Tasks
{bullets([f"[{t[0]}] {t[1]} · {t[4]} h" for t in p['tasks']])}

{bdd_section}## Definition of Ready
- [ ] Critérios de aceite revisados pelo PO.
- [ ] Dependências concluídas ou planejadas na mesma sprint.
- [ ] Ambiente da versão disponível.
"""
            add(p["id"], f"{p['id']} · {p['title']}", ["tipo:pbi", f"versão:{v}"], ms, f["id"], pbody, "PBI")

            for i, (area, title, desc, dod, h) in enumerate(p["tasks"], 1):
                tid = f"{p['id']}.T{i}"
                tbody = f"""## Campos
{fmt_fields([("Tipo", "Task"), ("PBI", p['id']), ("Área", area), ("Versão", v), ("Estimativa (sugestão)", f"{h} h"), ("Branch de trabalho", f"`task/{v}-<nº da issue>-<resumo>` → PR para `{ep['branch']}`")])}

## Objetivo
{desc}

## Definição de pronto
- [ ] {dod}
- [ ] PR revisado e mesclado em `{ep['branch']}`.
"""
                add(tid, f"{tid} · [{area}] {title}", ["tipo:task", AREA_LABEL[area], f"versão:{v}"], ms, p["id"], tbody, "Task")

# ---------------------------------------------------------------------------
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(ISS)

for n, it in enumerate(issues, 1):
    fname = f"{n:03d}_{it['key']}.md"
    it["file"] = fname
    front = ["---", f"key: {it['key']}", f"title: {json.dumps(it['title'], ensure_ascii=False)}",
             f"kind: {it['kind']}", f"labels: {json.dumps(it['labels'], ensure_ascii=False)}",
             f"milestone: {json.dumps(it['milestone'], ensure_ascii=False)}", f"parent: {it['parent'] or ''}", "---", ""]
    with open(os.path.join(ISS, fname), "w", encoding="utf-8") as fh:
        fh.write("\n".join(front) + it["body"])

with open(os.path.join(OUT, "issues.json"), "w", encoding="utf-8") as fh:
    json.dump([{k: it[k] for k in ("key", "title", "kind", "labels", "milestone", "parent", "file")} for it in issues], fh, ensure_ascii=False, indent=2)

# Árvore e tabela
tree, table = [], ["| # | Tipo | Chave | Título | Pai | Estimativa (sugestão) | Depende de |", "|---|---|---|---|---|---|---|"]
n = 0
for ep in EPICS:
    tree.append(f"📊 {ep['id']} · {ep['title']}  (branch {ep['branch']})")
    n += 1; table.append(f"| {n} | Épico | {ep['id']} | {ep['title']} | — | — | {'—' if ep['base']=='homolog-deploy' else 'EP-V' + str(int(ep['version'][1:])-1)} |")
    for fi, f in enumerate(ep["features"]):
        lastf = fi == len(ep["features"]) - 1
        tree.append(f"{'└──' if lastf else '├──'} 🎯 {f['id']} · {f['title']}")
        n += 1; table.append(f"| {n} | Feature | {f['id']} | {f['title']} | {ep['id']} | — | {', '.join(f['deps'])} |")
        for pi, p in enumerate(f["pbis"]):
            lastp = pi == len(f["pbis"]) - 1
            pre = '    ' if lastf else '│   '
            tree.append(f"{pre}{'└──' if lastp else '├──'} 📋 {p['id']} · {p['title']} · {p['pts']} pts")
            n += 1; table.append(f"| {n} | PBI | {p['id']} | {p['title']} | {f['id']} | {p['pts']} pts | {', '.join(p['deps']) or '—'} |")
            for ti, t in enumerate(p["tasks"]):
                lastt = ti == len(p["tasks"]) - 1
                pre2 = pre + ('    ' if lastp else '│   ')
                tree.append(f"{pre2}{'└──' if lastt else '├──'} ✅ [{t[0]}] {t[1]} · {t[4]} h")
                n += 1; table.append(f"| {n} | Task | {p['id']}.T{ti+1} | [{t[0]}] {t[1]} | {p['id']} | {t[4]} h | — |")

with open(os.path.join(OUT, "tree.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(tree) + "\n")
with open(os.path.join(OUT, "table.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(table) + "\n")

# Resumo numérico
summary = {}
for ep in EPICS:
    fs = ep["features"]; ps = [p for f in fs for p in f["pbis"]]; ts = [t for p in ps for t in p["tasks"]]
    summary[ep["version"]] = dict(features=len(fs), pbis=len(ps), tasks=len(ts), pts=sum(p["pts"] for p in ps), horas=sum(t[4] for t in ts))
with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(summary, fh, ensure_ascii=False, indent=2)
print(json.dumps(summary, ensure_ascii=False), len(issues), "issues")
