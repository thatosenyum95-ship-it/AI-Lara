"""Validate the curated AI-Lara instruction dataset before training."""
import json
from pathlib import Path

PATH = Path(__file__).with_name("examples.jsonl")
ALLOWED_FEATURES = {"search","login","notes","todo","camera","calculator","offline","notifications","profile","database","home_screen"}
def main():
    rows=[]
    for number,line in enumerate(PATH.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: row=json.loads(line)
        except json.JSONDecodeError as exc: raise SystemExit(f"Baris {number}: JSON tidak valid: {exc}")
        if not isinstance(row.get("prompt"),str) or not row["prompt"].strip():
            raise SystemExit(f"Baris {number}: prompt kosong")
        target=row.get("target")
        if not isinstance(target,dict) or not isinstance(target.get("project_name"),str):
            raise SystemExit(f"Baris {number}: target/project_name tidak valid")
        features=target.get("features"); screens=target.get("screens")
        if not isinstance(features,list) or not isinstance(screens,list) or "home" not in screens:
            raise SystemExit(f"Baris {number}: features/screens tidak valid")
        unknown=set(features)-ALLOWED_FEATURES
        if unknown: raise SystemExit(f"Baris {number}: fitur tidak dikenal {sorted(unknown)}")
        rows.append(row)
    prompts=[r["prompt"].casefold() for r in rows]
    if len(prompts)!=len(set(prompts)): raise SystemExit("Ada prompt duplikat; perbaiki sebelum training.")
    if len(rows)<20: raise SystemExit(f"Dataset terlalu kecil untuk pipeline awal: {len(rows)} contoh; minimal 20.")
    print(f"OK: {len(rows)} contoh valid. Catatan: ini dataset prototipe, belum cukup untuk model produksi.")
if __name__=="__main__": main()
