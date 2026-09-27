# -*- coding: utf-8 -*-
"""Gera os arquivos .feature, o preview de testes e a verificação de cobertura."""
import os
import re

from bdd import BDD
from data import EPICS

OUT = os.path.join(os.path.dirname(__file__), "out", "bdd")
TIPO_TAG = {"positivo": "@positivo", "negativo": "@negativo", "borda": "@borda", "seguranca": "@seguranca",
            "performance": "@performance", "regressao": "@regressao"}


def pbis():
    for ep in EPICS:
        for f in ep["features"]:
            for p in f["pbis"]:
                yield ep, f, p


def feature_text(ep, p, b):
    lines = ["# language: pt", f"@{ep['version']} @{p['id']}", f"Funcionalidade: {b['feature']}",
             f"  PBI {p['id']} · {p['title']}", ""]
    if b["contexto"]:
        lines.append("  Contexto:")
        for i, s in enumerate(b["contexto"]):
            kw = s if i == 0 else s  # já vêm com "Dado"/"E"
            lines.append(f"    {kw}")
        lines.append("")
    for sc in b["cenarios"]:
        cid, tipo, nome, passos, origem = sc[:5]
        ex = sc[5] if len(sc) > 5 else None
        tags = [f"@{cid}", TIPO_TAG[tipo]]
        if "proposta" in origem:
            tags.append("@pendente-confirmacao")
        lines.append("  " + " ".join(tags))
        lines.append(f"  # Origem: {origem}")
        lines.append(f"  {'Esquema do Cenário' if ex else 'Cenário'}: {cid} · {nome}")
        for s in passos:
            lines.append(f"    {s}")
        if ex:
            lines.append("")
            lines.append("    Exemplos:")
            widths = [max(len(str(r[i])) for r in ex) for i in range(len(ex[0]))]
            for r in ex:
                lines.append("      | " + " | ".join(str(c).ljust(w) for c, w in zip(r, widths)) + " |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def coverage(p, b):
    """Mapeia CAn e RNnn da PBI para cenários; devolve (linhas da matriz, lacunas automáticas)."""
    rows, missing = [], []
    refs = [(sc[0], sc[4]) for sc in b["cenarios"]]
    for i, ca in enumerate(p["criterios"], 1):
        hit = [cid for cid, o in refs if re.search(rf"\bCA{i}\b", o)]
        rows.append((f"CA{i} – {ca}", "Critério de aceite", ", ".join(hit) or "—"))
        if not hit:
            missing.append(f"CA{i} sem cenário: {ca}")
    for rn in p["rns"]:
        code = rn.split(" ")[0]
        hit = [cid for cid, o in refs if re.search(rf"\b{code}\b(?! \()", o)]
        rows.append((rn, "Regra de negócio do PBI", ", ".join(hit) or "—"))
    others = sorted({o for _, o in refs if not re.search(r"\bCA\d", o)})
    for o in others:
        rows.append((o, "Regra da feature/épico ou task", ", ".join(cid for cid, oo in refs if oo == o)))
    return rows, missing


def main():
    os.makedirs(OUT, exist_ok=True)
    preview = ["# Cenários de teste (BDD) — backlog v3–v6", "",
               "Preview gerado a partir dos critérios de aceite e das regras de negócio de cada PBI. Nada foi vinculado a Test Plan ou criado no GitHub.", "",
               "**Parâmetros usados:** tipos positivo, negativo, borda e, quando há requisito ou risco declarado, segurança, performance e regressão · idioma pt-BR · formato Gherkin (`# language: pt`) · um arquivo `.feature` por PBI.", "",
               "**Tags:** `@vN` (versão), `@<PBI>`, `@CTnn`, tipo (`@positivo`, `@negativo`, `@borda`, `@seguranca`, `@performance`, `@regressao`) e `@pendente-confirmacao` para cenários que dependem de regra ainda não confirmada.", ""]
    totals = {"cenarios": 0}
    summary = ["| Versão | PBI | Cenários | Positivo | Negativo | Borda | Segurança | Performance | Regressão | CA sem cenário |", "|---|---|---|---|---|---|---|---|---|---|"]
    all_missing = []
    for ep, f, p in pbis():
        b = BDD[p["id"]]
        txt = feature_text(ep, p, b)
        fname = f"{p['id']}.feature"
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(txt)
        rows, missing = coverage(p, b)
        all_missing += [f"{p['id']}: {m}" for m in missing]
        cnt = {t: sum(1 for sc in b["cenarios"] if sc[1] == t) for t in TIPO_TAG}
        n = len(b["cenarios"]); totals["cenarios"] += n
        summary.append(f"| {ep['version']} | {p['id']} | {n} | {cnt['positivo']} | {cnt['negativo']} | {cnt['borda']} | {cnt['seguranca']} | {cnt['performance']} | {cnt['regressao']} | {len(missing)} |")
        preview += [f"## Preview — Cenários de teste · PBI {p['id']} {p['title']}", "",
                    f"Arquivo: `out/bdd/{fname}` · {n} cenários", "", "### Matriz de cobertura", "",
                    "| Regra / critério | Origem | Cenários |", "|---|---|---|"]
        preview += [f"| {r} | {o} | {c} |" for r, o, c in rows]
        preview += ["", "### Cenários", "", "```gherkin", txt.rstrip(), "```", "", "### Lacunas identificadas"]
        preview += [f"- {x}" for x in (b["lacunas"] + missing)] or ["- Nenhuma."]
        preview += ["", "### Premissas"] + ([f"- {x}" for x in b["premissas"]] or ["- Nenhuma."])
        preview += ["", "### Pendências para sincronizar",
                    "- Onde os cenários ficam no GitHub: seção \"Cenários de teste (BDD)\" da issue do PBI (já incluída no corpo gerado) e/ou arquivo `.feature` no repositório.",
                    "- Massa de teste e acesso aos Spaces/Supabase da versão.", ""]
        b["_text"] = txt
        b["_rows"] = rows
    head = preview[:8] + ["## Resumo", ""] + summary + ["", f"Total: {totals['cenarios']} cenários em {len(BDD)} PBIs. CA sem cenário: {len(all_missing)}.", ""]
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write("\n".join(head + preview[8:]))
    print(totals, "CA sem cenário:", all_missing)
    return BDD


if __name__ == "__main__":
    main()
