"""Basic held-out evaluation: JSON validity and exact feature/screen set match."""
import json, os
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

ADAPTER_DIR=Path(os.environ.get("AILARA_OUTPUT_DIR","/content/drive/MyDrive/AI-Lara-Training/adapter"))
TEST_PATH=Path(os.environ.get("AILARA_TEST_PATH",ADAPTER_DIR/"held_out_test.jsonl"))
BASE_MODEL=os.environ.get("AILARA_BASE_MODEL","Qwen/Qwen2.5-1.5B-Instruct")
SYSTEM_PROMPT=("Kamu adalah AI-Lara, asisten perancang spesifikasi aplikasi Android. Balas hanya dengan JSON valid berisi tepat tiga kunci: project_name (string), features (array string), screens (array string). Gunakan fitur yang didukung: search, login, notes, todo, camera, calculator, offline, notifications, profile, database. Screens wajib berisi home; gunakan login, notes, tasks, profile, calculator, camera sesuai fitur yang relevan. Jangan sertakan markdown atau teks di luar JSON.")
def main():
    if not torch.cuda.is_available(): raise SystemExit("GPU diperlukan untuk evaluasi ini.")
    tok=AutoTokenizer.from_pretrained(ADAPTER_DIR,trust_remote_code=True)
    dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    q=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_use_double_quant=True,bnb_4bit_compute_dtype=dtype)
    base=AutoModelForCausalLM.from_pretrained(BASE_MODEL,quantization_config=q,device_map="auto",torch_dtype=dtype,trust_remote_code=True)
    model=PeftModel.from_pretrained(base,ADAPTER_DIR); model.eval()
    rows=[json.loads(s) for s in TEST_PATH.read_text(encoding="utf-8").splitlines() if s.strip()]
    valid=feature=screen=0
    for row in rows:
        msgs=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":row["prompt"]}]
        inp=tok.apply_chat_template(msgs,tokenize=True,add_generation_prompt=True,return_tensors="pt").to(model.device)
        with torch.no_grad(): out=model.generate(inp,max_new_tokens=160,do_sample=False,pad_token_id=tok.eos_token_id)
        raw=tok.decode(out[0][inp.shape[1]:],skip_special_tokens=True).strip()
        try:
            pred=json.loads(raw); valid+=1
            feature+=set(pred.get("features",[]))==set(row["target"].get("features",[]))
            screen+=set(pred.get("screens",[]))==set(row["target"].get("screens",[]))
        except Exception: pred={"parse_error":True,"raw":raw}
        print("\nPROMPT:",row["prompt"],"\nEXPECTED:",row["target"],"\nPREDICTED:",pred)
    n=max(1,len(rows))
    print(f"\nJSON valid: {valid}/{n} ({valid/n:.0%})")
    print(f"Exact feature match: {feature}/{n} ({feature/n:.0%})")
    print(f"Exact screen match: {screen}/{n} ({screen/n:.0%})")
    print("Small test set: metrics are indicative only, not evidence of production quality.")
if __name__=="__main__": main()
